# Trạng thái bằng chứng và giới hạn bài nộp

## Kết quả đo bổ sung thực tế

- Grade: `R-S8-grade-20261118-205236-536bf2`, code_hash `536bf24a371db6c95db422959c3222d7ddb5122b095f6301eb8b9224fc69ebf1`.
- Base S8: `R-S8-before-20261118-205240-536bf2`; prepared: `R-S8-prepared-20261118-205240-536bf2`; after: `R-S8-after-20261118-205241-536bf2`.
- Đo bổ sung bộ nền prepared: `R-base-prepared-20261118-204525-c522a1`. Đều được chạy sau khi biết S8, không thay thế thời điểm hoặc report lịch sử B8.
- Visible, regression, monitor, criteria và snapshot đạt; hidden chưa có trên máy. S8 after 260/260, bộ nền 110/110; tác hại 0; hàng chờ 5 phút/0 ca ùn; S8 chi phí 2.952đ, ROI 2.39.
- Grade tổng FAIL vì thiếu 28 file S1–S7 được manifest yêu cầu. 23 file hiện có chỉ khác CRLF đã khôi phục byte LF khớp hash chính thức; không sửa manifest, tiêu chí hoặc snapshot.
- Đã thử fetch repo cards chính thức đang được cung cấp; trả Repository not found. Cần Coach/người có quyền cung cấp đủ gói hoặc hướng dẫn chính thức tương thích manifest; không tự xóa các mục kiểm. Chưa đọc nội dung các thẻ khác S8.
- .gitattributes giữ LF cho nguồn khóa và nguyên byte cho tiêu chí/snapshot/bộ gom. Chưa tuyên bố integrity đạt.

## Tham chiếu lịch sử chưa nhận report/journal gốc

### templates/form-b-evaluation-gates.md

- `R-base-after-20261118-154301-d8c618`
- `R-base-before-20261118-161648-0db83f`
- `R-base-prepared-20261118-163302-79c1d8`

### templates/form-c-incident.md

- `R-S8-after-20261118-173547-c522a1`
- `R-S8-before-20261118-170344-79c1d8`
- `R-S8-grade-20261118-170342-79c1d8`
- `R-S8-grade-20261118-173554-c522a1`
- `R-S8-prepared-20261118-170344-79c1d8`

### TEAM.md

- `R-S8-grade-20261118-170342-79c1d8`
- `R-S8-grade-20261118-172624-90a202`

Các mã trên được giữ để minh bạch, không tái tạo report hoặc dòng journal giả. Số liệu chính của C7–C12 hiện đã gắn vào lần đo bổ sung có file thật; B8 lịch sử giữ nguyên. Không bắt buộc chạy lại cùng ID/thời điểm cũ. Nhóm cần nhận file gốc hoặc giải trình thiếu bằng chứng này cho Coach.

## Việc cần con người/nguồn bên ngoài hoàn tất

- PIC xác nhận hoặc sửa đề xuất Cải tiến thêm và ký v2; tiêu chí đã ký không thay đổi.
- Từng thành viên tự rà đóng góp, dùng AI và exit ticket. Bản gợi ý trong TEAM không phải lời xác nhận cá nhân đã thu thập.
- Xác nhận quyền Read của tài khoản chấm và lịch demo/phản biện; không có chứng cứ truy cập trong phiên này.
- Mỗi thành viên tự nộp link repo trên LMS trước hạn hoặc hạn đã được Coach gia hạn; trợ lý không đăng nhập/nộp LMS.
- Gói chính thức/manifest cần được làm rõ trước khi xét mở pilot. Nếu quá hạn cải tiến vẫn không gỡ được thì ra quyết định tiếp theo đúng criteria, không ngầm gia hạn.

## Giải trình phạm vi kiểm tra

Hai ticket adhoc không chứng minh chống mọi prompt injection. Test tuần tự không chứng minh concurrency, thu hồi phê duyệt đồng thời hay idempotency ngoài môi trường mock. Nhóm ? của bộ nền có chi phí 10.359đ/ticket, chưa hiệu quả riêng theo trần đã ký, cần kiểm lại trước pilot thật. Điều kiện bảo mật/pilot thật còn Chưa trong checklist để tránh khẳng định quá mức.

## Chuẩn hóa byte trước lần kiểm tra cuối

Đã đặt LF cho bốn đầu vào được phép sửa (guards, monitors, operating_gates, switches) để code_hash tái lập giữa hệ điều hành; không đổi logic hoặc giá trị cấu hình. Sau đổi định dạng đã chạy grade mới nêu trên. Tiêu chí, lock và hai snapshot giữ nguyên byte; bản thu gom dùng -text để bảo toàn chữ ký/hashes. Không dùng kết quả code_hash c522 của lượt trước để xác nhận bản LF mới.
