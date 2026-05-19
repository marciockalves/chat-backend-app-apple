from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chat.id")
    content: str
