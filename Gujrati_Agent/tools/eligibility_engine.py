import json
from typing import Dict

def load_rules(path="data/rules_gu.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def check_eligibility(profile: Dict, scheme_rule: Dict) -> Dict:
    missing = []
    required_fields = scheme_rule.get("required_fields", [])
    for rf in required_fields:
        if profile.get(rf) in (None, "", []):
            missing.append(rf)

    if missing:
        return {"eligible": False, "missing_fields": missing, "reasons": ["માહિતી અધૂરી છે"], "documents": scheme_rule.get("documents", [])}

    reasons = []
    rules = scheme_rule.get("rules", {})
    age = profile.get("age") or 0
    income = profile.get("income_monthly") or 0
    caste = profile.get("caste_category")
    farmer = profile.get("farmer")
    student = profile.get("student")

    if "min_age" in rules and age < rules["min_age"]:
        reasons.append(f"ઉંમર {rules['min_age']} થી ઓછી")
    if "max_age" in rules and age > rules["max_age"]:
        reasons.append(f"ઉંમર {rules['max_age']} થી વધુ")
    if "income_cap" in rules and income > rules["income_cap"]:
        reasons.append("આવક મર્યાદા કરતાં વધુ")
    if "requires_caste" in rules and rules["requires_caste"] and caste not in rules["requires_caste"]:
        reasons.append("જાતિ શ્રેણી અનુકૂળ નથી")
    if "requires_farmer" in rules and rules["requires_farmer"] and not farmer:
        reasons.append("ખેડૂત હોવું જરૂરી")
    if "requires_student" in rules and rules["requires_student"] and not student:
        reasons.append("વિદ્યાર્થી હોવું જરૂરી")

    eligible = len(reasons) == 0
    return {
        "eligible": eligible,
        "missing_fields": [],
        "reasons": ["પાત્ર"] if eligible else reasons,
        "documents": scheme_rule.get("documents", [])
    }
