from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import grpc_client
import os

from dto.score import ClientData

class HealthResponse(BaseModel):
    status: str
    grpc_status: str

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Initialize gRPC client

    host = os.getenv('GRPC_HOST', 'localhost')
    port = int(os.getenv('GRPC_PORT', '50051'))
    app.state.grpc_client = grpc_client.CreditScoringClient(host, port)

@app.on_event("shutdown")
async def shutdown_event():
    # Clean up gRPC client
    app.state.grpc_client.close()

@app.post("/score")
def score(data: ClientData):
    try:
        result = app.state.grpc_client.score_credit(
            age=data.age,
            income=data.income,
            education=data.education,
            work=data.work,
            car=data.car
        )
        
        return {
            "approved": result['approved'],
            "score": result['score'],
            "message": result['message']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))