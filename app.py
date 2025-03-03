from flask import Flask, request, send_file
import cv2
import os
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "AI Image to Video Generator is running! Use /generate endpoint."

@app.route('/generate', methods=['POST'])
def generate_video():
    files = request.files.getlist("images")
    image_paths = []
    
    for file in files:
        if file.filename == '':
            return "Empty filename detected.", 400
        img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(img_path)
        image_paths.append(img_path)
    
    if not image_paths:
        return "No images uploaded.", 400
    
    frame = cv2.imread(image_paths[0])
    if frame is None:
        return "Error reading images.", 400
    
    height, width, layers = frame.shape
    video_path = os.path.join(OUTPUT_FOLDER, "ai_video.mp4")
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*"mp4v"), 5, (width, height))
    
    for img_path in image_paths:
        image = cv2.imread(img_path)
        if image is not None:
            video.write(image)
    
    video.release()
    
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
