"""
Base entity class - Demonstrates abstract class and OOP concepts
"""
from abc import ABC, abstractmethod
from datetime import datetime


class BaseEntity(ABC):
    """
    Abstract base class for all entities
    Demonstrates: Abstract class, encapsulation, inheritance
    """
    
    def __init__(self, entity_id=None):
        self._id = entity_id
        self._is_active = True
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    # Abstract methods - must be implemented by subclasses (polymorphism)
    @abstractmethod
    def get_display_info(self):
        """Return formatted display information"""
        pass
    
    @abstractmethod
    def get_code(self):
        """Return entity code"""
        pass
    
    # Getters and setters (encapsulation)
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def is_active(self):
        return self._is_active
    
    @is_active.setter
    def is_active(self, value):
        self._is_active = value
    
    @property
    def created_at(self):
        return self._created_at
    
    @created_at.setter
    def created_at(self, value):
        self._created_at = value
    
    @property
    def updated_at(self):
        return self._updated_at
    
    @updated_at.setter
    def updated_at(self, value):
        self._updated_at = value
