import sys
import os
import json
import base64
import requests

API_URL = "http://127.0.0.1:8001"

def main():
    if len(sys.argv) < 2:
        print("Usage: python wrapper.py <command> [args]")
        sys.exit(1)
        
    command = sys.argv[1]
    
    try:
        if command == "extract_ui":
            res = requests.get(f"{API_URL}/extract_ui")
            print(json.dumps(res.json(), indent=2))
            
        elif command == "screenshot":
            res = requests.get(f"{API_URL}/screenshot")
            data = res.json()
            if "screenshot_base64" in data:
                img_data = base64.b64decode(data["screenshot_base64"])
                save_path = os.path.join(os.path.dirname(__file__), "screenshot.png")
                with open(save_path, "wb") as f:
                    f.write(img_data)
                print(f"Screenshot saved to: {save_path}")
            else:
                print("Failed to get screenshot from bridge.")
                
        elif command == "webcam":
            res = requests.get(f"{API_URL}/webcam")
            data = res.json()
            if "webcam_base64" in data:
                img_data = base64.b64decode(data["webcam_base64"])
                save_path = os.path.join(os.path.dirname(__file__), "webcam.jpg")
                with open(save_path, "wb") as f:
                    f.write(img_data)
                print(f"Webcam photo saved to: {save_path}")
            else:
                print("Failed to get webcam photo from bridge.")
                
        elif command == "listen":
            res = requests.get(f"{API_URL}/listen")
            print(res.json().get("transcription", "[Error getting transcription]"))
            
        elif command == "click":
            x, y = int(sys.argv[2]), int(sys.argv[3])
            res = requests.post(f"{API_URL}/click", json={"x": x, "y": y})
            print(res.json())
            
        elif command == "type":
            text = " ".join(sys.argv[2:])
            res = requests.post(f"{API_URL}/type", json={"text": text})
            print(res.json())
            
        elif command == "hotkey":
            keys = sys.argv[2:]
            res = requests.post(f"{API_URL}/hotkey", json={"keys": keys})
            print(res.json())
            
        elif command == "open":
            app_name = " ".join(sys.argv[2:])
            res = requests.post(f"{API_URL}/open", json={"app_name": app_name})
            print(res.json())
            
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print(f"ERROR: No se pudo conectar al Ojo de Antigravity. Asegúrate de ejecutar 'Arrancar_Ojos_Antigravity.bat' primero.")
        sys.exit(1)
    except Exception as e:
        print(f"Error executing {command}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
