"""
User model for authentication
Demonstrates: Inheritance, Constructor overloading
"""
from .base_entity import BaseEntity


class User(BaseEntity):
    """User entity - inherits from BaseEntity"""
    
    def __init__(self, user_id=None, username=None, password=None, full_name=None, role=None):
        """Constructor with parameters (demonstrates constructor)"""
        super().__init__(user_id)
        self._username = username
        self._password = password
        self._full_name = full_name
        self._role = role
    
    def get_display_info(self):
        """Implementation of abstract method (polymorphism)"""
        return f"ID: {self._id} | Username: {self._username} | Full Name: {self._full_name} | Role: {self._role}"
    
    def get_code(self):
        """Implementation of abstract method"""
        return self._username
    
    # Getters and setters
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        self._username = value
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = value
    
    @property
    def full_name(self):
        return self._full_name
    
    @full_name.setter
    def full_name(self, value):
        self._full_name = value
    
    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, value):
        self._role = value
