# Tái lập và kiểm tra bài nộp

Các file trong `submission/` được lưu nguyên byte, manifest bảo vệ bộ gom. Source trên Windows có thể bị Git đổi xuống dòng; `.gitattributes` giữ LF cho nguồn manifest và đầu vào code/config. Riêng tiêu chí/snapshot là bản đã ký; không tự format hoặc ký lại.

## Kiểm tra bộ gom

```powershell
python -m lab10.check_submission
python -m unittest discover -s tests
```

Trong phiên hoàn thiện: 13 tests đạt, kiểm bộ nộp báo ĐỦ THÀNH PHẦN. Đủ thành phần không đồng nghĩa integrity hoặc test ẩn đã đạt.

## Nếu clone sang máy mới và hash file ký khác

Không thay ngưỡng hoặc khóa. Bản `submission/config/acceptance_criteria.json` và lock được gom từ đúng file đã ký, giữ nguyên byte trong Git. Kiểm hash bản gom trước khi khôi phục source:

```powershell
$signedLock = Get-Content -Raw -Encoding UTF8 .\submission\config\acceptance_criteria.lock | ConvertFrom-Json
$artifactHash = (Get-FileHash .\submission\config\acceptance_criteria.json -Algorithm SHA256).Hash.ToLowerInvariant()
if ($artifactHash -ne $signedLock.sha256) { throw 'Bản tiêu chí trong bộ gom không khớp chữ ký; dừng và đối chiếu bản gốc.' }
Copy-Item -LiteralPath .\submission\config\acceptance_criteria.json -Destination .\config\acceptance_criteria.json
Copy-Item -LiteralPath .\submission\config\acceptance_criteria.lock -Destination .\config\acceptance_criteria.lock
python -m lab10.criteria verify
```

Đây là khôi phục chính xác byte đã ký từ artifact, không sửa nội dung hoặc tạo chữ ký mới. Nếu snapshot không khớp thì kiểm hash bản gom với round1.lock trước, đối chiếu bản gốc và khôi phục đúng byte; không chạy checkpoint lần nữa.

## Chạy lại bản hiện tại

```powershell
python -m lab10.grade --incident S8
```

Kết quả đã đo: visible/regression/monitor đạt; integrity còn thiếu 28 file S1–S7 mà manifest yêu cầu. Nguồn cards được cung cấp trả Repository not found; không tự xóa mục manifest hoặc làm giả file. Chỉ nhận gói chính thức/hướng dẫn tương thích từ Coach, không đọc nội dung thẻ ngoài S8 để làm bài.

Nếu kết quả có mã mới và nhóm chọn dùng nó cho bài nộp, cập nhật C0/C12 và các tham chiếu liên quan trước khi chạy:

```powershell
python -m lab10.check_submission --collect
```

Grade mới ghi đúng thời gian mới; không tái tạo mã report/journal lịch sử từ máy thành viên. Giữ hồ sơ thiếu nguồn ở `docs/evidence-status.md`.
