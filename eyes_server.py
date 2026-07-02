from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyautogui
import mss
from PIL import Image
import base64
import os
from io import BytesIO
import cv2
import speech_recognition as sr

# Import directly from the local actions
from ui_extraction import extract_interactive_elements
from actions import launch_application, focus_app, type_unicode_smart

app = FastAPI(title="ARKAIOS Eyes & Ears Bridge (Foreground Session 1)")

class ClickRequest(BaseModel):
    x: int
    y: int
    clicks: int = 1
    button: str = "left"

class TypeRequest(BaseModel):
    text: str

class HotkeyRequest(BaseModel):
    keys: list[str]

class AppRequest(BaseModel):
    app_name: str

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Eyes and Ears are active!"}

@app.get("/webcam")
def take_webcam_picture():
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise Exception("Cannot open webcam")
        
        # Give camera time to warm up and adjust exposure
        for _ in range(5):
            cap.read()
            
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise Exception("Failed to grab frame from webcam")
            
        # Convert CV2 BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        
        # Resize to save bandwidth
        img.thumbnail((1280, 720))
        
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        return {"webcam_base64": b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/listen")
def listen_microphone():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            # Listen for up to 5 seconds
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        
        # Recognize using Google Web Speech API (Free, no key required)
        text = recognizer.recognize_google(audio, language="es-ES")
        return {"transcription": text}
    except sr.WaitTimeoutError:
        return {"transcription": "[No se detectó voz]"}
    except sr.UnknownValueError:
        return {"transcription": "[Audio incomprensible]"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/extract_ui")
def extract_ui():
    try:
        elements = extract_interactive_elements()
        return {"elements": elements}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/screenshot")
def take_screenshot():
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            shot = sct.grab(monitor)
            img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
            img = img.resize((1280, 720))
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return {"screenshot_base64": b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/click")
def click(req: ClickRequest):
    try:
        pyautogui.click(x=req.x, y=req.y, clicks=req.clicks, button=req.button)
        return {"status": f"Clicked at ({req.x}, {req.y})"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/type")
def type_text(req: TypeRequest):
    try:
        type_unicode_smart(req.text)
        return {"status": "Typed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/hotkey")
def hotkey(req: HotkeyRequest):
    try:
        pyautogui.hotkey(*req.keys)
        return {"status": f"Pressed {req.keys}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/open")
def open_app(req: AppRequest):
    try:
        launch_application(req.app_name)
        return {"status": f"Opened {req.app_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/focus")
def focus_window(req: AppRequest):
    try:
        success = focus_app(req.app_name)
        return {"status": "Focused" if success else "Failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
