# retriever_server.py
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import json, os

app = FastAPI(title="BYC Retriever")

BASE = os.path.join(os.path.dirname(__file__), "build")
DOCS = os.path.join(BASE, "chunks.jsonl")  # adapta si tu archivo es otro

def load_docs():
    docs = []
    if os.path.exists(DOCS):
        with open(DOCS, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    docs.append(json.loads(line))
                except:
                    pass
    return docs

DOCS_MEM = load_docs()

@app.get("/search")
def search(q: str = Query(""), top_k: int = 6):
    ql = q.lower()
    results = []
    for d in DOCS_MEM:
        title = (d.get("title") or "").lower()
        body  = (d.get("body")  or "").lower()
        if ql in title or ql in body:
            results.append({
                "doc_id": d.get("id") or d.get("doc_id") or "",
                "title": d.get("title") or "",
                "body":  d.get("body") or "",
                "url":   d.get("url") or ""
            })
        if len(results) >= top_k:
            break
    return JSONResponse({"results": results})
