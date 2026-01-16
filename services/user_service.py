import hashlib
from repositories.user_repository import UserRepository
from entities.users import Manager, Cashier, WarehouseKeeper
from entities.base import UserStatus

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    # Thêm tham số admin_user vào tất cả các hàm quan trọng
    def create_user(self, admin_user, username, password, full_name, email, phone, role):
        
        # --- BẢO MẬT ---
        if admin_user.role != 'Manager':
            raise PermissionError("⛔ BẢO MẬT: Chỉ Manager mới được tạo nhân viên.")
        
        """Tạo nhân viên mới"""
        # 1. Kiểm tra trùng username
        if self.user_repo.find_by_username(username):
            print(f"❌ Username '{username}' đã tồn tại.")
            return None

        # 2. Hash mật khẩu
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()

        # 3. Khởi tạo đối tượng theo Role
        # ID để None để DB tự sinh
        if role == 'Manager':
            user = Manager(None, username, pwd_hash, full_name, email, phone)
        elif role == 'Cashier':
            user = Cashier(None, username, pwd_hash, full_name, email, phone)
        elif role == 'WarehouseKeeper':
            user = WarehouseKeeper(None, username, pwd_hash, full_name, email, phone)
        else:
            print("❌ Role không hợp lệ.")
            return None

        saved_user = self.user_repo.save(user)
        print(f"✅ Đã tạo nhân viên: {username} - {role}")
        return saved_user

    def update_user_info(self, admin_user, user_id, full_name, email, phone):
        # --- BẢO MẬT ---
        if admin_user.role != 'Manager':
            raise PermissionError("⛔ BẢO MẬT: Chỉ Manager mới được cập nhật thông tin nhân viên.")
        """Cập nhật thông tin cơ bản"""
        user = self.user_repo.find_by_id(user_id)
        if user:
            user.full_name = full_name
            user.email = email
            user.phone = phone
            self.user_repo.save(user)
            print("✅ Cập nhật thông tin thành công.")
        else:
            print("❌ Không tìm thấy User.")

    def set_user_status(self, admin_user, user_id, status: UserStatus):
        # --- BẢO MẬT ---
        if admin_user.role != 'Manager':
            raise PermissionError("⛔ BẢO MẬT: Chỉ Manager mới được khóa/mở tài khoản.")
        """Khóa hoặc Mở khóa tài khoản"""
        user = self.user_repo.find_by_id(user_id)
        if user:
            user.status = status
            self.user_repo.save(user)
            print(f"✅ Đã chuyển trạng thái user thành: {status.value}")
        else:
            print("❌ Không tìm thấy User.")

    def reset_password(self, admin_user, user_id, new_password):
        # --- BẢO MẬT ---
        if admin_user.role != 'Manager':
            raise PermissionError("⛔ BẢO MẬT: Chỉ Manager mới được cấp lại mật khẩu.")
        """Manager cấp lại mật khẩu cho nhân viên"""
        user = self.user_repo.find_by_id(user_id)
        if user:
            user.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            self.user_repo.save(user)
            print(f"✅ Đã reset mật khẩu cho {user.username}")
        else:
            print("❌ Không tìm thấy User.")
    
    def get_all_users(self, admin_user):
            # Kiểm tra quyền
            if admin_user.role != 'Manager':
                raise PermissionError("⛔ BẢO MẬT: Bạn không có quyền xem danh sách nhân viên.")
            
            return self.user_repo.find_all()