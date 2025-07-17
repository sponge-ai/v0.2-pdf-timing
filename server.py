from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
import time
load_dotenv()

app = FastAPI()
client = OpenAI()

@app.get("/")
def read_root():
    return FileResponse("static/main.html")

@app.post("/upload")
async def post_response(
    file: UploadFile = File(...), 
    prompt: Optional[str] = Form("Summarize this file: ")
):
    start_time = time.time()
    
    file_content = await file.read()
    read_time = time.time()

    file_response = client.files.create(
        file = (file.filename, file_content),
        purpose = "user_data"
    )
    upload_time = time.time()
    
    file_id = file_response.id

    response = client.responses.create(
        model = "gpt-4o",
        input = [
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": prompt },
                    { "type": "input_file", "file_id": file_id }
                ]
            }
        ]
    )
    response_time = time.time()

    print(f"File read: {read_time - start_time:.2f}s")
    print(f"OpenAI upload: {upload_time - read_time:.2f}s")
    print(f"OpenAI response: {response_time - upload_time:.2f}s")
    print(f"Total: {response_time - start_time:.2f}s")

    return response.output[0].content[0].text