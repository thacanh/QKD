# QuantumShield FinEdu frontend

Dashboard React + TypeScript cho QuantumShield FinEdu.

```powershell
npm install
npm run dev
```

Frontend gọi `http://localhost:8000/api/simulate`. Hãy khởi động FastAPI từ
thư mục gốc trước khi chạy thí nghiệm. Các lệnh kiểm tra:

```powershell
npm run lint
npm run build
```

Giao diện cho phép chọn dataset, vị trí/độ dài cửa sổ, ngưỡng fixed hoặc AI,
công suất, góc thiên đỉnh và Eve. Mỗi kết quả hiển thị QBER/Psift/Peve, khóa
sau hậu xử lý, metadata AES-256-GCM và có thể được xuất thành CSV.
