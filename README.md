# 🛒 HỆ THỐNG QUẢN LÝ SIÊU THỊ (SUPERMARKET MANAGEMENT SYSTEM)

> **Đồ án cuối kỳ môn Lập trình Hướng đối tượng (OOP)**  
> **Ngôn ngữ:** Python 3 + MySQL  
> **Kiến trúc:** Layered Architecture (Entities - Repositories - Services - Controllers)

---

## 📖 Giới thiệu
<<<<<<< HEAD
Dự án là một hệ thống hoàn chỉnh mô phỏng quy trình vận hành của một siêu thị hiện đại. Hệ thống được thiết kế theo mô hình phân lớp chuẩn công nghiệp, tách biệt rõ ràng giữa dữ liệu, logic nghiệp vụ và giao diện điều khiển.
=======
Dự án là một hệ thống backend hoàn chỉnh mô phỏng quy trình vận hành của một siêu thị hiện đại. Hệ thống được thiết kế theo mô hình phân lớp chuẩn công nghiệp, tách biệt rõ ràng giữa dữ liệu, logic nghiệp vụ và giao diện điều khiển.
>>>>>>> 52d8cfccbbde2cb9bf3ebe64c05bd4f84e978eaf

Dự án tập trung giải quyết các bài toán nghiệp vụ phức tạp như:
*   **Quản lý hạn sử dụng (FEFO):** Hàng hết hạn trước xuất trước.
*   **Bảo mật phân quyền (RBAC):** Chặt chẽ từ giao diện xuống tận lớp xử lý dữ liệu.
*   **Quản lý khách hàng:** Tích điểm và đổi điểm thưởng.

Hiện tại, hệ thống sử dụng giao diện dòng lệnh giả lập (CLI/Mock UI) để demo toàn bộ chức năng, sẵn sàng để tích hợp với giao diện đồ họa (PyQt6) trong tương lai.

---

## 🚀 Tính năng nổi bật

### 1. Quản lý Bán hàng (Sales) - Dành cho Thu ngân
- **Xử lý FEFO (First Expired, First Out):** Khi bán hàng, hệ thống tự động trừ kho vào các Lô hàng có hạn sử dụng gần nhất.
- **Tích điểm & Tiêu điểm:** 
  - Tự động tích điểm theo giá trị đơn hàng.
  - Cho phép khách hàng dùng điểm để trừ tiền trực tiếp.
- **In hóa đơn:** Hiển thị hóa đơn chi tiết ra màn hình sau khi thanh toán.
- **Tra cứu linh hoạt:** Hỗ trợ tìm sản phẩm bằng Mã vạch (Product Code) thay vì ID nội bộ.

### 2. Quản lý Kho (Inventory) - Dành cho Thủ kho
- **Quản lý đa Lô hàng (Batch Management):** Một mã sản phẩm có thể có nhiều lô nhập với hạn sử dụng khác nhau.
- **Nhập kho chi tiết:** Yêu cầu nhập Hạn sử dụng (Expiry Date) cho từng lần nhập.
- **Tra cứu hạn sử dụng:** Xem chi tiết từng lô hàng của một sản phẩm để biết lô nào sắp hết hạn.
- **Cảnh báo tồn kho:** Lọc ra các sản phẩm sắp hết hàng.

### 3. Bảo mật & Phân quyền (Security) - Dành cho Quản lý
- **Zero Trust Architecture:** Lớp Service tự kiểm tra quyền của người gọi (User Context). Hacker không thể vượt quyền bằng cách gọi API trực tiếp mà không thông qua giao diện.
- **3 Vai trò (Roles):**
  - **Manager:** Quản trị toàn bộ, xem báo cáo, quản lý nhân sự.
  - **Cashier:** Chỉ được bán hàng.
  - **WarehouseKeeper:** Chỉ được nhập/xuất kho.

---

## 🛠 Cài đặt & Hướng dẫn chạy

### Yêu cầu hệ thống
- Python 3.8 trở lên.
- MySQL Server (XAMPP hoặc MySQL Installer).

### Bước 1: Cài đặt thư viện
Chạy lệnh sau tại terminal:
```bash
pip install -r requirements.txt
```

### Bước 2: Cấu hình Database
1. Mở file `database.py`.
2. Tìm class `DatabaseConfig` và cập nhật mật khẩu MySQL của bạn:
   ```python
   PASSWORD = 'your_mysql_password' 
   ```

### Bước 3: Khởi tạo dữ liệu mẫu
1. Mở phần mềm quản lý MySQL (như MySQL Workbench).
<<<<<<< HEAD
2. Mở file `seed_data.sql` (nằm trong thư mục gốc).
=======
2. Mở file `seed_data_v2.sql` (nằm trong thư mục gốc).
>>>>>>> 52d8cfccbbde2cb9bf3ebe64c05bd4f84e978eaf
3. Chạy toàn bộ script (Execute) để tạo database, bảng và dữ liệu mẫu (Sản phẩm, Khách hàng, Lô hàng...).

### Bước 4: Chạy chương trình
```bash
python main.py
```

---

## 🔐 Tài khoản Demo (Có sẵn sau khi chạy Seed Data)

| Vai trò | Username | Password | Chức năng được phép |
| :--- | :--- | :--- | :--- |
| **Quản lý (Admin)** | `admin` | `123456` | Toàn quyền (Báo cáo, Nhân sự, Bán hàng, Kho) |
| **Thu ngân** | `tn1` | `123456` | Bán hàng, Tích điểm, Tìm khách hàng |
| **Thủ kho** | `kho1` | `123456` | Nhập kho, Kiểm tra hạn sử dụng, Xem tồn kho |
<<<<<<< HEAD

---

## 📂 Cấu trúc dự án

```text
supermarket_management/
│
├── main.py                   # [ENTRY POINT] File chạy chính (Menu Console & Điều hướng)
├── database.py               # [CONFIG] Cấu hình kết nối MySQL & Tự động tạo bảng
├── ui_mocks.py               # [VIEW LAYER] Giả lập giao diện (Interface chuẩn cho UI thật)
├── seed_data_v2.sql          # [DATA] Script SQL tạo dữ liệu mẫu, Stored Procedures & FEFO Setup
├── requirements.txt          # [DEPENDENCIES] Danh sách các thư viện Python cần cài đặt
├── setup_guide.txt           # [DOCS] Hướng dẫn cài đặt nhanh cho giáo viên
├── README.md                 # [DOCS] Tài liệu mô tả dự án đầy đủ
│
├── entities/                 # [ENTITY LAYER] Các class thực thể (OOP Model)
│   ├── __init__.py
│   ├── base.py               # Lớp cha BaseEntity, Enum trạng thái
│   ├── users.py              # Các role: Manager, Cashier, WarehouseKeeper
│   ├── products.py           # Product, ProductBatch (Lô hàng), StockEntry (Phiếu nhập)
│   ├── orders.py             # Invoice, InvoiceItem, Customer
│   └── reports.py            # Các class hỗ trợ báo cáo
│
├── repositories/             # [REPOSITORY LAYER] Tương tác trực tiếp với MySQL (DAO)
│   ├── __init__.py
│   ├── base_repository.py    # Abstract Class quản lý kết nối DB chung
│   ├── user_repository.py    # CRUD User, Map dữ liệu nhân viên
│   ├── product_repository.py # CRUD Product, Xử lý nhập/xuất Lô hàng (Batch)
│   ├── customer_repository.py# CRUD Customer, Tìm kiếm khách hàng
│   └── order_repository.py   # Xử lý Transaction hóa đơn (Invoice & Items)
│
├── services/                 # [SERVICE LAYER] Xử lý logic nghiệp vụ cốt lõi
│   ├── __init__.py
│   ├── auth_service.py       # Xác thực đăng nhập, Mã hóa mật khẩu (SHA256)
│   ├── user_service.py       # Nghiệp vụ quản lý nhân sự (Check quyền Admin)
│   ├── inventory_service.py  # Nghiệp vụ kho: Nhập kho theo lô, Check hạn sử dụng
│   ├── sales_service.py      # Nghiệp vụ bán hàng: Logic FEFO, Tích điểm, Hoàn trả
│   ├── customer_service.py   # Tra cứu lịch sử mua hàng, Quản lý thông tin khách
│   └── report_service.py     # Tổng hợp doanh thu, Thống kê Top bán chạy
│
└── controllers/              # [CONTROLLER LAYER] Điều phối luồng dữ liệu (View <-> Service)
    ├── __init__.py
    ├── auth_controller.py    # Điều khiển luồng đăng nhập
    ├── user_controller.py    # Điều khiển giao diện quản lý nhân sự
    ├── inventory_controller.py # Điều khiển giao diện kho (Nhập/Xem)
    ├── sales_controller.py   # Điều khiển giao diện bán hàng (Scan/Thanh toán)
    └── report_controller.py  # Điều khiển giao diện báo cáo

=======

---

## 📂 Cấu trúc dự án

```text
supermarket_management/
│
├── main.py                   # Entry point (Menu chính & Điều hướng)
├── database.py               # Cấu hình kết nối MySQL & Tự động tạo bảng
├── seed_data.sql          # Script SQL tạo dữ liệu mẫu & Stored Procedures
├── ui_mocks.py               # Giả lập giao diện (Interface chuẩn cho UI thật)
├── requirements.txt          # Danh sách thư viện
│
├── entities/                 # [DATA LAYER] Các class thực thể (OOP)
│   ├── base.py               # BaseEntity
│   ├── users.py              # Manager, Cashier, WarehouseKeeper
│   ├── products.py           # Product, ProductBatch, StockEntry
│   └── orders.py             # Invoice, InvoiceItem, Customer
│
├── repositories/             # [DAO LAYER] Tương tác trực tiếp SQL
│   ├── base_repository.py    # Abstract Class
│   ├── user_repository.py
│   ├── product_repository.py # Xử lý Product & Batch
│   └── ...
│
├── services/                 # [LOGIC LAYER] Xử lý nghiệp vụ phức tạp
│   ├── sales_service.py      # Logic FEFO, Tích điểm, Hoàn trả
│   ├── inventory_service.py  # Logic Nhập kho theo Lô
│   ├── auth_service.py       # Logic Đăng nhập, Hash pass
│   └── ...
│
└── controllers/              # [CONTROL LAYER] Điều phối luồng dữ liệu
    ├── auth_controller.py
    ├── sales_controller.py
    ├── inventory_controller.py
    └── ...
>>>>>>> 52d8cfccbbde2cb9bf3ebe64c05bd4f84e978eaf
```

---

<<<<<<< HEAD
=======
## 🧪 Kiểm thử (Testing)
Dự án đi kèm bộ test tích hợp (Integration Test) để đảm bảo logic chạy đúng.

**Cách chạy:**
```bash
python test_backend_full.py
```

**Kịch bản test tự động bao gồm:**
1.  **Quản trị:** Tạo nhân viên mới -> Đăng nhập bằng nhân viên đó.
2.  **Kho vận:** Nhập 2 lô hàng (1 lô cũ, 1 lô mới).
3.  **Khách hàng:** Tạo khách hàng mới.
4.  **Bán hàng:** Thực hiện giao dịch mua hàng -> Hệ thống tự động trừ kho vào lô cũ (FEFO) -> Kiểm tra tồn kho sau khi trừ.
5.  **Báo cáo:** Kiểm tra doanh thu được cập nhật.

---

>>>>>>> 52d8cfccbbde2cb9bf3ebe64c05bd4f84e978eaf
## 📝 Thông tin tác giả
-   **Nhóm:** 209
-   **Sinh viên:**
      -   Phạm Xuân Vỹ - 20237496
      -   Nguyễn Quang Tùng - 20227163
-   **Lớp:** 163629
-   **Môn học:** Lập trình hướng đối tượng - MI4090
