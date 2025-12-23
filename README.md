# Hệ Thống Quản Lý Siêu Thị (Supermarket Management System)

## Mô tả

Dự án quản lý siêu thị được xây dựng bằng Python với các tính năng đầy đủ:
- Quản lý sản phẩm
- Quản lý nhân viên
- Hệ thống báo cáo
- Xác thực người dùng
- Lưu trữ dữ liệu với SQLite

## Các Tính Năng Chính

### 1. Hệ Thống Menu
- Menu chính với các nhóm chức năng
- Menu con cho từng nghiệp vụ
- Điều hướng linh hoạt giữa các menu

### 2. Quản Lý Sản Phẩm
- ✓ Thêm mới sản phẩm
- ✓ Duyệt danh sách sản phẩm
- ✓ Tìm kiếm (theo mã, tên, danh mục)
- ✓ Cập nhật thông tin sản phẩm
- ✓ Xóa sản phẩm
- ✓ Xóa tất cả sản phẩm
- ✓ Sắp xếp (theo giá, tên)

### 3. Quản Lý Nhân Viên
- ✓ Thêm mới nhân viên
- ✓ Duyệt danh sách nhân viên
- ✓ Tìm kiếm (theo mã, tên, chức vụ)
- ✓ Cập nhật thông tin nhân viên
- ✓ Xóa nhân viên
- ✓ Xóa tất cả nhân viên
- ✓ Sắp xếp (theo lương)

### 4. Báo Cáo
- Báo cáo tồn kho
- Báo cáo hàng sắp hết
- Báo cáo giá trị tồn kho
- Báo cáo danh sách nhân viên
- Báo cáo nhân viên theo chức vụ
- Báo cáo sản phẩm theo danh mục

### 5. Xác Thực Người Dùng
- Đăng nhập bắt buộc
- Quản lý phiên làm việc
- Đăng xuất

## Các Khái Niệm OOP Được Sử Dụng

### 1. Abstract Class (Lớp Trừu Tượng)
- `BaseEntity`: Lớp cơ sở trừu tượng cho tất cả các entity
- `GenericDAO`: Interface DAO trừu tượng

### 2. Inheritance (Kế Thừa)
- `User`, `Product`, `Employee` kế thừa từ `BaseEntity`
- `UserDAO`, `ProductDAO`, `EmployeeDAO` kế thừa từ `GenericDAO`

### 3. Polymorphism (Đa Hình)
- Abstract methods được implement khác nhau ở mỗi lớp con
- Các phương thức `get_display_info()` và `get_code()` có implementation riêng

### 4. Encapsulation (Đóng Gói)
- Sử dụng properties và private attributes (`_attribute`)
- Getters và setters cho tất cả các thuộc tính

### 5. Constructor
- Tất cả các class đều có `__init__()` constructor
- Constructor với tham số tùy chọn

### 6. Object as Parameter/Return Type
- Các phương thức DAO nhận và trả về objects
- Service layer làm việc với objects

## Cấu Trúc Dự Án

```
df/
├── main.py                      # Entry point
├── sql/
│   └── schema.sql              # Database schema
├── src/
│   ├── models/                 # Domain models
│   │   ├── base_entity.py     # Abstract base class
│   │   ├── user.py
│   │   ├── product.py
│   │   └── employee.py
│   ├── dao/                    # Data Access Objects
│   │   ├── generic_dao.py     # Generic DAO interface
│   │   ├── user_dao.py
│   │   ├── product_dao.py
│   │   └── employee_dao.py
│   ├── services/               # Business logic
│   │   ├── auth_service.py
│   │   └── report_service.py
│   ├── ui/                     # User Interface
│   │   ├── product_ui.py
│   │   ├── employee_ui.py
│   │   └── report_ui.py
│   └── utils/                  # Utilities
│       └── database.py
└── README.md
```

## Yêu Cầu Hệ Thống

- Python 3.6 trở lên
- SQLite3 (đi kèm với Python)

## Cài Đặt và Chạy

### 1. Clone repository

```bash
git clone https://github.com/Tung227163/df.git
cd df
```

### 2. Chạy chương trình

```bash
python main.py
```

### 3. Đăng nhập

Tài khoản mặc định:
- **Username**: `admin`
- **Password**: `admin123`

### 4. Demo OOP Concepts (Tùy chọn)

Để xem demo các khái niệm OOP:
```bash
python demo.py
```

## Sử Dụng

1. **Đăng nhập** với tài khoản admin
2. **Chọn chức năng** từ menu chính:
   - Quản lý sản phẩm (1)
   - Quản lý nhân viên (2)
   - Báo cáo (3)
3. **Thực hiện các tác vụ** trong menu con
4. **Đăng xuất** hoặc thoát khi hoàn tất

## Database

Hệ thống sử dụng SQLite để lưu trữ dữ liệu lâu dài:
- File database: `supermarket.db`
- Tự động tạo khi chạy lần đầu
- Dữ liệu mẫu được thêm tự động

## Dữ Liệu Mẫu

### Sản phẩm mẫu
- Gạo Thơm (P001)
- Dầu ăn (P002)
- Sữa tươi (P003)
- Bánh mì (P004)

### Nhân viên mẫu
- Nguyễn Văn A - Quản lý (E001)
- Trần Thị B - Thu ngân (E002)
- Lê Văn C - Nhân viên kho (E003)

## Tác Giả

Dự án được phát triển cho môn học Lập trình Hướng Đối Tượng

## License

MIT License
