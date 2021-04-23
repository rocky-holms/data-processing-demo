"""Routes for files."""

import base64
import json
import logging
import os
from io import StringIO
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse
from src.api.routers.dependencies import get_api_key
from src.api.routers.responses import file_responses
from src.celery.worker import celery_conn
from src.mongo.query import (
    get_all_records_db,
    get_by_customer_by_class,
    get_by_customer_by_id,
    get_by_customer_by_travel_type,
    get_by_customer_by_type,
)
from starlette.responses import JSONResponse

router = APIRouter(
    prefix="/data",
    dependencies=[Depends(get_api_key)],
    tags=["Data"],
)

data_task_name = os.environ.get("DATA_TASK_NAME")


@router.post("/upload", status_code=status.HTTP_202_ACCEPTED, responses=file_responses)
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        task = celery_conn.send_task(data_task_name, args=[contents])
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File could not be uploaded: Filename-{file.filename}",
        )

    return JSONResponse(
        content=f"Processing file now. Job ID: {task.id}",
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.post(
    "/multi-upload", status_code=status.HTTP_202_ACCEPTED, responses=file_responses
)
async def multi_upload(files: List[UploadFile] = File(...)):
    file_data = []

    for file in files:
        try:
            task = celery_conn.send_task(data_task_name, args=[file.file.read()])
            file_data.append({"Filename": file.filename, "Process ID": task.id})
        except Exception as e:
            logging.error(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File could not be uploaded: Filename-{file.filename}",
            )

    return JSONResponse(
        content=f"Processing files now. Job details: {file_data}",
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.get("/status/{id}")
def upload_status(id: str):
    task = celery_conn.AsyncResult(id)
    if task.state == "SUCCESS":
        response = {"status": task.state, "result": task.result, "task_id": id}
    elif task.state == "FAILURE":
        response = json.loads(
            task.backend.get(task.backend.get_key_for_task(task.id)).decode("utf-8")
        )
        del response["children"]
        del response["traceback"]
    else:
        response = {"status": task.state, "result": task.info, "task_id": id}
    return response


@router.get("/records")
async def get_all_records():
    data = get_all_records_db()
    revised_data = StreamingResponse(StringIO(data), media_type="application/yaml")
    return revised_data


@router.get("/records/query/customer-type/{customer_type}")
async def query_by_customer_type(customer_type: str):
    data = get_by_customer_by_type(customer_type)
    revised_data = StreamingResponse(StringIO(data), media_type="application/yaml")
    return revised_data


@router.get("/records/query/travel-type/{travel_type}")
async def query_by_travel_type(travel_type: str):
    data = get_by_customer_by_travel_type(travel_type)
    revised_data = StreamingResponse(StringIO(data), media_type="application/yaml")
    return revised_data


@router.get("/records/query/class/{class_type}")
async def query_by_customer_class(class_type: str):
    data = get_by_customer_by_class(class_type)
    revised_data = StreamingResponse(StringIO(data), media_type="application/yaml")
    return revised_data


@router.get("/records/query/class/{customer_id}")
async def query_by_customer_id(customer_id: int):
    data = get_by_customer_by_id(customer_id)
    revised_data = StreamingResponse(StringIO(data), media_type="application/yaml")
    return revised_data
