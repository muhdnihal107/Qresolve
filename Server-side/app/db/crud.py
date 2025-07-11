from bson import ObjectId
from datetime import datetime
from app.db.connection import db
from app.models.ticket import TicketCreate, TicketUpdate
from typing import Optional
import random

def get_user_by_email(email: str) -> Optional[dict]:
    return db.users.find_one({"email": email})

def get_user_by_id(user_id: str) -> Optional[dict]:
    return db.users.find_one({"_id": ObjectId(user_id)})

def create_user(user_dict: dict):
    return db.users.insert_one(user_dict)

def update_user_verified(user_id: str):
    db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_verified": True}}
    )

def create_ticket(ticket: dict):
    ticket["created_at"] = datetime.utcnow()
    ticket["status"] = "open"
    return db.tickets.insert_one(ticket)

def get_ticket_by_id(ticket_id: str):
    return db.tickets.find_one({"_id": ObjectId(ticket_id)})

def get_all_tickets():
    return list(db.tickets.find())

def get_tickets_by_user(user_id: str):
    return list(db.tickets.find({"user_id": user_id}))

def get_tickets_by_agent(agent_id: str):
    return list(db.tickets.find({"agent_id": agent_id}))

def update_ticket(ticket_id: str, updates: TicketUpdate):
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    result = db.tickets.update_one({"_id": ObjectId(ticket_id)}, {"$set": update_data})
    return result.modified_count

def delete_ticket(ticket_id: str):
    return db.tickets.delete_one({"_id": ObjectId(ticket_id)})

def submit_feedback(ticket_id: str, rating: int, comment: str = None):
    feedback_doc = {
        "ticket_id": ObjectId(ticket_id),
        "rating": rating,
        "comment": comment,
        "created_at": datetime.utcnow()
    }
    return db.feedback.insert_one(feedback_doc)

def get_feedback_by_ticket(ticket_id: str):
    return db.feedback.find_one({"ticket_id": ObjectId(ticket_id)})

def get_random_available_agent(department: str):
    agents = list(db.users.find({
        "role": "agent",
        "is_verified": True,
        "is_available": True,
        "department": department
    }))
    return random.choice(agents) if agents else None