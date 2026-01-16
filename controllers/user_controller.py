from services.user_service import UserService
from entities.base import UserStatus

# controllers/user_controller.py

class UserController:
    # 1. Nhận user vào init
    def __init__(self, view, user):
        self.view = view
        self.user = user # Manager đang đăng nhập
        self.user_service = UserService()

    def load_user_list(self):
        try:
            # Truyền self.user xuống service
            users = self.user_service.get_all_users(self.user)
            self.view.update_user_table(users)
        except PermissionError as pe:
            self.view.show_error(str(pe))
        except Exception as e:
            self.view.show_error(f"Lỗi: {e}")

    def handle_create_user(self):
        data = self.view.get_create_inputs()
        if not data['username'] or not data['password']:
            self.view.show_error("Username/Pass trống.")
            return

        try:
            # Truyền self.user xuống service
            new_user = self.user_service.create_user(
                admin_user=self.user, # <--- QUAN TRỌNG
                username=data['username'],
                password=data['password'],
                full_name=data['fullname'],
                email="",
                phone="",
                role=data['role']
            )
            
            if new_user:
                self.view.show_success(f"Đã tạo: {new_user.username}")
                self.load_user_list()
        except PermissionError as pe:
            self.view.show_error(str(pe))
        except Exception as e:
            self.view.show_error(f"Lỗi: {e}")

    def handle_update_role(self):
        """Cập nhật quyền (Role) hoặc Trạng thái"""
        # Lưu ý: UserService cần hỗ trợ hàm update role riêng hoặc ta dùng hàm update chung
        # Ở bài trước UserService chưa có hàm update_role cụ thể, 
        # nhưng ta có thể giả định hoặc dùng trực tiếp Repo nếu cần gấp.
        # Tốt nhất là thêm hàm update_role vào UserService. 
        # Ở đây tôi demo logic:
        
        data = self.view.get_role_update_inputs()
        user_id = data['user_id']
        
        if not user_id:
            self.view.show_error("Chưa chọn nhân viên cần sửa.")
            return

        print(f"🔄 [CONTROLLER]: Đang yêu cầu cập nhật User ID {user_id} thành Role {data['new_role']}...")
        # Code thực tế sẽ gọi: self.user_service.update_user_role(user_id, data['new_role'])
        self.view.show_success("Chức năng cập nhật quyền đang được xử lý (Demo).")