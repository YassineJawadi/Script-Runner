from flask import Blueprint, request, jsonify
from app import db
from app.models import RobotTest

robot_bp = Blueprint("robot", __name__)

# 🟢 Create a new test (mock for now)
@robot_bp.route("/run", methods=["POST"])
def run_robot_test():
    data = request.get_json()

    new_test = RobotTest(
        user_id=data.get("user_id", 1),  # later: from JWT
        name=data["name"],
        file_path=data["file_path"],
        status="pending"
    )
    db.session.add(new_test)
    db.session.commit()

    return jsonify(new_test.to_dict()), 201


# 🟢 Get all tests
@robot_bp.route("/results", methods=["GET"])
def get_results():
    results = RobotTest.query.all()
    return jsonify([r.to_dict() for r in results])
