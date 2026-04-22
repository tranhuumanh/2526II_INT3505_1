import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. Cấu hình (Thiết lập ngưỡng và số lượng người dùng)
export let options = {
    vus: 10,           // 10 người dùng ảo
    duration: '5s',    // Chạy trong 5 giây
};

// 2. Hàm thực thi chính (Phải có từ khóa 'export default')
export default function () {
    // Gọi API của bạn
    let res = http.get('http://127.0.0.1:5000/books');

    // Kiểm tra kết quả trả về
    check(res, {
        'status là 200': (r) => r.status === 200,
        'phản hồi nhanh < 200ms': (r) => r.timings.duration < 200,
    });

    // Nghỉ 1 giây trước khi lặp lại (giả lập hành vi người dùng thật)
    sleep(1);
}