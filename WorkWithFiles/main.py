from fastapi import FastAPI, File, UploadFile
from starlette.responses import FileResponse, StreamingResponse

app = FastAPI()


@app.post("/file")
async def upload_file(uploaded_file : UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f"1_{filename}", "wb") as f:
        f.write(file.read())

@app.post("/files")
async def upload_files(uploaded_files : list[UploadFile]):
    for uploaded_file in uploaded_files:
        count = 1
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(f"{count}_{filename}", "wb") as f:
            f.write(file.read())
        count += 1



@app.get("/files/{filename}")
async def get_file(filename : str):
    return FileResponse(filename)

def iterfile(filename : str):
    with open(filename, "rb") as f:
        while chunk :=  f.read(1024 * 1024):
            yield chunk

@app.get("/files/streaming/{filename}")
async def get_streaming_file(filename : str):
    return StreamingResponse(iterfile(filename), media_type="video/mp4")

