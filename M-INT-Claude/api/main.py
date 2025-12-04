from dotenv import load_dotenv
load_dotenv()
import time
from fastapi import FastAPI
from schemas import AnalyzeRequest, AnalyzeResponse
from pipeline.pipeline_runner import run_pipeline

app = FastAPI()


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    start = time.perf_counter()  # High-precision timer

    result = run_pipeline(req.domain, req.payload)

    end = time.perf_counter()
    processing_time = end - start

    return AnalyzeResponse(
        domain=req.domain,
        result=result,
        processing_time=processing_time,  # ⬅ Add this field
    )
