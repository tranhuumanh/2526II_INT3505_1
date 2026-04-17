Bước 1: Chuyển đổi API Blueprint sang OpenAPI
Chúng ta sẽ sử dụng công cụ apib2swagger. Đây là công cụ phổ biến nhất để bắc cầu giữa hai định dạng này.

Lệnh cài đặt:

PowerShell
npm install -g apib2swagger
Lệnh chuyển đổi:
Giả sử bạn đang đứng ở thư mục gốc của repo 2526II_INT3505_1:

PowerShell
apib2swagger -i openapi-comparison/api-blueprint/library.apib -o openapi-comparison/api-blueprint/swagger-bridge.yaml
Bước 2: Sinh code từ file đã chuyển đổi
Sau khi đã có file swagger-bridge.yaml, bạn sử dụng openapi-generator-cli để sinh Client SDK (ví dụ TypeScript Axios).

Lệnh thực hiện (Dùng định dạng PowerShell):

PowerShell
npx @openapitools/openapi-generator-cli generate `
     -i openapi-comparison/api-blueprint/swagger-bridge.yaml `
     -g typescript-axios `
     -o ./generated/apib-client
Bước 3: Kiểm tra kết quả
Sau khi chạy xong, bạn sẽ thấy thư mục generated/apib-client xuất hiện. Tại đây, mã nguồn TypeScript đã được tạo ra dựa trên các Data Structures (Book, BookInput) mà bạn định nghĩa trong file Blueprint: