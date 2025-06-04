from fastapi import FastAPI, File, UploadFile
import os

app = FastAPI()

UPLOAD_FOLDER = "/path/to/uploaded/files"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"File '{file.filename}' saved at '{file_location}'"}