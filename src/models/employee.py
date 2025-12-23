"""
Employee model
Demonstrates: Inheritance, encapsulation
"""
from .base_entity import BaseEntity
from datetime import datetime


class Employee(BaseEntity):
    """Employee entity"""
    
    def __init__(self, employee_id=None, employee_code=None, full_name=None,
                 phone=None, email=None, position=None, salary=0.0, hire_date=None):
        super().__init__(employee_id)
        self._employee_code = employee_code
        self._full_name = full_name
        self._phone = phone
        self._email = email
        self._position = position
        self._salary = salary
        self._hire_date = hire_date
    
    def get_display_info(self):
        """Implementation of abstract method"""
        return (f"Code: {self._employee_code} | Name: {self._full_name} | "
                f"Position: {self._position} | Phone: {self._phone} | "
                f"Salary: {self._salary:,.0f}")
    
    def get_code(self):
        """Implementation of abstract method"""
        return self._employee_code
    
    # Getters and setters
    @property
    def employee_code(self):
        return self._employee_code
    
    @employee_code.setter
    def employee_code(self, value):
        self._employee_code = value
    
    @property
    def full_name(self):
        return self._full_name
    
    @full_name.setter
    def full_name(self, value):
        self._full_name = value
    
    @property
    def phone(self):
        return self._phone
    
    @phone.setter
    def phone(self, value):
        self._phone = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value
    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value
    
    @property
    def salary(self):
        return self._salary
    
    @salary.setter
    def salary(self, value):
        self._salary = value
    
    @property
    def hire_date(self):
        return self._hire_date
    
    @hire_date.setter
    def hire_date(self, value):
        self._hire_date = value
