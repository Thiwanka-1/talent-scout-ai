import difflib

def calculate_fuzzy_match_logic(candidate_skills_str: str, job_skills_str: str):
    """Advanced Fuzzy Matching Algorithm (Runs deterministically outside the LLM)"""
    c_skills = [s.strip() for s in candidate_skills_str.split(',') if s.strip()]
    j_skills = [s.strip() for s in job_skills_str.split(',') if s.strip()]

    matched = []
    missing = []
    
    for js in j_skills:
        is_matched = False
        for cs in c_skills:
            if js.lower() in cs.lower() or cs.lower() in js.lower():
                is_matched = True
                break
            if difflib.SequenceMatcher(None, js.lower(), cs.lower()).ratio() > 0.6:
                is_matched = True
                break
                
        if is_matched:
            matched.append(js)
        else:
            missing.append(js)

    total = len(j_skills)
    match_pct = round((len(matched) / total) * 100, 2) if total > 0 else 0.0
    return match_pct, missing