from database import db

class ReportService:
    def __init__(self):
        self.cursor = db.cursor

    def get_revenue_report(self):
        """Báo cáo doanh thu tổng"""
        query = "SELECT SUM(total_amount) as total_rev, COUNT(*) as total_inv FROM invoices"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result # {'total_rev': ..., 'total_inv': ...}

    def get_top_products(self, limit=5):
        """Lấy top sản phẩm bán chạy"""
        query = """
            SELECT p.name, SUM(ii.quantity) as total_sold
            FROM invoice_items ii
            JOIN products p ON ii.product_id = p.id
            GROUP BY p.name
            ORDER BY total_sold DESC
            LIMIT %s
        """
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()