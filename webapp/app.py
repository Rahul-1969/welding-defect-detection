from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
from detect import predict

app = Flask(__name__)

# Absolute path anchored to this file so it works regardless of CWD.
# In Docker: /app/webapp/app.py → BASE_DIR = /app → UPLOAD_FOLDER = /app/uploads
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# Serve result images stored in UPLOAD_FOLDER
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/detect", methods=["POST"])
def detect():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded", "success": False}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected", "success": False}), 400

        filename = secure_filename(file.filename)
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(upload_path)
        print(f"[WeldAI] Uploaded: {upload_path}")

        start_time = time.time()
        result, output_path, details = predict(upload_path)
        processing_time = round(time.time() - start_time, 3)

        print(f"[WeldAI] Output:   {output_path}")
        print(f"[WeldAI] Exists:   {os.path.exists(output_path)}")

        if not os.path.exists(output_path):
            return jsonify({
                "error": "Result image was not written to disk.",
                "success": False
            }), 500

        result_filename = os.path.basename(output_path)
        has_defect = details["detected_count"] > 0 or "Defect" in result

        return jsonify({
            "success": True,
            "result": result,
            "image": "/uploads/" + result_filename,
            "status": "DEFECT DETECTED" if has_defect else "GOOD WELD",
            "detections_count": details["detected_count"],
            "confidence": details["max_score"],
            "processing_time": processing_time,
            "details": details
        })

    except Exception as e:
        print(f"[WeldAI] ERROR: {e}")
        return jsonify({
            "error": "Inspection failed. Please upload a valid welding image.",
            "success": False
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)