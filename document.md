# ĐẶC TẢ HỆ THỐNG QUANTUMSHIELD FINEDU

## I. Tổng quan

QuantumShield FinEdu là Web Dashboard mô phỏng phân phối khóa CV-QKD/FSO qua
vệ tinh trên dữ liệu kênh đo thực nghiệm. A2C đóng vai trò lớp điều khiển chọn
ngưỡng thu; khóa sau sifting, sửa lỗi và privacy amplification được dùng để
bảo vệ dữ liệu tài chính mẫu bằng AES-256-GCM.

Sản phẩm là phòng thí nghiệm phần mềm phục vụ đào tạo và nghiên cứu, không phải
hệ thống QKD phần cứng đã được chứng nhận để triển khai trực tiếp trong ngân
hàng.

## II. Công nghệ

- Frontend: React, TypeScript, Vite và Tailwind CSS.
- Backend: FastAPI, PyTorch, NumPy và `cryptography`.
- AI: `PolicyNet` nạp bắt buộc từ `backend/weights/policy.pth`.
- Dữ liệu: `clearlowSI.csv`, `clearhighSI.csv`, `lightrain.csv`, mỗi trace có
  `2^24` giá trị độ lợi kênh.
- Bảo vệ payload: AES-256-GCM, nonce 96 bit, authentication tag 128 bit.

## III. Pipeline backend

1. Chọn dataset, vị trí bắt đầu và độ dài cửa sổ 4.096-16.384 mẫu.
2. Cắt cửa sổ trực tiếp từ trace, chuẩn hóa giá trị về `[0, 1]` và áp dụng suy
   hao theo góc thiên đỉnh.
3. Tính state tám chiều: mean, std, min, max, Q25, Q75, công suất phát và
   log-mean.
4. Chọn `rho`: người học đặt trực tiếp ở fixed mode, hoặc PolicyNet chọn trong
   `[0, 5]` ở adaptive mode.
5. Charlie tạo tín hiệu cho Alice và Bob; hệ thống sifting theo basis.
6. Nếu Eve hoạt động, mô hình intercept-resend gây disturbance tối đa 25% theo
   Gaussian overlap và đồng thời tính `Peve`.
7. Phiên bị hủy nếu không có bit sifted hoặc QBER từ 11% trở lên.
8. Với phiên đạt ngưỡng: Cascade sửa lỗi, trừ lượng parity bị lộ, ước lượng
   thông tin của Eve, trừ security margin 32 bit và dùng Toeplitz universal
   hash để tạo khóa cuối.
9. Chỉ khi còn ít nhất 256 bit khóa và khóa Alice/Bob trùng nhau, Alice mới mã
   hóa payload bằng AES-256-GCM. Bob phải xác thực tag trước khi nhận bản rõ.

Backend trả thêm nguyên nhân hủy có cấu trúc, nguồn/cửa sổ dataset, mean/std,
interception strength, nonce, tag và trạng thái integrity verification.

## IV. Dashboard

Sidebar cho phép:

- Chọn Low Scintillation, High Scintillation hoặc Light Rain.
- Chọn vị trí bắt đầu, độ dài cửa sổ hoặc lấy cửa sổ ngẫu nhiên.
- Chọn fixed/adaptive; fixed mode có slider `rho`.
- Điều chỉnh công suất `[-5, 10] dBm`, góc `[0, 60]` và Eve `[0, 200] m`.
- Chạy thí nghiệm theo yêu cầu thay vì tự gọi API sau mỗi thay đổi slider.

Main panel hiển thị QBER/Psift/Peve, 256 bit preview, số bit sửa lỗi/rò rỉ,
khóa cuối, ciphertext Base64, nonce, authentication tag và bản rõ tại Bob.
Tối đa 20 kết quả gần nhất được giữ trong phiên trình duyệt và có thể xuất CSV.

Banner dùng cùng tiêu chí với backend:

- Xanh: đủ khóa, AES-GCM xác thực và round-trip thành công.
- Đỏ: QBER từ 11% trở lên, không phát sinh ciphertext.
- Vàng: QBER chưa vượt ngưỡng nhưng không còn đủ 256 bit khóa cho AES.

## V. Kịch bản demo

1. Fixed `rho=0`, Low Scintillation, cửa sổ 0/8.192, 4,5 dBm, góc 60°:
   giữ quá nhiều bit nhiễu, QBER vượt 11%, phiên bị hủy.
2. Giữ nguyên toàn bộ đầu vào và chuyển sang AI Adaptive: A2C chọn ngưỡng,
   QBER xuống dưới 11%, tạo đủ khóa và AES-256-GCM thành công.
3. Low Scintillation, 5 dBm, góc 30°, Eve ở 20 m: intercept-resend làm QBER
   vượt ngưỡng; Alice không tạo ciphertext.

Các giá trị trên được khóa bằng unit/integration test trong
`backend/test_quantumshield.py` để tránh preset demo bị lệch khi sửa code.
