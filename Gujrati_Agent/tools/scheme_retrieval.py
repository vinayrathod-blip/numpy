import json
from typing import List, Dict

def load_schemes(path="data/schemes_gu.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def keyword_retrieve(query: str, profile: Dict, top_k: int = 5) -> List[Dict]:
    corpus = load_schemes()
    q = (query or "").lower()
    scored = []
    for s in corpus:
        text = (s.get("title","") + " " + s.get("summary","") + " " + " ".join(s.get("tags",[]))).lower()
        score = sum([1 for kw in q.split() if kw in text])
        # Simple district filter
        districts = s.get("districts")
        if districts and profile.get("district") and profile["district"] not in districts and "All" not in districts:
            continue
        scored.append((score, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in scored[:top_k]]
