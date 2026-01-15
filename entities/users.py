from entities.base import BaseUser, UserStatus

class Manager(BaseUser):
    def __init__(self, id, username, password_hash, full_name, email, phone, status=UserStatus.ACTIVE):
        super().__init__(id, username, password_hash, full_name, email, phone, status)
        self.role = "Manager"

    def assign_role(self, user, role):
        print(f"Manager assigned {role}")

class Cashier(BaseUser):
    def __init__(self, id, username, password_hash, full_name, email, phone, status=UserStatus.ACTIVE):
        super().__init__(id, username, password_hash, full_name, email, phone, status)
        self.role = "Cashier"

class WarehouseKeeper(BaseUser):
    def __init__(self, id, username, password_hash, full_name, email, phone, status=UserStatus.ACTIVE):
        super().__init__(id, username, password_hash, full_name, email, phone, status)
        self.role = "WarehouseKeeper"