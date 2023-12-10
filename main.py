import os
import re
import json
import base64
import humanize
from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

DATA_PATH=os.environ.get("DATA_PATH", "data/")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def make_boolean(value):
    true_values = [ "true", "yes", "y", "1", 1 ]
    false_values = [ "false", "no", "n", "0", 0 ]

    if type(value) == bool:
        return value

    if value.lower() in false_values:
        return False

    if value.lower() in true_values:
        return True

    return False

@app.get("/")
def read_root():
    return {
        "paths": [
            "/"
        ]
    }

@app.options("/{full_path:path}")
async def options_handler(list_name: str):
    """
    Handle OPTIONS requests for the specified endpoint.
    """
    return {}

@app.put("/{full_path:path}")
async def write(full_path: str, request: Request):
    # get file and folder path
    file_path = os.path.join(DATA_PATH, full_path)
    folder_path = os.path.dirname(file_path)

    # ensure all folder exists
    try:
        os.makedirs(folder_path, exist_ok=True)
    except FileExistsError as error:
        key = error.filename
        error_message = {"msg": f"key '{key}' is already a key!"}
        return JSONResponse(content=error_message, status_code=409)

    # write base64 encoded data
    exists = os.path.exists(file_path)
    size = 0

    data = base64.b64encode(await request.body())
    try:
        with open(file_path, "wb") as f:
            f.write(data)
        size = os.path.getsize(file_path)
    except IsADirectoryError as error:
        key_path = error.filename
        error_message = {"msg": f"key '{key_path}' is already part of a key!"}
        return JSONResponse(content=error_message, status_code=409)

    return {
        "created": not exists,
        "size": size,
        "size_human": humanize.naturalsize(size)
    }

@app.get("/{full_path:path}")
async def read(full_path: str, plain = False, b64 = False, prefix = None):
    b64 = make_boolean(b64)
    plain = make_boolean(plain)
    path = os.path.join(DATA_PATH, full_path)

    # get keys (files) if path is a folder
    if os.path.isdir(path):
        keys = os.listdir(path)

        if prefix:
            # Use the filter() function to filter strings that start with the prefix
            keys = list(filter(lambda item: item.startswith(prefix), keys))

        return {"keys": keys}

    if os.path.isfile(path):
        with open(path, 'rb') as f:
            data = f.read()

        if plain:
            data = base64.b64decode(data)
            return Response(content=data, media_type="text/plain")

        size = os.path.getsize(path)
        timestamp = os.path.getmtime(path)
        iso8601_date_time = datetime.utcfromtimestamp(timestamp).isoformat()

        if not b64:
            data = base64.b64decode(data)

        return {
            "size": size,
            "size_human": humanize.naturalsize(size),
            "timestamp": iso8601_date_time,
            "content": data
        }

    error_message = {"msg": f"key '{path}' not found!"}
    return JSONResponse(content=error_message, status_code=404)