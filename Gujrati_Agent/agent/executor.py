from tools.scheme_retrieval import keyword_retrieve
from tools.eligibility_engine import load_rules, check_eligibility
from tools.application_api import submit_application

class Executor:
    def __init__(self):
        self.rules = load_rules()

    def retrieve(self, query, profile):
        return keyword_retrieve(query=query, profile=profile, top_k=5)

    def check(self, profile, schemes):
        results = []
        for s in schemes:
            rule = self.rules.get(s["id"], {"required_fields": ["age","income_monthly"], "rules": {}, "documents": ["આધારકાર્ડ"]})
            res = check_eligibility(profile, rule)
            results.append({"scheme": s, "result": res})
        return results

    def get_documents_for_scheme(self, scheme_id):
        meta = self.rules.get(scheme_id, {})
        return meta.get("documents", ["આધારકાર્ડ"])

    def apply(self, scheme_id, profile, documents):
        return submit_application(scheme_id, profile, documents)
