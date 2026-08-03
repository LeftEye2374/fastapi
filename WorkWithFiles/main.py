from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.psot("/files")
async def upload_files():
    ...



