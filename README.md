# PythonLocalPhoneSpeechDownloader,a  Local Call Log Downloader

A lightweight, asynchronous FastAPI microservice designed to stream remote `.aac` audio files (such as call logs or voice recordings) and save them to a designated local directory with sanitized file naming conventions.

---

## Features

* **Asynchronous File Streaming:** Utilizes `httpx.AsyncClient` to stream large audio files efficiently without loading the entire payload into RAM.
* **Configurable Environment:** Supports `.env` file management for local storage paths and server ports via `python-dotenv`.
* **Filename Sanitization:** Strips invalid path characters from incoming input variables to prevent file system errors and path traversal vulnerabilities.
* **RESTful Endpoint:** Single `POST` endpoint accepting structured JSON payloads parsed and validated with Pydantic.

---

## Requirements

* Python 3.9+
* Dependencies listed in `requirements.txt`:
* `fastapi`
* `uvicorn`
* `httpx`
* `pydantic`
* `python-dotenv`



---

## Setup & Installation

1. **Clone the repository:**
```bash
git clone https://github.com/baban9999ytr/PythonLocalPhoneSpeechDownloader.git
cd PythonLocalPhoneSpeechDownloader

```


2. **Create and activate a virtual environment:**
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

```


3. **Install required packages:**
```bash
pip install -r requirements.txt

```


4. **Configure Environment Variables:**
Copy `.env.example` to create your local `.env` file:
```bash
cp .env.example .env

```


Modify `.env` to suit your environment settings:
```env
DOWNLOAD_DIR=downloads
HOST=0.0.0.0
PORT=8000

```



---

## Usage

### 1. Run the Server

Start the application using Python or Uvicorn directly:

```bash
python main.py

```

*The API will be accessible at `http://localhost:8000` by default.*

### 2. Interactive API Documentation

Once running, view Swagger UI documentation in your browser at:
`http://localhost:8000/docs`

---

## API Reference

### Download Audio File

* **Endpoint:** `/download`
* **Method:** `POST`
* **Content-Type:** `application/json`

#### Request Body Example

```json
{
  "url": "https://example.com/audio/sample_recording.aac",
  "phone_number": "+1234567890",
  "start_time": "2026-08-05_16-00-00"
}

```

#### Successful Response (`200 OK`)

```json
{
  "status": "success",
  "saved_path": "downloads/+1234567890_2026-08-05_16-00-00.aac"
}

```

#### Error Handling

* **`400/404 Bad Request / Not Found`**: Returns upstream HTTP status code if the remote source link is unreachable or fails to return a `200 OK`.
* **`500 Internal Server Error`**: Catches file system permissions errors or streaming interruptions during processing.

---

## Project Structure

```text
PythonLocalPhoneSpeechDownloader/
│
├── main.py              # Application entrypoint & endpoint logic
├── requirements.txt     # Python project dependencies
├── .env.example         # Example environment configuration template
├── .gitignore           # Ignored files (virtualenvs, local .env, downloads)
└── downloads/           # Default local storage target for downloaded AAC files

```

---

## License

Distributed under the APACHE License. See `LICENSE` for details.
