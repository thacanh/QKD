# QuantumShield FinEdu v2

QuantumShield FinEdu là phòng thí nghiệm web mô phỏng CV-QKD/FSO trên dữ liệu
kênh đo thực nghiệm. Mô hình A2C chọn ngưỡng thu, chuỗi khóa được sửa lỗi và
rút gọn bằng Toeplitz, sau đó 256 bit khóa QKD được dùng trực tiếp cho
AES-256-GCM để bảo vệ nội dung tài chính mẫu.

> Đây là phần mềm mô phỏng phục vụ đào tạo và nghiên cứu, không phải thiết bị
> QKD vật lý đã được kiểm định cho hệ thống tài chính thực tế.

## Điểm chính của phiên bản 2

- Đọc cửa sổ 4.096-16.384 mẫu trực tiếp từ `clearlowSI.csv`,
  `clearhighSI.csv` hoặc `lightrain.csv`.
- So sánh ngưỡng cố định với A2C trên đúng cùng cửa sổ dữ liệu.
- Mô phỏng Eve kiểu intercept-resend: Eve ở gần làm QBER Bob tăng và có thể
  khiến phiên bị hủy ở ngưỡng 11%.
- Cascade + ước lượng rò rỉ + Toeplitz privacy amplification dùng FFT.
- AES-256-GCM với nonce 96 bit, authentication tag 128 bit và AAD gắn với
  metadata phiên.
- Lịch sử tối đa 20 thí nghiệm và xuất CSV từ dashboard.
- Không âm thầm chạy model ngẫu nhiên khi weight thiếu hoặc không tương thích.
- Backend nạp trực tiếp model ba điều kiện từ `backend/weights/policy.pth`; dashboard
  có ba nút chọn Low SI, High SI và Light Rain.

## Chạy dự án

Backend, từ thư mục gốc:

```powershell
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend, ở terminal khác:

```powershell
cd frontend
npm install
npm run dev
```

Mở `http://localhost:5173`. API health check nằm tại
`http://localhost:8000/api/health`.

## Kịch bản demo đề xuất

1. **Fixed ρ=0:** Low Scintillation, cửa sổ 0, 8.192 mẫu, 4,5 dBm, góc 60°.
   Ngưỡng quá thấp giữ nhiều bit nhiễu, QBER vượt 11% và phiên bị hủy.
2. **AI Adaptive:** giữ nguyên mọi đầu vào. A2C chọn ρ thích nghi, tạo đủ khóa
   cho AES-256-GCM và Bob xác thực/giải mã thành công.
3. **Eve:** Low Scintillation, 5 dBm, góc 30°, Eve cách Bob 20 m. Tấn công làm
   QBER vượt ngưỡng và Alice không tạo ciphertext.

## Kiểm thử

```powershell
python -m unittest backend.test_quantumshield -v
cd frontend
npm run lint
npm run build
```

CSV lớn được chuyển thành cache `*.uint8.npy` ở lần đọc đầu tiên. Cache chỉ là
artifact tăng tốc, được bỏ qua bởi `backend/.gitignore` và có thể xóa để tái tạo.
