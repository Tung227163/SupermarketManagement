#!/bin/bash

# Script để chạy Java Web Servlet Basic Project
# Ngày 1: Tổng quan về Java Web và Servlet cơ bản

echo "🚀 Java Web Servlet Basic - Ngày 1"
echo "=================================="
echo ""

# Kiểm tra Java
echo "📋 Kiểm tra môi trường..."
if command -v java &> /dev/null; then
    echo "✅ Java: $(java -version 2>&1 | head -n 1)"
else
    echo "❌ Java không được cài đặt!"
    echo "   Vui lòng cài đặt JDK 11 hoặc cao hơn"
    exit 1
fi

# Kiểm tra Maven
if command -v mvn &> /dev/null; then
    echo "✅ Maven: $(mvn -version 2>&1 | head -n 1)"
    
    echo ""
    echo "🔨 Compile dự án..."
    mvn clean compile
    
    if [ $? -eq 0 ]; then
        echo "✅ Compile thành công!"
        echo ""
        echo "🚀 Chạy ứng dụng..."
        echo "   Truy cập: http://localhost:8080/servlet-basic"
        echo "   Nhấn Ctrl+C để dừng"
        echo ""
        mvn tomcat7:run
    else
        echo "❌ Compile thất bại!"
        exit 1
    fi
else
    echo "⚠️  Maven không được cài đặt!"
    echo ""
    echo "📖 Hướng dẫn cài đặt Maven:"
    echo "   Ubuntu/Debian: sudo apt install maven"
    echo "   CentOS/RHEL: sudo yum install maven"
    echo "   macOS: brew install maven"
    echo "   Windows: Tải từ https://maven.apache.org/"
    echo ""
    echo "📖 Hoặc sử dụng cách khác để chạy:"
    echo "   1. Cài đặt Maven"
    echo "   2. Chạy: mvn clean compile"
    echo "   3. Chạy: mvn tomcat7:run"
    echo "   4. Truy cập: http://localhost:8080/servlet-basic"
    echo ""
    echo "📖 Hoặc deploy lên Tomcat server:"
    echo "   1. mvn clean package"
    echo "   2. Copy target/java-web-servlet-basic.war vào Tomcat webapps/"
    echo "   3. Khởi động Tomcat"
    exit 1
fi