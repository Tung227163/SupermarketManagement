# repositories/base_repository.py
from abc import ABC, abstractmethod
from database import db

class BaseRepository(ABC):
    """
    Lớp trừu tượng cho Repository.
    Sử dụng @property để lấy cursor mới nhất từ db mỗi khi gọi lệnh.
    """
    def __init__(self):
        self.db = db
        # Không lưu self.cursor = db.cursor ở đây nữa để tránh lỗi NoneType

    @property
    def conn(self):
        """Lấy connection hiện tại"""
        if not self.db.connection or not self.db.connection.is_connected():
            print("⚠️ Mất kết nối DB. Đang thử kết nối lại...")
            self.db.connect()
        return self.db.connection

    @property
    def cursor(self):
        """Luôn lấy cursor hợp lệ"""
        if self.db.cursor is None:
            # Nếu cursor chưa có (do kết nối lỗi lúc đầu), thử kết nối lại
            self.db.connect()
        
        if self.db.cursor is None:
             raise Exception("❌ LỖI NGHIÊM TRỌNG: Không thể kết nối đến MySQL. Vui lòng kiểm tra lại password trong database.py và đảm bảo MySQL đã bật (Start).")
             
        return self.db.cursor

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