from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from agents.data_agent import DataAgent
from agents.research_agent import ResearchAgent
from agents.orchestrator import Orchestrator

app = FastAPI(title="Multi-Agent Backend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

data_agent = DataAgent()
research_agent = ResearchAgent()
orchestrator = Orchestrator(data_agent, research_agent)

@app.post("/data-agent/query")
async def data_query(query: str = Form(...), file: UploadFile | None = File(None)):
    file_bytes = await file.read() if file else None
    return data_agent.handle(query, file.filename if file else None, file_bytes)

@app.post("/research-agent/query")
async def research_query(query: str = Form(...), file: UploadFile | None = File(None)):
    file_bytes = await file.read() if file else None
    return research_agent.handle(query, file.filename if file else None, file_bytes)

@app.post("/orchestrate")
async def orchestrate(query: str = Form(...), file: UploadFile | None = File(None)):
    file_bytes = await file.read() if file else None
    return orchestrator.route(query, file.filename if file else None, file_bytes)
