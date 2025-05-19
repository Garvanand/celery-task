from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from ..tasks.embedding_tasks import process_file_and_generate_embeddings
from ..core.config import settings
from typing import List
import asyncio

router = APIRouter()

@router.post("/files/process")
async def process_files(files: List[UploadFile]):
    """Process multiple files and generate embeddings"""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    tasks = []
    for file in files:
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} is too large. Maximum size is {settings.MAX_FILE_SIZE/1024/1024}MB"
            )
        
        task = process_file_and_generate_embeddings.delay(content, file.filename)
        tasks.append({"filename": file.filename, "task_id": task.id})
    
    return JSONResponse(
        content={
            "message": "Files processing started",
            "tasks": tasks
        },
        status_code=202
    )

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a task"""
    task = process_file_and_generate_embeddings.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        response = {
            'status': 'pending',
            'task_id': task_id,
        }
    elif task.state == 'SUCCESS':
        response = {
            'status': 'completed',
            'task_id': task_id,
            'result': task.result
        }
    elif task.state == 'FAILURE':
        response = {
            'status': 'failed',
            'task_id': task_id,
            'error': str(task.result)
        }
    else:
        response = {
            'status': task.state,
            'task_id': task_id,
        }
    
    return JSONResponse(content=response) 