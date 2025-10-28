# backend/api/notifications.py
import logging
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
import smtplib
from email.message import EmailMessage

from services.notifications import NotificationService
from core.schemas import NotificationRequest

logger = logging.getLogger(__name__)
bp = Blueprint("notifications", __name__)

# Initialize notification service
notification_service = NotificationService()

def send_email(to_email: str, subject: str, body: str):
    """Send an email notification."""
    sender = current_app.config.get("SENDER_EMAIL")
    password = current_app.config.get("SENDER_EMAIL_PASSWORD")
    
    if not sender or not password:
        logger.warning("Email credentials not set; skipping send.")
        return False
    
    try:
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(sender, password)
            s.send_message(msg)
        
        logger.info(f"Email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

@bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    """Get notifications for the current user."""
    user_id = get_jwt_identity()
    
    try:
        limit = request.args.get("limit", default=50, type=int)
        unread_only = request.args.get("unread_only", default=False, type=bool)
        
        notifications = notification_service.get_notifications(user_id, limit, unread_only)
        
        return jsonify({
            "status": "success",
            "count": len(notifications),
            "notifications": notifications
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving notifications: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve notifications"
        }), 500

@bp.route("/unread_count", methods=["GET"])
@jwt_required()
def get_unread_count():
    """Get the count of unread notifications for the current user."""
    user_id = get_jwt_identity()
    
    try:
        count = notification_service.get_unread_count(user_id)
        
        return jsonify({
            "status": "success",
            "unread_count": count
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving unread count: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve unread count"
        }), 500

@bp.route("/<notification_id>/read", methods=["PATCH"])
@jwt_required()
def mark_as_read(notification_id):
    """Mark a notification as read."""
    user_id = get_jwt_identity()
    
    try:
        result = notification_service.mark_as_read(notification_id, user_id)
        
        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        logger.error(f"Error marking notification as read: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to mark notification as read"
        }), 500

@bp.route("/read_all", methods=["PATCH"])
@jwt_required()
def mark_all_as_read():
    """Mark all notifications as read for the current user."""
    user_id = get_jwt_identity()
    
    try:
        result = notification_service.mark_all_as_read(user_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error marking all notifications as read: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to mark all notifications as read"
        }), 500

@bp.route("/<notification_id>", methods=["DELETE"])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification."""
    user_id = get_jwt_identity()
    
    try:
        result = notification_service.delete_notification(notification_id, user_id)
        
        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to delete notification"
        }), 500

@bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_all_notifications():
    """Delete all notifications for the current user."""
    user_id = get_jwt_identity()
    
    try:
        result = notification_service.delete_all_notifications(user_id)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error deleting all notifications: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to delete all notifications"
        }), 500

@bp.route("/send_test", methods=["POST"])
@jwt_required()
def send_test():
    """Send a test email notification."""
    user_id = get_jwt_identity()
    
    try:
        data = request.get_json() or {}
        to_email = data.get("email")
        
        if not to_email:
            return jsonify({
                "status": "error",
                "message": "Email address is required"
            }), 400
        
        ok = send_email(to_email, "PriceHawk Test Notification", 
                       "This is a test notification from PriceHawk. Your price tracking system is working correctly!")
        
        # Create a notification record
        notification_service.create_notification({
            "user_id": user_id,
            "type": "test",
            "message": "Test notification sent to your email"
        })
        
        return jsonify({
            "status": "success",
            "sent": ok,
            "message": "Test notification sent"
        }), 200
    except Exception as e:
        logger.error(f"Error sending test notification: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Failed to send test notification"
        }), 500
