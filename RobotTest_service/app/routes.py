import os
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app import db
from app.models import RobotTest
from app.services.runner import run_robot_test

robot_bp = Blueprint("robot", __name__)

UPLOAD_FOLDER = "robot_tests"
ALLOWED_EXTENSIONS = {"robot"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@robot_bp.route("/run", methods=["POST"])
def run_robot():
    data = request.get_json()

    new_test = RobotTest(
        user_id=data.get("user_id", 1),  # TODO: replace with JWT later
        name=data["name"],
        file_path=data["file_path"]  # must be relative like "robot_tests/login.robot"
    )
    db.session.add(new_test)
    db.session.commit()

    run_robot_test(new_test)
    return jsonify(new_test.to_dict()), 201


@robot_bp.route("/results", methods=["GET"])
def get_results():
    results = RobotTest.query.all()
    return jsonify([r.to_dict() for r in results])


@robot_bp.route("/upload", methods=["POST"])
def upload_test():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        return jsonify({"message": f"{filename} uploaded successfully",
                        "path": save_path}), 201

    return jsonify({"error": "Invalid file type, only .robot allowed"}), 400


@robot_bp.route("/tests", methods=["GET"])
def list_tests():
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".robot")]
    return jsonify(files)


@robot_bp.route("/tests/<name>", methods=["DELETE"])
def delete_test(name):
    file_path = os.path.join(UPLOAD_FOLDER, name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": f"{name} deleted"}), 200
    return jsonify({"error": "File not found"}), 404


@robot_bp.route("/tests/<name>", methods=["GET"])
def download_test(name):
    file_path = os.path.join(UPLOAD_FOLDER, name)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404
