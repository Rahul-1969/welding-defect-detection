from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import time
from detect import predict

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# Route to serve uploaded images
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


from werkzeug.utils import secure_filename

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded", "success": False}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected", "success": False}), 400

        start_time = time.time()
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)

        result, output_path, details = predict(path)
        processing_time = round(time.time() - start_time, 3)

        filename = os.path.basename(output_path)
        has_defect = details["detected_count"] > 0 or "Defect" in result

        return jsonify({
            "success": True,
            "result": result,
            "image": "/uploads/" + filename,
            "status": "DEFECT DETECTED" if has_defect else "GOOD WELD",
            "detections_count": details["detected_count"],
            "confidence": details["max_score"],
            "processing_time": processing_time,
            "details": details
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)