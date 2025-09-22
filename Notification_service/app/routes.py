from flask import Blueprint, request, jsonify
from .models import db, Notification
from .services.email_sender import send_email
from datetime import datetime

notification_bp = Blueprint("notifications", __name__)

@notification_bp.route("/", methods=["POST"])
def create_notification():
    data = request.get_json()

    user_id = data.get("user_id")
    email = data.get("email")
    message = data.get("message")
    notif_type = data.get("type", "email")

    notification = Notification(
        user_id=user_id,
        message=message,
        type=notif_type,
        sent_at=datetime.utcnow()
    )

    db.session.add(notification)
    db.session.commit()

    # ✅ Envoi réel vers l’email du JSON
    if notif_type == "email" and email:
        send_email(email, "Notification", message)

    return jsonify(notification.to_dict()), 201

@notification_bp.route("/", methods=["GET"])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([n.to_dict() for n in notifications]), 200


@notification_bp.route("/<int:notif_id>", methods=["GET"])
def get_notification(notif_id):
    notification = Notification.query.get_or_404(notif_id)
    return jsonify(notification.to_dict()), 200


@notification_bp.route("/<int:notif_id>", methods=["DELETE"])
def delete_notification(notif_id):
    notification = Notification.query.get_or_404(notif_id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted"}), 200
