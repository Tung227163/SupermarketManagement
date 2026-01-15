# entities/users.py
from entities.base import BaseUser, UserStatus

class Manager(BaseUser):
    def assign_role(self, user: BaseUser, role: str):
        print(f"Manager {self.username} assigned role {role} to {user.username}")

    def view_reports(self):
        print(f"Manager {self.username} is viewing reports.")

class Cashier(BaseUser):
    def sell_product(self):
        print(f"Cashier {self.username} is processing a sale.")

    def create_invoice(self):
        print("Creating invoice...")

class WarehouseKeeper(BaseUser):
    def receive_goods(self):
        print(f"WarehouseKeeper {self.username} is receiving goods.")

    def issue_goods(self):
        print(f"WarehouseKeeper {self.username} is issuing goods.")

    def check_inventory(self):
        print("Checking inventory...")