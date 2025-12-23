"""
Authentication service
Demonstrates: Service layer pattern, object as parameter and return type
"""
from ..dao.user_dao import UserDAO
from ..models.user import User


class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.user_dao = UserDAO()
        self.current_user = None
    
    def login(self, username: str, password: str) -> User:
        """
        Authenticate user
        Demonstrates: method returning object
        """
        self.current_user = self.user_dao.authenticate(username, password)
        return self.current_user
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self) -> User:
        """Get currently logged in user - demonstrates returning object"""
        return self.current_user
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_user is not None
    
    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.current_user is not None and self.current_user.role == 'ADMIN'
