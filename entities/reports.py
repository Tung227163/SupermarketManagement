# entities/reports.py
from datetime import datetime
from entities.base import BaseEntity

class BusinessReport(BaseEntity):
    def __init__(self, id: int, report_date: datetime, total_revenue: float, total_invoices: int):
        super().__init__(id)
        self.report_date = report_date
        self.total_revenue = total_revenue
        self.total_invoices = total_invoices
        self.point = 0 # Có thể là điểm đánh giá hiệu quả kinh doanh

    def export_pdf(self):
        print(f"Exporting Business Report for {self.report_date} to PDF...")
        # Logic tạo file PDF sẽ được thực hiện ở service hoặc utility

class CustomerReport(BaseEntity):
    def __init__(self, id: int, report_date: datetime, total_customers: int, vip_customers: int):
        super().__init__(id)
        self.report_date = report_date
        self.total_customers = total_customers
        self.vip_customers = vip_customers

    def export_pdf(self):
        print(f"Exporting Customer Report for {self.report_date} to PDF...")