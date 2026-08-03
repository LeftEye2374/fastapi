from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse

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




