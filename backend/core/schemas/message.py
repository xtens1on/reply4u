from datetime import datetime

from pydantic import BaseModel


class MessageSchema(BaseModel):
    content: str
    date: datetime
    role: str = 'user'

    @property
    def shortcuts(self):
        return {
            'date': self.date.date(),
            'time': self.date.time(),
            'content': self.content,
            'message': self.content,
        }