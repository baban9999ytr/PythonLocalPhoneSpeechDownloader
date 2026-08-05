import os
import re
from pathlib import Path
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl

load_dotenv()

app = FastAPI(title="Local Call Log Downloader")

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR_ENV = os.getenv("DOWNLOAD_DIR")
TARGET_DIR = Path(DOWNLOAD_DIR_ENV) if DOWNLOAD_DIR_ENV else (BASE_DIR / "downloads")

class DownloadRequest(BaseModel):
    url: HttpUrl
    phone_number: str
    start_time: str

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name)

@app.post("/download", status_code=status.HTTP_200_OK)
async def download_file(payload: DownloadRequest):
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    safe_phone = sanitize_filename(payload.phone_number)
    safe_time = sanitize_filename(payload.start_time)
    
    file_name = f"{safe_phone}_{safe_time}.aac"
    file_path = TARGET_DIR / file_name

    try:
        print(f"Async Downloading: {payload.url} -> {file_path}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("GET", str(payload.url)) as response:
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code, 
                        detail="Failed to fetch file from remote source."
                    )
                
                with open(file_path, "wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)

        return {"status": "success", "saved_path": str(file_path)}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Download failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An error occurred during file download."
        )

if __name__ == "__main__":
    import uvicorn
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=HOST, port=PORT)