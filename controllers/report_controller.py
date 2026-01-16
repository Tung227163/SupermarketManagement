from services.report_service import ReportService

# controllers/report_controller.py

class ReportController:
    # 1. Nhận user vào init
    def __init__(self, view, user):
        self.view = view
        self.user = user
        self.report_service = ReportService()

    def load_dashboard_data(self):
        try:
            # Truyền self.user xuống service
            daily_data = self.report_service.get_daily_revenue(self.user) 
            
            if daily_data:
                self.view.update_daily_revenue(daily_data)
            else:
                self.view.update_daily_revenue({'total_orders': 0, 'total_revenue': 0})

            top_products = self.report_service.get_top_selling_products(self.user, limit=5)
            self.view.update_top_products(top_products)
            
        except PermissionError as pe:
            # Đây là dòng sẽ in ra nếu Hacker cố tình gọi hàm này mà không phải Manager
            print(f"❌ {pe}") 
        except Exception as e:
            print(f"Lỗi báo cáo: {e}")