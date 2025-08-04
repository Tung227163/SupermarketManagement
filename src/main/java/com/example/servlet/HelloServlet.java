package com.example.servlet;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

/**
 * HelloServlet - Servlet đầu tiên trả về "Hello World"
 * 
 * Servlet này minh họa:
 * - Cách tạo một servlet cơ bản
 * - Cách xử lý HTTP GET request
 * - Cách trả về response HTML
 * 
 * URL: http://localhost:8080/servlet-basic/hello
 */
public class HelloServlet extends HttpServlet {
    
    private static final long serialVersionUID = 1L;
    
    /**
     * Constructor mặc định
     */
    public HelloServlet() {
        super();
    }
    
    /**
     * Phương thức init() được gọi khi servlet được khởi tạo
     */
    @Override
    public void init() throws ServletException {
        System.out.println("HelloServlet đã được khởi tạo!");
    }
    
    /**
     * Xử lý HTTP GET requests
     * Phương thức này được gọi khi client gửi GET request đến servlet
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
            // Tạo HTML response
            out.println("<!DOCTYPE html>");
            out.println("<html>");
            out.println("<head>");
            out.println("<title>Hello Servlet</title>");
            out.println("<meta charset='UTF-8'>");
            out.println("<style>");
            out.println("body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }");
            out.println(".container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }");
            out.println("h1 { color: #333; }");
            out.println(".info { background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0; }");
            out.println("</style>");
            out.println("</head>");
            out.println("<body>");
            out.println("<div class='container'>");
            out.println("<h1>🎉 Hello World từ Servlet!</h1>");
            out.println("<p>Chào mừng bạn đến với Java Web Servlet!</p>");
            
            out.println("<div class='info'>");
            out.println("<h3>Thông tin Servlet:</h3>");
            out.println("<p><strong>Servlet Name:</strong> " + this.getServletName() + "</p>");
            out.println("<p><strong>Request Method:</strong> " + request.getMethod() + "</p>");
            out.println("<p><strong>Request URI:</strong> " + request.getRequestURI() + "</p>");
            out.println("<p><strong>Server Info:</strong> " + getServletContext().getServerInfo() + "</p>");
            out.println("</div>");
            
            out.println("<p>Đây là servlet đầu tiên của bạn! 🚀</p>");
            out.println("<p><a href='/servlet-basic/param?name=Java&age=25'>Thử servlet với tham số</a></p>");
            out.println("</div>");
            out.println("</body>");
            out.println("</html>");
            
        } finally {
            out.close();
        }
    }
    
    /**
     * Xử lý HTTP POST requests
     * Trong ví dụ này, chúng ta chuyển POST requests sang doGet()
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        doGet(request, response);
    }
    
    /**
     * Phương thức destroy() được gọi khi servlet bị hủy
     */
    @Override
    public void destroy() {
        System.out.println("HelloServlet đã được hủy!");
    }
}