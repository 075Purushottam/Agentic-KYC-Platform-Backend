case_store = {}

def save_case(case_id,state):
    case_store[case_id] = state

def get_case(case_id):
    return case_store.get(case_id)