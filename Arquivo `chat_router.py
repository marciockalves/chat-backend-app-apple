from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.services import chat_service
from src.config import database

router = APIRouter(prefix="/chats")

@router.post("/create", response_model=Chat)
def create_chat(user_id: int):
    return chat_service.create_chat(user_id)

@router.get("/messages/{chat_id}", response_model=List[Message])
def get_messages(chat_id: int):
    return chat_service.get_messages(chat_id)
