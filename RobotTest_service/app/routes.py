from flask import Blueprint, jsonify
from .models import TestResult

robot_bp = Blueprint("robot", __name__)

@robot_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "RobotTest service is alive!"})

@robot_bp.route("/results", methods=["GET"])
def get_results():
    results = TestResult.query.all()
    return jsonify([r.to_dict() for r in results])