from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from detect import predict

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# Route to serve uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/detect", methods=["POST"])
def detect():

    file = request.files["file"]

    path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(path)

    result, output_path = predict(path)

    filename = os.path.basename(output_path)

    return jsonify({
        "result": result,
        "image": "/uploads/" + filename
    })


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)