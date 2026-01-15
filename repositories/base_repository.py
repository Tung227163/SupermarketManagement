# repositories/base_repository.py
from abc import ABC, abstractmethod
from database import db

class BaseRepository(ABC):
    """
    Lớp trừu tượng cho Repository.
    Cung cấp đối tượng db.cursor để thực thi SQL.
    """
    def __init__(self):
        self.db = db
        self.conn = db.connection
        self.cursor = db.cursor

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def delete(self, id):
        pass