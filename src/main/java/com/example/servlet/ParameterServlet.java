package com.example.servlet;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Enumeration;

/**
 * ParameterServlet - Servlet nhận và xử lý tham số từ URL
 * 
 * Servlet này minh họa:
 * - Cách nhận tham số từ URL (Query Parameters)
 * - Cách xử lý các tham số khác nhau
 * - Cách hiển thị thông tin tham số ra trang web
 * 
 * URL ví dụ: http://localhost:8080/servlet-basic/param?name=Java&age=25&city=HaNoi
 */
public class ParameterServlet extends HttpServlet {
    
    private static final long serialVersionUID = 1L;
    
    /**
     * Constructor mặc định
     */
    public ParameterServlet() {
        super();
    }
    
    /**
     * Phương thức init() được gọi khi servlet được khởi tạo
     */
    @Override
    public void init() throws ServletException {
        System.out.println("ParameterServlet đã được khởi tạo!");
    }
    
    /**
     * Xử lý HTTP GET requests với tham số
     * 
     * @param request - HttpServletRequest chứa thông tin từ client
     * @param response - HttpServletResponse để gửi phản hồi về client
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        // Thiết lập content type cho response
        response.setContentType("text/html;charset=UTF-8");
        
        // Lấy PrintWriter để ghi response
        PrintWriter out = response.getWriter();
        
        try {
            // Lấy các tham số cụ thể từ request
            String name = request.getParameter("name");
            String age = request.getParameter("age");
            String city = request.getParameter("city");
            String email = request.getParameter("email");
            
            // Tạo HTML response
            out.println("<!DOCTYPE html>");
            out.println("<html>");
            out.println("<head>");
            out.println("<title>Parameter Servlet</title>");
            out.println("<meta charset='UTF-8'>");
            out.println("<style>");
            out.println("body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }");
            out.println(".container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }");
            out.println("h1 { color: #333; }");
            out.println(".param-info { background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0; }");
            out.println(".param-item { background: #f9f9f9; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }");
            out.println(".form-section { background: #fff3cd; padding: 20px; border-radius: 5px; margin: 20px 0; }");
            out.println("input, select { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }");
            out.println("button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }");
            out.println("button:hover { background: #0056b3; }");
            out.println("</style>");
            out.println("</head>");
            out.println("<body>");
            out.println("<div class='container'>");
            out.println("<h1>📋 Parameter Servlet Demo</h1>");
            
            // Hiển thị thông tin tham số cụ thể
            out.println("<div class='param-info'>");
            out.println("<h3>Thông tin tham số nhận được:</h3>");
            
            if (name != null) {
                out.println("<div class='param-item'><strong>Tên:</strong> " + escapeHtml(name) + "</div>");
            }
            if (age != null) {
                out.println("<div class='param-item'><strong>Tuổi:</strong> " + escapeHtml(age) + "</div>");
            }
            if (city != null) {
                out.println("<div class='param-item'><strong>Thành phố:</strong> " + escapeHtml(city) + "</div>");
            }
            if (email != null) {
                out.println("<div class='param-item'><strong>Email:</strong> " + escapeHtml(email) + "</div>");
            }
            
            // Nếu không có tham số nào
            if (name == null && age == null && city == null && email == null) {
                out.println("<p>Không có tham số nào được truyền vào.</p>");
                out.println("<p>Thử truy cập: <a href='/servlet-basic/param?name=Java&age=25&city=HaNoi'>Với tham số mẫu</a></p>");
            }
            out.println("</div>");
            
            // Hiển thị tất cả tham số
            out.println("<div class='param-info'>");
            out.println("<h3>Tất cả tham số trong request:</h3>");
            
            Enumeration<String> parameterNames = request.getParameterNames();
            if (parameterNames.hasMoreElements()) {
                while (parameterNames.hasMoreElements()) {
                    String paramName = parameterNames.nextElement();
                    String[] paramValues = request.getParameterValues(paramName);
                    
                    out.println("<div class='param-item'>");
                    out.println("<strong>" + escapeHtml(paramName) + ":</strong> ");
                    
                    if (paramValues.length == 1) {
                        out.println(escapeHtml(paramValues[0]));
                    } else {
                        out.println("[");
                        for (int i = 0; i < paramValues.length; i++) {
                            out.println(escapeHtml(paramValues[i]));
                            if (i < paramValues.length - 1) {
                                out.println(", ");
                            }
                        }
                        out.println("]");
                    }
                    out.println("</div>");
                }
            } else {
                out.println("<p>Không có tham số nào.</p>");
            }
            out.println("</div>");
            
            // Form để test tham số
            out.println("<div class='form-section'>");
            out.println("<h3>Test với tham số của bạn:</h3>");
            out.println("<form method='GET' action='/servlet-basic/param'>");
            out.println("<p>");
            out.println("<label>Tên: </label>");
            out.println("<input type='text' name='name' value='" + (name != null ? escapeHtml(name) : "") + "' placeholder='Nhập tên của bạn'>");
            out.println("</p>");
            out.println("<p>");
            out.println("<label>Tuổi: </label>");
            out.println("<input type='number' name='age' value='" + (age != null ? escapeHtml(age) : "") + "' placeholder='Nhập tuổi'>");
            out.println("</p>");
            out.println("<p>");
            out.println("<label>Thành phố: </label>");
            out.println("<select name='city'>");
            out.println("<option value=''>Chọn thành phố</option>");
            out.println("<option value='HaNoi'" + (isSelected(city, "HaNoi")) + ">Hà Nội</option>");
            out.println("<option value='HoChiMinh'" + (isSelected(city, "HoChiMinh")) + ">TP. Hồ Chí Minh</option>");
            out.println("<option value='DaNang'" + (isSelected(city, "DaNang")) + ">Đà Nẵng</option>");
            out.println("<option value='CanTho'" + (isSelected(city, "CanTho")) + ">Cần Thơ</option>");
            out.println("</select>");
            out.println("</p>");
            out.println("<p>");
            out.println("<label>Email: </label>");
            out.println("<input type='email' name='email' value='" + (email != null ? escapeHtml(email) : "") + "' placeholder='Nhập email'>");
            out.println("</p>");
            out.println("<button type='submit'>Gửi tham số</button>");
            out.println("</form>");
            out.println("</div>");
            
            // Thông tin request
            out.println("<div class='param-info'>");
            out.println("<h3>Thông tin Request:</h3>");
            out.println("<p><strong>Method:</strong> " + request.getMethod() + "</p>");
            out.println("<p><strong>URI:</strong> " + request.getRequestURI() + "</p>");
            out.println("<p><strong>Query String:</strong> " + (request.getQueryString() != null ? request.getQueryString() : "Không có") + "</p>");
            out.println("<p><strong>Remote Address:</strong> " + request.getRemoteAddr() + "</p>");
            out.println("</div>");
            
            out.println("<p><a href='/servlet-basic/hello'>← Quay lại Hello Servlet</a></p>");
            out.println("</div>");
            out.println("</body>");
            out.println("</html>");
            
        } finally {
            out.close();
        }
    }
    
    /**
     * Xử lý HTTP POST requests
     * Chuyển POST requests sang doGet() để xử lý tương tự
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        doGet(request, response);
    }
    
    /**
     * Escape HTML để tránh XSS
     * @param input chuỗi cần escape
     * @return chuỗi đã được escape
     */
    private String escapeHtml(String input) {
        if (input == null) {
            return "";
        }
        return input.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\"", "&quot;")
                   .replace("'", "&#x27;");
    }
    
    /**
     * Kiểm tra option được chọn trong select
     * @param currentValue giá trị hiện tại
     * @param optionValue giá trị option
     * @return " selected" nếu được chọn, "" nếu không
     */
    private String isSelected(String currentValue, String optionValue) {
        return (currentValue != null && currentValue.equals(optionValue)) ? " selected" : "";
    }
    
    /**
     * Phương thức destroy() được gọi khi servlet bị hủy
     */
    @Override
    public void destroy() {
        System.out.println("ParameterServlet đã được hủy!");
    }
}