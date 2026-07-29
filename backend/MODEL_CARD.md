# Policy model card

## Artifact

- Weight đang được backend sử dụng: `weights/policy.pth`
- Architecture: `PolicyNet`, trạng thái 8 chiều, action là hệ số ngưỡng
  `rho` trong `[0, 5]`.
- Runtime: PyTorch CPU hoặc CUDA; backend yêu cầu weight tải `strict=True`.

## Dữ liệu và split

Mô hình hiện hành do nhóm cung cấp được huấn luyện chung trên ba điều kiện:

- Low Scintillation: 40 trace train, 40 trace test.
- High Scintillation: 40 trace train, 40 trace test.
- Light Rain: 40 trace train, 40 trace test.

Mỗi trạng thái gồm mean, standard deviation, min, max, percentile 25/75,
công suất phát và log-mean của cửa sổ kênh. Script huấn luyện hiện hành chưa
được đóng gói trong repository này, vì vậy checkpoint chưa thể tái lập đầy đủ
chỉ từ mã nguồn đang công bố.

## Giới hạn

- Weight chỉ điều khiển ngưỡng thu; không thay thế giao thức QKD.
- Kết quả phụ thuộc mô hình vật lý/nhiễu mô phỏng và không phải chứng nhận an
  toàn phần cứng.
- Cần lưu kèm script train hiện hành, seed, phiên bản thư viện và metrics từng
  tập trước khi công bố kết quả nghiên cứu có khả năng tái lập đầy đủ.
