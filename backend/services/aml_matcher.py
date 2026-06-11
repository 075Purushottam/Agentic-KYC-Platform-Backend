import json
import re
from rapidfuzz import fuzz

class AMLScreeningEngine:
    def __init__(self, ofac_file: str, pep_file: str):

        with open(ofac_file, "r", encoding="utf-8") as f:
            self.ofac_data = json.load(f)

        with open(pep_file, "r", encoding="utf-8") as f:
            self.pep_data = json.load(f)
   # --------------------------------------------------
   # Normalization
   # --------------------------------------------------
    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
        text = str(text).lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    # --------------------------------------------------
    # Matching Helpers
    # --------------------------------------------------
    def calculate_name_score(
        self,
        customer_name,
        watchlist_name
    ):
        customer_name = self.normalize_text(customer_name)
        watchlist_name = self.normalize_text(watchlist_name)
        return fuzz.token_set_ratio(
            customer_name,
            watchlist_name
        )
    def calculate_alias_score(
        self,
        customer_name,
        aliases
    ):
        
        if not aliases:
                return 0

        aliases = [a for a in aliases if a and a.lower() != "nan"]

        scores = [
            self.calculate_name_score(customer_name, alias)
            for alias in aliases
        ]

        return max(scores) if scores else 0

    def calculate_dob_score(
        self,
        customer_dob,
        record_dob
    ):
        
        if not customer_dob or not record_dob:
                return 0

        if isinstance(record_dob, list):
            record_dob = record_dob[0]

        return 100 if str(customer_dob).strip() in str(record_dob) else 0

    def calculate_country_score(
        self,
        customer_country,
        record_country
    ):
        
        if not customer_country or not record_country:
                return 0

        if isinstance(record_country, list):
            record_country = record_country[0]

        return 100 if self.normalize_text(customer_country) == self.normalize_text(record_country) else 0

    def calculate_address_score(
        self,
        customer_address,
        addresses
    ):
        if not customer_address or not addresses:
            return 0
        best_score = 0
        for address in addresses:
            score = fuzz.token_set_ratio(
                self.normalize_text(customer_address),
                self.normalize_text(address)
            )
            best_score = max(
                best_score,
                score
            )
        return best_score
    # --------------------------------------------------
    # Risk Logic
    # --------------------------------------------------
    def calculate_match_score(
        self,
        name_score,
        alias_score,
        dob_score,
        country_score,
        address_score
    ):
        best_name_score = max(
            name_score,
            alias_score
        )
        score = (
            best_name_score * 0.50
            + dob_score * 0.25
            + country_score * 0.15
            + address_score * 0.10
        )
        return round(score, 2)
    # --------------------------------------------------
    # Screening
    # --------------------------------------------------
    def screen_dataset(
        self,
        customer,
        dataset,
        source_name
    ):
        matches = []
        for row in dataset:
            record_country = (
                row.get("country")
                or row.get("countries",[0])
            )
            name_score = self.calculate_name_score(
                customer.get("name"),
                row.get("name")
            )
            # if name_score>=80:
            #     print(name_score)
            #     print(customer.get("name"))
            alias_score = self.calculate_alias_score(
                customer.get("name"),
                row.get("aliases", [])
            )
            dob_score = self.calculate_dob_score(
                customer.get("dob"),
                row.get("dob")
            )
            country_score = self.calculate_country_score(
                customer.get("country"),
                record_country
            )
            address_score = self.calculate_address_score(
                customer.get("address"),
                row.get("addresses", [])
            )
            final_score = self.calculate_match_score(
                name_score,
                alias_score,
                dob_score,
                country_score,
                address_score
            )
            if final_score >= 70:
                reasons = []
                if max(name_score, alias_score) >= 85:
                    reasons.append(
                        f"Strong name match ({max(name_score, alias_score):.1f})"
                    )
                if dob_score == 100:
                    reasons.append(
                        "Date of birth matched"
                    )
                if country_score == 100:
                    reasons.append(
                        "Nationality matched"
                    )
                if address_score >= 85:
                    reasons.append(
                        "Address matched"
                    )
                matches.append(
                    {
                        "source": source_name,
                        "matched_entity": row.get("name"),
                        "match_score": final_score,
                        "reason": reasons,
                        "record": row
                    }
                )
        matches.sort(
            key=lambda x: x["match_score"],
            reverse=True
        )
        return matches
    # --------------------------------------------------
    # Main AML Check
    # --------------------------------------------------
    def run(
        self,
        customer
    ):
        active_signals = []
        reasons = []
        sources = []
        risk_score = 0
        # -----------------------
        # OFAC Screening
        # -----------------------
        ofac_matches = self.screen_dataset(
            customer,
            self.ofac_data,
            "OFAC"
        )
        if ofac_matches:
            best_match = ofac_matches[0]
            active_signals.append(
                "SANCTIONS_MATCH"
            )
            risk_score += 70
            reasons.extend(
                best_match["reason"]
            )
            reasons.append(
                "Sanctions list match detected"
            )
            sources.append(
                {
                    "dataset": "OFAC",
                    "matched_entity":
                        best_match["matched_entity"],
                    "match_score":
                        best_match["match_score"]
                }
            )
        # -----------------------
        # PEP Screening
        # -----------------------
        pep_matches = self.screen_dataset(
            customer,
            self.pep_data,
            "PEP"
        )
        if pep_matches:
            best_match = pep_matches[0]
            active_signals.append(
                "PEP_MATCH"
            )
            risk_score += 30
            reasons.extend(
                best_match["reason"]
            )
            roles = (
                best_match["record"]
                .get("roles", [])
            )
            if roles:
                reasons.append(
                    f"PEP role identified: {', '.join(roles)}"
                )
            sources.append(
                {
                    "dataset": "PEP",
                    "matched_entity":
                        best_match["matched_entity"],
                    "match_score":
                        best_match["match_score"]
                }
            )
        risk_score = min(
            risk_score,
            100
        )
        return {
            "risk_score": risk_score,
            "active_signals": active_signals,
            "reason": list(set(reasons)),
            "source": sources
        }