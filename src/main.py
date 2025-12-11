from fastapi import FastAPI
from pydantic import BaseModel
from utils import process_image


class ImageRequest(BaseModel):
    SoDinhDanh: str
    HinhAnh: str


app = FastAPI()

@app.get("/manage/health")
def health_check():
    return {
        "status": 200, 
        "description": "Service is healthy"
    }


@app.post("/api/upload")
def upload(req: ImageRequest):
    file_path = process_image(req.SoDinhDanh, req.HinhAnh)
    return {
        "status": 200,
        "description": "Success",
        "file_path": file_path
    }