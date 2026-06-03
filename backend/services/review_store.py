pending_reviews = {}
def add_review(case_id, state):

    pending_reviews[case_id] = state


def get_review(case_id):

    return pending_reviews.get(case_id)


def remove_review(case_id):

    pending_reviews.pop(case_id, None)