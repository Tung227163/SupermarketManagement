# entities/base.py
from datetime import datetime
from enum import Enum

class BaseEntity:
    """
    Lớp cơ sở cho tất cả các thực thể trong hệ thống.
    Quản lý ID và thời gian tạo/cập nhật.
    """
    def __init__(self, id: int = None):
        self.id = id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

class UserStatus(Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    LOCKED = "Locked"

class BaseUser(BaseEntity):
    """
    Lớp cơ sở cho người dùng hệ thống (Manager, Cashier, WarehouseKeeper).
    """
    def __init__(self, id: int, username: str, password_hash: str, 
                 full_name: str, email: str, phone: str, status: UserStatus = UserStatus.ACTIVE):
        super().__init__(id)
        self.username = username
        self.password_hash = password_hash
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.status = status

    def login(self):
        # Logic đăng nhập thực tế sẽ ở Service, ở đây mô phỏng hành vi
        print(f"User {self.username} logging in...")
        return True

    def logout(self):
        print(f"User {self.username} logged out.")

    def change_password(self, new_pwd: str):
        # Trong thực tế cần hash lại password trước khi lưu
        self.password_hash = new_pwd
        self.updated_at = datetime.now()
        print("Password changed.")