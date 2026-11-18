# Team

## Thông tin nhóm

- Tên nhóm: `Nhom2nguoi` (tên repo giữ nguyên dù nhóm có 4 người).
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
- Mã lần chạy prepared & grade S8 được thành viên ghi trước: `R-S8-grade-20261118-170342-79c1d8`, `R-S8-grade-20261118-172624-90a202` (chưa nhận report gốc). Kiểm chứng cuối có file thật: `R-S8-grade-20261118-205236-536bf2`, monitor/regression/visible đạt; integrity còn thiếu gói chính thức.
- Dòng trong phiếu: Form B mục B0–B2, B7.3; Form C mục C0, C2, C8.

### Exit ticket

- **Một điều học được:** Lòng tin của con người trong hệ thống không thể chỉ phục hồi bằng việc giảm tỷ lệ lỗi trên metric kỹ thuật mà cần phân định rõ ràng thứ bậc kiểm soát, tính hợp lệ của thẩm quyền phê duyệt (hết hạn, thu hồi, hạn mức) và minh bạch lý do ra quyết định.
- **Một điều còn chưa chắc:** Làm thế nào để cân bằng tối ưu giữa việc kiểm soát rủi ro gian lận hoàn tiền dồn dập (rate-limit/escalate) với trải nghiệm của khách hàng mua nhiều đơn hợp lệ bị giao trễ cùng ngày ngoài đời thực.


## VuDucThang-2A202603601

### Phần việc phụ trách

Trưởng nhóm, vận hành và pháp lý: B4–B6, operations/legal, B7.5–B7.6; C1, C3.1/C3.4, C4, giả định C5; tổng hợp C9–C11, hồ sơ nộp và phối hợp quyết định.

### Đóng góp cụ thể

Chủ trì phiên làm việc với trợ lý AI để tổng hợp HAZOP, pre-mortem (đã xác nhận nhóm thống nhất ba ưu tiên), runbook, kiểm tra hash xuống dòng và hoàn thiện tài liệu. Hồ sơ v2 ghi Cải tiến thêm theo phạm vi công việc được trưởng nhóm giao cho trợ lý; không tạo chữ ký tay hoặc chứng nhận thay cá nhân.

### Bằng chứng

Phiếu B/C các mục trên; grade `R-S8-grade-20261118-205236-536bf2`; commit tiêu chí 395b881; snapshot 21ef0483; file docs/evidence-status.md.

### Exit ticket

- Bài học từ phần việc: cấu hình kiểm mẫu không đủ khôi phục lòng tin nếu hệ thống vẫn dùng phê duyệt sai.
- Điều còn chưa chắc: người duyệt thật cần bằng chứng và mức kiểm nào trước khi giảm kiểm tay.
- Nội dung được trợ lý hỗ trợ soạn theo yêu cầu trưởng nhóm; không khẳng định đã phỏng vấn cá nhân.

## BuiManhLinh-2A202603539

### Phần việc phụ trách

Kỹ sư cổng: guards.py, B7.1–B7.2; phân tích/sửa quyền phê duyệt, trần khách/ngày, C6–C7 và C9.

### Đóng góp cụ thể

Theo commit 24f01e8: bổ sung _approval_problem để kiểm phạm vi, người duyệt, thời hạn, trạng thái và hạn mức; cộng ledger kiểm trần tự động/ngày/khách; cập nhật cây nguyên nhân trước/sau. Đóng góp được tổng hợp từ lịch sử repo theo phân công. Trợ lý hỗ trợ biên tập hồ sơ, chưa có thông tin riêng về công cụ cá nhân dùng khi viết code.

### Bằng chứng

Commit 24f01e8; guards.py; grade `R-S8-grade-20261118-205236-536bf2`: visible/regression đạt, bản sửa vẫn phục vụ S8-05 hợp lệ.

### Exit ticket

- Bài học từ phần việc: mã tồn tại không đồng nghĩa phê duyệt hợp lệ; phạm vi, trạng thái, thời hạn và số tiền đều cần kiểm trước ghi.
- Điều còn chưa chắc: cách bảo đảm kiểm quyền và ghi tiền nguyên tử khi có nhiều yêu cầu đồng thời.
- Nội dung được trợ lý hỗ trợ soạn theo yêu cầu trưởng nhóm; không khẳng định đã phỏng vấn cá nhân.

## MaiTuanAnh-2A202603574

### Phần việc phụ trách

Sản phẩm/kinh doanh: tiêu chí, B3/B7.4, business config; specification/giả định C5, phối hợp quyết định v1/v2 và chi phí/ROI.

### Đóng góp cụ thể

Tổng hợp dựa phân công và nội dung repo: B3, B7.4, C5 có nội dung; commit 91a1c4f cập nhật C5. Tiêu chí/Phiếu A được trợ lý hỗ trợ trong phiên làm việc của trưởng nhóm, không gán toàn bộ nội dung đó là do cá nhân tự viết. Phần hồ sơ này được trợ lý hỗ trợ biên tập theo phân công; không suy ra công cụ cá nhân đã dùng từ lịch sử Git.

### Bằng chứng

Các mục B3/B7.4/C5, commit 91a1c4f và grade `R-S8-grade-20261118-205236-536bf2`; S8 after chi phí 2.952đ/ticket, ROI 2.39; bộ nền nhóm ? vẫn cần xem lại riêng.

### Exit ticket

- Bài học từ phần việc: ROI là tiết kiệm ròng chia tổng chi phí, không phải tỷ lệ tiết kiệm trên giá làm tay.
- Điều còn chưa chắc: chi phí theo kho và công kiểm lại thay đổi bao nhiêu ở pilot thật.
- Nội dung được trợ lý hỗ trợ soạn theo yêu cầu trưởng nhóm; không khẳng định đã phỏng vấn cá nhân.

## Ghi nhận dùng AI và xác nhận cá nhân

Vũ Đức Thắng đã dùng trợ lý trong phiên này để đọc repo, hỗ trợ soạn phiếu/config, tổng hợp bằng chứng, chạy kiểm tra và chuẩn bị hồ sơ. Ba mục cá nhân bổ sung có ghi nguồn và nội dung exit ticket do trợ lý hỗ trợ soạn theo yêu cầu trưởng nhóm; không trình bày là lời tự thuật đã được phỏng vấn riêng. Mỗi thành viên chịu trách nhiệm đọc, hiểu và giải thích phần mang tên mình. Mục Nguyễn Hữu Tiến giữ nguyên nội dung từ repo; Tiến cần tự bổ sung việc dùng AI nếu có. Không ghi nhận ai đã nộp LMS, demo với Coach hoặc tạo chữ ký tay khi chưa có xác nhận. Quyết định trong hồ sơ được ghi rõ tại C12.
