import fitz
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class ResearchAgent:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.docs = []  # list of tuples (filename, text)

    def _extract_text(self, filename, file_bytes):
        if not filename or not file_bytes:
            return None
        if not filename.lower().endswith(".pdf"):
            return None
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = " ".join([p.get_text() for p in doc])
        return text

    def _add_to_index(self, text, filename):
        embeddings = self.model.encode([text])
        if self.index is None:
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.docs.append((filename, text))

    def _search(self, query, topk=1):
        if self.index is None:
            return []
        q_emb = self.model.encode([query]).astype(np.float32)
        D, I = self.index.search(q_emb, topk)
        return [self.docs[i] for i in I[0]]

    def _summarize(self, text, max_sent=3):
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        return ". ".join(sentences[:max_sent]) + ("" if len(sentences) <= max_sent else "...")

    def handle(self, query, filename, file_bytes):
        text = self._extract_text(filename, file_bytes) if file_bytes else None
        if text:
            self._add_to_index(text, filename)

        q_lower = (query or "").lower()

        if "summar" in q_lower:
            if text:
                return {"type":"text","text": self._summarize(text)}
            results = self._search(query, topk=1)
            if results:
                return {"type":"text","text": self._summarize(results[0][1])}
            return {"text":"No PDF indexed. Upload PDFs first."}

        if "keyword" in q_lower:
            if text:
                words = [w for w in text.split() if len(w) > 5]
                top_words = list(dict.fromkeys(words))[:10]
                return {"type":"text","text": ", ".join(top_words)}
            return {"text":"No PDF provided."}

        if "which paper" in q_lower or "yolo" in q_lower:
            results = self._search(query, topk=3)
            if results:
                return {"type":"text","text": f"Best match: {results[0][0]}"}
            return {"type":"text","text": "No relevant paper found."}

        return {"type":"text","text": text[:400] + "..." if text else "No PDF provided."}
