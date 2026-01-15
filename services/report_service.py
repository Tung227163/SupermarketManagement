from database import db
from datetime import datetime

class ReportService:
    def __init__(self):
        self.cursor = db.cursor

    def get_daily_revenue(self, date_str=None):
        """Doanh thu trong ngày (Mặc định là hôm nay)"""
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
            
        query = """
            SELECT COUNT(*) as total_orders, SUM(total_amount) as total_revenue
            FROM invoices
            WHERE DATE(invoice_date) = %s
        """
        self.cursor.execute(query, (date_str,))
        return self.cursor.fetchone()

    def get_monthly_revenue(self, month, year):
        query = """
            SELECT DATE(invoice_date) as sale_date, SUM(total_amount) as revenue
            FROM invoices
            WHERE MONTH(invoice_date) = %s AND YEAR(invoice_date) = %s
            GROUP BY DATE(invoice_date)
            ORDER BY sale_date
        """
        self.cursor.execute(query, (month, year))
        return self.cursor.fetchall()

    def get_top_selling_products(self, limit=5):
        """Top sản phẩm bán chạy nhất"""
        query = """
            SELECT p.name, SUM(ii.quantity) as total_sold
            FROM invoice_items ii
            JOIN products p ON ii.product_id = p.id
            GROUP BY p.id, p.name
            ORDER BY total_sold DESC
            LIMIT %s
        """
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()

    def get_inventory_value(self):
        """Tổng giá trị hàng tồn kho (Vốn)"""
        query = "SELECT SUM(price * stock_qty) as total_value FROM products"
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        return res['total_value'] if res['total_value'] else 0