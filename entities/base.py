from datetime import datetime
from enum import Enum

class BaseEntity:
    def __init__(self, id: int = None):
        self.id = id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class UserStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    LOCKED = "Locked"

class BaseUser(BaseEntity):
    def __init__(self, id: int, username: str, password_hash: str, 
                 full_name: str, email: str, phone: str, status: UserStatus = UserStatus.ACTIVE):
        super().__init__(id)
        self.username = username
        self.password_hash = password_hash
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.status = status
        self.role = "User" # Giá trị mặc định

    def login(self):
        return True
    
    def logout(self):
        pass