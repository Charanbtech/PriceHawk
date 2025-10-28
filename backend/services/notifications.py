"""
Notification service for PriceHawk.
Handles creating, retrieving, and managing user notifications.
"""
import logging
from datetime import datetime
from typing import Dict, List, Optional

from core.db import get_db

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for managing user notifications."""
    
    def __init__(self):
        self.db = get_db()
    
    def create_notification(self, notification_data: Dict) -> Dict:
        """
        Create a new notification.
        
        Args:
            notification_data: Dict containing notification details
            
        Returns:
            Dict: The created notification
        """
        required_fields = {"user_id", "type", "message"}
        
        # Validate required fields
        if not all(field in notification_data for field in required_fields):
            missing = required_fields - set(notification_data.keys())
            logger.error(f"Missing required fields for notification: {missing}")
            return {"status": "error", "message": f"Missing required fields: {missing}"}
        
        notification = {
            "user_id": notification_data["user_id"],
            "type": notification_data["type"],
            "message": notification_data["message"],
            "product_id": notification_data.get("product_id"),
            "read": False,
            "created_at": datetime.utcnow(),
            # Optional fields
            "old_price": notification_data.get("old_price"),
            "new_price": notification_data.get("new_price"),
            "url": notification_data.get("url"),
            "image_url": notification_data.get("image_url"),
            "product_name": notification_data.get("product_name")
        }
        
        # Remove None values
        notification = {k: v for k, v in notification.items() if v is not None}
        
        result = self.db.notifications.insert_one(notification)
        notification["_id"] = result.inserted_id
        
        logger.info(f"Created notification for user {notification_data['user_id']}")
        
        return {
            "status": "success",
            "notification_id": str(result.inserted_id),
            "notification": notification
        }
    
    def get_notifications(self, user_id: str, limit: int = 50, unread_only: bool = False) -> List[Dict]:
        """
        Get notifications for a user.
        
        Args:
            user_id: The ID of the user
            limit: Maximum number of notifications to return
            unread_only: Whether to return only unread notifications
            
        Returns:
            List[Dict]: List of notifications
        """
        query = {"user_id": user_id}
        
        if unread_only:
            query["read"] = False
        
        notifications = list(self.db.notifications.find(
            query,
            sort=[("created_at", -1)],
            limit=limit
        ))
        
        # Convert ObjectId to string for JSON serialization
        for notification in notifications:
            notification["_id"] = str(notification["_id"])
            if "product_id" in notification and notification["product_id"]:
                notification["product_id"] = str(notification["product_id"])
        
        return notifications
    
    def mark_as_read(self, notification_id: str, user_id: str) -> Dict:
        """
        Mark a notification as read.
        
        Args:
            notification_id: The ID of the notification
            user_id: The ID of the user (for security)
            
        Returns:
            Dict: Status of the operation
        """
        from bson.objectid import ObjectId
        
        try:
            obj_id = ObjectId(notification_id)
        except Exception:
            return {"status": "error", "message": "Invalid notification ID"}
            
        result = self.db.notifications.update_one(
            {"_id": obj_id, "user_id": user_id},
            {"$set": {"read": True}}
        )
        
        if result.matched_count > 0:
            return {"status": "success", "message": "Notification marked as read"}
        else:
            return {"status": "error", "message": "Notification not found"}
    
    def mark_all_as_read(self, user_id: str) -> Dict:
        """
        Mark all notifications for a user as read.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Dict: Status of the operation
        """
        result = self.db.notifications.update_many(
            {"user_id": user_id, "read": False},
            {"$set": {"read": True}}
        )
        
        return {
            "status": "success", 
            "message": f"Marked {result.modified_count} notifications as read"
        }
    
    def delete_notification(self, notification_id: str, user_id: str) -> Dict:
        """
        Delete a notification.
        
        Args:
            notification_id: The ID of the notification
            user_id: The ID of the user (for security)
            
        Returns:
            Dict: Status of the operation
        """
        from bson.objectid import ObjectId
        
        try:
            obj_id = ObjectId(notification_id)
        except Exception:
            return {"status": "error", "message": "Invalid notification ID"}
            
        result = self.db.notifications.delete_one(
            {"_id": obj_id, "user_id": user_id}
        )
        
        if result.deleted_count > 0:
            return {"status": "success", "message": "Notification deleted"}
        else:
            return {"status": "error", "message": "Notification not found"}
    
    def delete_all_notifications(self, user_id: str) -> Dict:
        """
        Delete all notifications for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            Dict: Status of the operation
        """
        result = self.db.notifications.delete_many({"user_id": user_id})
        
        return {
            "status": "success", 
            "message": f"Deleted {result.deleted_count} notifications"
        }
    
    def get_unread_count(self, user_id: str) -> int:
        """
        Get the count of unread notifications for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            int: Count of unread notifications
        """
        count = self.db.notifications.count_documents({
            "user_id": user_id,
            "read": False
        })
        
        return count