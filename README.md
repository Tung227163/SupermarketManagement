# Java Web Servlet Basic - Ngày 1

## 📋 Tổng quan

Dự án này là một ứng dụng Java Web cơ bản sử dụng Servlet, được thiết kế cho chương trình học **Ngày 1: Tổng quan về Java Web và Servlet cơ bản**.

### 🎯 Mục tiêu học tập

- Tìm hiểu về Java Web, HTTP và mô hình Client-Server
- Hiểu về Servlet và cách Servlet hoạt động
- Viết Servlet đầu tiên (HelloServlet)
- Cách xây dựng và deploy ứng dụng web trên Tomcat
- Xử lý tham số từ URL trong Servlet

## 🛠️ Yêu cầu hệ thống

### Phần mềm cần thiết:

1. **Java Development Kit (JDK) 11 hoặc cao hơn**
   ```bash
   java -version
   ```

2. **Apache Maven 3.6 hoặc cao hơn**
   ```bash
   mvn -version
   ```

3. **Apache Tomcat 9.0 hoặc cao hơn**
   - Tải từ: https://tomcat.apache.org/
   - Hoặc sử dụng embedded Tomcat thông qua Maven plugin

4. **IDE (tùy chọn)**
   - IntelliJ IDEA
   - Eclipse IDE for Enterprise Java Developers
   - Visual Studio Code với Java Extension Pack

## 🚀 Cài đặt và chạy dự án

### Cách 1: Sử dụng Maven Tomcat Plugin (Khuyến nghị)

1. **Clone hoặc tải dự án**
   ```bash
   git clone <repository-url>
   cd java-web-servlet-basic
   ```

2. **Compile dự án**
   ```bash
   mvn clean compile
   ```

3. **Chạy với embedded Tomcat**
   ```bash
   mvn tomcat7:run
   ```

4. **Truy cập ứng dụng**
   - Mở trình duyệt và truy cập: `http://localhost:8080/servlet-basic`

### Cách 2: Deploy lên Tomcat Server

1. **Build WAR file**
   ```bash
   mvn clean package
   ```

2. **Copy WAR file to Tomcat**
   ```bash
   cp target/java-web-servlet-basic.war $TOMCAT_HOME/webapps/
   ```

3. **Khởi động Tomcat**
   ```bash
   $TOMCAT_HOME/bin/startup.sh    # Linux/Mac
   $TOMCAT_HOME/bin/startup.bat   # Windows
   ```

4. **Truy cập ứng dụng**
   - Mở trình duyệt: `http://localhost:8080/java-web-servlet-basic`

## 📁 Cấu trúc dự án

```
java-web-servlet-basic/
├── pom.xml                                 # Maven configuration
├── README.md                               # Tài liệu dự án
├── src/
│   └── main/
│       ├── java/
│       │   └── com/
│       │       └── example/
│       │           └── servlet/
│       │               ├── HelloServlet.java      # Servlet "Hello World"
│       │               └── ParameterServlet.java  # Servlet xử lý tham số
│       ├── resources/                      # Resources (empty)
│       └── webapp/
│           ├── index.html                  # Trang chủ
│           └── WEB-INF/
│               └── web.xml                 # Web deployment descriptor
└── target/                                 # Build output (generated)
```

## 🔧 Các Servlet trong dự án

### 1. HelloServlet
- **URL:** `/hello`
- **Mô tả:** Servlet đầu tiên trả về "Hello World"
- **Tính năng:**
  - Hiển thị thông tin servlet lifecycle
  - Thông tin request method và URI
  - Server information
  - Giao diện đẹp với CSS

### 2. ParameterServlet
- **URL:** `/param`
- **Mô tả:** Servlet nhận và xử lý tham số từ URL
- **Tính năng:**
  - Nhận tham số từ URL query string
  - Hiển thị tất cả parameters
  - Form tương tác để test
  - Bảo mật XSS với HTML escaping
  - Hỗ trợ cả GET và POST methods

## 🧪 Cách sử dụng và test

### Test HelloServlet:
1. Truy cập: `http://localhost:8080/servlet-basic/hello`
2. Quan sát thông tin servlet lifecycle
3. Kiểm tra các thông tin request được hiển thị

### Test ParameterServlet:

1. **Không có tham số:**
   ```
   http://localhost:8080/servlet-basic/param
   ```

2. **Với tham số cơ bản:**
   ```
   http://localhost:8080/servlet-basic/param?name=Java&age=25
   ```

3. **Với nhiều tham số:**
   ```
   http://localhost:8080/servlet-basic/param?name=Java&age=25&city=HaNoi&email=test@example.com
   ```

4. **Sử dụng form tương tác:**
   - Truy cập `/param` và sử dụng form để nhập dữ liệu
   - Test với các giá trị khác nhau

## 📖 Kiến thức được minh họa

### 1. Servlet Lifecycle
- `init()`: Khởi tạo servlet
- `doGet()`, `doPost()`: Xử lý HTTP requests
- `destroy()`: Hủy servlet

### 2. HTTP Request Processing
- Nhận HTTP GET/POST requests
- Xử lý request parameters
- Tạo HTTP response

### 3. Parameter Handling
- `request.getParameter(name)`: Lấy giá trị tham số
- `request.getParameterNames()`: Lấy tất cả tên tham số
- `request.getParameterValues(name)`: Lấy mảng giá trị tham số

### 4. HTML Response Generation
- Sử dụng `PrintWriter` để tạo HTML
- Dynamic content generation
- CSS styling inline

### 5. Security Best Practices
- HTML escaping để tránh XSS attacks
- Input validation

### 6. Web Configuration
- `web.xml` deployment descriptor
- Servlet mapping và URL patterns

## 🎯 Bài tập đã hoàn thành

✅ **Bài tập 1:** Viết một Servlet trả về "Hello World"
- Tạo `HelloServlet` với thông tin chi tiết
- Hiển thị servlet lifecycle information
- Giao diện đẹp với CSS

✅ **Bài tập 2:** Viết Servlet nhận tham số từ URL và hiển thị ra trang
- Tạo `ParameterServlet` xử lý parameters
- Hiển thị tất cả tham số được truyền
- Form tương tác để test
- Bảo mật XSS

## 🔍 Troubleshooting

### Lỗi thường gặp:

1. **Port 8080 đã được sử dụng:**
   ```bash
   # Thay đổi port trong pom.xml hoặc dừng service đang dùng port 8080
   sudo lsof -i :8080
   ```

2. **Java version không tương thích:**
   ```bash
   # Kiểm tra Java version
   java -version
   # Cập nhật JAVA_HOME nếu cần
   ```

3. **Maven không tìm thấy dependencies:**
   ```bash
   # Xóa cache và tải lại
   mvn clean
   mvn dependency:resolve
   ```

4. **Servlet không load:**
   - Kiểm tra `web.xml` configuration
   - Đảm bảo class path đúng trong servlet-class
   - Kiểm tra console logs cho error messages

## 📚 Tài liệu tham khảo

- [Oracle Java Servlet Tutorial](https://docs.oracle.com/javaee/7/tutorial/servlets.htm)
- [Apache Tomcat Documentation](https://tomcat.apache.org/tomcat-9.0-doc/)
- [Maven Getting Started Guide](https://maven.apache.org/guides/getting-started/)

## 🤝 Đóng góp

Nếu bạn muốn cải thiện dự án:
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

Dự án này được sử dụng cho mục đích học tập và giáo dục.

---

**Happy Coding! 🚀**