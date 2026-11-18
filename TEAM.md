# Team

## Thông tin nhóm

- Tên nhóm ('Nhom2nguoi'):
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-Nhom2nguoi-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S8

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Vũ Đức Thắng | 2A202603601 | Vận hành và pháp lý | V |
|   2 | Bùi Mạnh Linh | 2A202603539 | Kỹ sư cổng | |
|   3 | Nguyễn Hữu Tiến | 2A202603598 | Đo kiểm & Bằng chứng | |
|   4 | Mai Tuấn Anh | 2A202603574 | Sản phẩm & Kinh doanh | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenHuuTien-2A202603598

### Phần việc phụ trách

- Vai trong bàn: Kỹ sư Đo kiểm & Bằng chứng
- Các mục phụ trách: A2 (Telemetry/đo lường), A3 (Khoảng tin cậy), B0–B2 (Đo kiểm baseline & phân tích lỗi chìm), B7.3 (Behavioral test), C0 (Nhật ký chạy 4 mốc), C2 (Bảng soát lỗi thẻ S8 qua trace), C8 (Chỉ số theo dõi mới trong `lab10/monitors.py`), hỗ trợ chạy grade và kiểm tra regression.
- File tham gia: `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`, `lab10/monitors.py`.

### Đóng góp cụ thể

- Thực hiện đo kiểm bộ nền (baseline) tại B0–B2, phân tích ca lỗi chìm T-002@55 bị model đè dữ liệu DB.
- Thiết kế 2 ca behavioral test hiểm tại B7.3 chứng minh hệ thống từ chối hoàn sai và chặn lộ PII.
- Đo kiểm mốc chuẩn bị (prepared) và sự cố thẻ S8; hoàn thành nhật ký số liệu C0.
- Thực hiện trace phân tích sâu C2 cho 3 loại lỗi thẻ S8 (phê duyệt hết hạn, phê duyệt vượt trần, và khách hoàn dồn dập).
- Lập trình và kiểm thử thành công monitor mới `approval_usage_rate` và `recheck_rate` trong `lab10/monitors.py` (C8), giúp hệ thống tự động phát hiện bất thường và đạt kết quả kiểm định `monitor ✅` trong `lab10.grade`.

### Bằng chứng

- Commit ký tiêu chí: `395b881`
- Commit hoàn thành B7.3: `8e16488`
- Mã lần chạy baseline: `R-base-before-20261118-153905-bde05c`
- Mã lần chạy prepared & grade S8: `R-S8-grade-20261118-170342-79c1d8`, `R-S8-grade-20261118-172624-90a202`
- Dòng trong phiếu: Form B mục B0–B2, B7.3; Form C mục C0, C2, C8.

### Exit ticket

- **Một điều học được:** Lòng tin của con người trong hệ thống không thể chỉ phục hồi bằng việc giảm tỷ lệ lỗi trên metric kỹ thuật mà cần phân định rõ ràng thứ bậc kiểm soát, tính hợp lệ của thẩm quyền phê duyệt (hết hạn, thu hồi, hạn mức) và minh bạch lý do ra quyết định.
- **Một điều còn chưa chắc:** Làm thế nào để cân bằng tối ưu giữa việc kiểm soát rủi ro gian lận hoàn tiền dồn dập (rate-limit/escalate) với trải nghiệm của khách hàng mua nhiều đơn hợp lệ bị giao trễ cùng ngày ngoài đời thực.
