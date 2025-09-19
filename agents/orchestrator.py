import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class Orchestrator:
    def __init__(self, data_agent, research_agent):
        self.data_agent = data_agent
        self.research_agent = research_agent
        model_path = os.path.join(os.path.dirname(__file__), "classifier.pkl")
        if os.path.exists(model_path):
            self.vectorizer, self.clf = joblib.load(model_path)
        else:
            # Train quick dummy classifier on sample keywords
            texts = [
                "show me sales trends for august",
                "plot revenue by product",
                "summarize this paper",
                "extract keywords from pdf",
                "which paper discusses YOLOv8"
            ]
            labels = ["data", "data", "research", "research", "research"]
            self.vectorizer = TfidfVectorizer()
            X = self.vectorizer.fit_transform(texts)
            self.clf = LogisticRegression().fit(X, labels)
            joblib.dump((self.vectorizer, self.clf), model_path)

    def route(self, query, filename, file_bytes):
        X = self.vectorizer.transform([query])
        label = self.clf.predict(X)[0]
        if label == "data":
            return self.data_agent.handle(query, filename, file_bytes)
        else:
            return self.research_agent.handle(query, filename, file_bytes)
