# app/main.py

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from fastapi import Form
from utils import process_image

app = FastAPI()

# Static files and templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/hello", response_class=PlainTextResponse)
async def say_hello():
    return "Jai Daleshwar"

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # path to transparent frame image
    frame_path = os.path.join("static", "frame.png")  
    output_filename = process_image(file.file, frame_path)
    download_url = f"/static/{output_filename}"
    return JSONResponse(content={"url": download_url})

@app.post("/generate")
async def generate_hq_image(
    file: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    scale: float = Form(...),
    canvas_width: int = Form(...),
    canvas_height: int = Form(...)
):
    frame_path = os.path.join("static", "frame.png")
    filename = process_image(
        file.file, frame_path,
        x=x, y=y, scale=scale,
        canvas_width=canvas_width, canvas_height=canvas_height
    )
    return JSONResponse(content={"url": f"/static/{filename}"})
    print("📥 Received image with:")
    print("x =", x, "y =", y, "scale =", scale)
    return JSONResponse(content={"url": f"/static/{filename}"})
