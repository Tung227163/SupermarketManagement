"""
Generic DAO interface
Demonstrates: Abstract class, polymorphism
"""
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

T = TypeVar('T')


class GenericDAO(ABC, Generic[T]):
    """Generic DAO interface for CRUD operations"""
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity"""
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: int) -> T:
        """Find entity by ID"""
        pass
    
    @abstractmethod
    def find_by_code(self, code: str) -> T:
        """Find entity by code"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """Find all entities"""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> List[T]:
        """Find entities by name"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> bool:
        """Update an entity"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity (soft delete)"""
        pass
    
    @abstractmethod
    def delete_all(self) -> bool:
        """Delete all entities (soft delete)"""
        pass
