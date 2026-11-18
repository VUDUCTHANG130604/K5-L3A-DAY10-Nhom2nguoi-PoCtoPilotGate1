# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-Nhom2nguoi-PoCtoPilotGate1

**Người cầm bút chính:** Mai Tuấn Anh (sản phẩm và kinh doanh).
Phối hợp: Nguyễn Hữu Tiến (đo kiểm), Bùi Mạnh Linh (cổng), Vũ Đức Thắng (vận hành và pháp lý, trưởng nhóm).

Lập trước mọi lần chạy trợ lý. Căn cứ: đề, dữ liệu và code trong repo. Chưa có PRD v1.1 và eval card Lab 9 để đối chiếu; không khẳng định đã kiểm chứng hai tài liệu đó. Ngưỡng là lựa chọn trước đo, không phải kết quả thực nghiệm.

## A1 · Mục tiêu (câu 1.1–1.2)

### Câu 1.1 · Mục tiêu cấp hệ thống

Xử lý yêu cầu hoàn phí giao trễ đúng chính sách và đúng bên chịu trách nhiệm, giảm chi phí so với làm tay, đồng thời giữ khả năng đối soát, quyền phê duyệt của con người và dữ liệu cá nhân của khách/người nhận.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Phạm Kiều Oanh (`NV-OANH`): đối soát được mỗi khoản hoàn với đơn, người trả và bằng chứng trách nhiệm; hãng/shop không gánh tiền hoặc lỗi không có căn cứ.
- Chị Trần Thị Hạnh (`NV-HANH`): nhận đủ bằng chứng khi ticket chuyển người, giữ quyền duyệt khoản vượt hạn mức; hàng chờ không quá SLA 60 phút và không vượt công suất người trực.

## A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3–1.4)

| Nội dung | Offline cho một bước: chọn chính sách | Telemetry production: ghi lỗi hãng thiếu căn cứ |
|---|---|---|
| Bước / hành vi | Agent chọn phiên bản chính sách hoàn tiền | Tool file_carrier_fault tạo lỗi cho hãng, ảnh hưởng đối soát bên thứ ba |
| Thước đo | Tỷ lệ lần chọn policy_id không khớp chính sách có hiệu lực tại ngày xử lý (%) | Số bản ghi lỗi hãng thiếu căn cứ nguyên nhân thuộc trách nhiệm hãng hoặc không khớp kiện/hãng (bản ghi) |
| Dữ liệu | Bộ nền 22 ticket × 5 seed; sự kiện policy.policy_id trong trace, bảng policies và ngày as_of. Tiến lập đáp án từ thời hạn hiệu lực; Linh rà soát độc lập. Bổ sung thẻ sau khi được phát. | Audit log thao tác ghi, bản ghi lỗi hãng, đơn/kiện, tracking và chính sách tại thời điểm ghi; thu tất cả bản ghi tự động, không dùng nhãn đúng/sai của test. Đây là telemetry cần triển khai trong pilot. |
| Cách tính | 100 × số lần policy đã chọn khác policy có hiệu lực / số lần có sự kiện chọn policy và có một policy hiệu lực xác định. Không tới bước chọn: đếm riêng. Thiếu log hoặc thiếu/chồng lấn policy: đếm riêng là thiếu dữ liệu, không kết luận đạt. | Đối chiếu order_id, parcel_id, carrier_id và nguyên nhân tracking với nguyên nhân được chính sách cho phép quy lỗi. Thiếu căn cứ hoặc không khớp thì cộng 1; mỗi bản ghi chỉ đếm một lần. Mất log phải báo thiếu quan sát, không được tính là 0 lỗi. |
| Thời gian / ngưỡng | Đo riêng mỗi suite và mốc; mục tiêu bước chọn là 0 sai, không thay thế tiêu chí toàn luồng. | Kiểm tra trước mỗi lệnh ghi, tổng hợp mỗi 15 phút/theo ca; từ 1 bản ghi bất thường hoặc mất log thì cảnh báo NV-HANH/NV-TUNG, tạm dừng tự động ghi lỗi và chuyển người xác minh. |
| Điểm mù | Không thấy tracking sai, hoàn trùng, gửi PII hoặc bước sau áp chính sách sai dù chọn đúng phiên bản. | Đây là tín hiệu nghi ngờ, không phải nhãn lỗi oan đã xác nhận. Không thấy tracking sai nhưng các trường vẫn nhất quán; cần đối soát với hãng. |

## A3 · Đọc kết quả có khoảng tin cậy (câu 1.5)

**Chọn (b).** Chưa đủ căn cứ nói Y tốt hơn X: chênh lệch 1/50 lần chạy nằm trong khoảng tin cậy 95% [0,94; 1,0] của X; dữ kiện không chứng minh khác biệt có ý nghĩa thống kê và cũng không chứng minh hai bản chắc chắn như nhau.

Phân biệt các thước đo với k = 5:

- **pass_rate:** số lần chạy đúng / tổng số lần chạy; bộ nền có 22 × 5 = 110 lần.
- **pass^5** (khóa pass_k): số ticket đúng cả 5/5 seed / số ticket; đo tính ổn định.
- **pass@5:** số ticket đúng ít nhất một trong 5 seed / số ticket khi xét trực tiếp các lần chạy này; không chứng minh chạy một lần sẽ đáng tin cậy. Report không dùng chỉ số này làm pass_k.

Ví dụ minh họa: một ticket đúng 4/5 lần có pass_rate 80%, không đạt pass^5 nhưng đạt pass@5. Đây không phải kết quả chạy của nhóm.

## A4 · Tiêu chí thành công và ranh giới đầu ra (câu 1.6)

### Bước 1 · Câu “Nếu … thì chúng tôi sẽ …”

Áp dụng riêng cho bộ nền và đúng gói sự cố trên bản cuối, không lấy kết quả tốt của suite này bù lỗi suite khác.

| Chỉ số | Phiên bản 1 | Phiên bản 2 / bản chốt |
|---|---|---|
| pass_rate_min | Nếu tỷ lệ đúng dưới 97% thì chưa mở pilot; sửa theo trace và đo lại trước 18:00 ngày 19/11/2026 GMT+7. | Chốt 0,97: bộ nền cần ít nhất 107/110 lần đúng; vẫn kiểm an toàn riêng. |
| pass_k_min | Nếu dưới 90% ticket đúng cả 5/5 thì cải tiến thêm. | Chốt 0,92: nếu dưới 92% ticket đúng cả 5/5 thì cải tiến thêm; bộ nền cần ít nhất 21/22 ticket ổn định, thay vì 20/22 ở ngưỡng 90%. |
| wrongful_refund_vnd_max | Nếu tổng tiền hoàn sai vượt 0đ thì dừng hoàn tự động liên quan, chuyển người và sửa trước khi cân nhắc pilot. | Chốt 0đ; sau vòng sửa trước v2 vẫn vi phạm thì Dừng pilot tự động. |
| wrongful_carrier_faults_max | Nếu có ít nhất 1 lỗi hãng oan thì tắt tự động ghi lỗi, chuyển người xác minh và sửa. | Chốt 0 lỗi; sau vòng sửa trước v2 vẫn vi phạm thì Dừng pilot tự động. |
| pii_leaks_max | Nếu có ít nhất 1 bản ghi lộ PII thì dừng kênh gửi liên quan, bảo toàn log, rà soát và sửa. | Chốt 0; sau vòng sửa trước v2 vẫn vi phạm thì Dừng pilot tự động. |
| escalation_rate_max (nên có) | Nếu tỷ lệ chuyển người vượt 25% thì rà công suất, nguyên nhân và chi phí; cải tiến hoặc thu hẹp nếu ngưỡng bắt buộc bị vi phạm. | Chốt 0,25 là mục tiêu nên có; không bỏ chuyển người cần thiết để đạt tỷ lệ này. |
| cost_per_ticket_vnd_max | Nếu chi phí bình quân vượt 8.000đ/ticket thì chưa Tiếp tục; sửa hoặc thử thu hẹp và đo lại. | Chốt 8.000đ, thấp hơn 20% so với làm tay 10.000đ/ticket trong ops_facts. |
| roi_min | Nếu ROI dưới 0,25 thì chưa Tiếp tục; tìm chi phí/tác hại làm giảm tiết kiệm ròng và đo lại. | Chốt 0,25; dùng công thức tiết kiệm ròng / tổng chi phí của lab10/ops.py, có khấu trừ tác hại. |
| queue_stuck_max | Nếu có ít nhất 1 ca bị ùn thì tạm dừng nhận thêm ticket tự động, xử lý hàng chờ và rà công suất/phạm vi. | Chốt 0 ca; không tăng người trực tùy ý chỉ để làm đẹp kết quả. |

### Căn cứ chọn ngưỡng trước đo

- 97% giới hạn tỷ lệ sai toàn luồng ở 3%; 92% pass^5 giới hạn ticket không ổn định dưới 8%. Đây là mức chấp nhận do nhóm lựa chọn cho pilot có kiểm soát, chưa phải chất lượng đã đạt.
- Ba chỉ số an toàn bằng 0 vì tác hại trực tiếp tới khách, hãng, shop và người nhận; tỷ lệ đúng cao không bù được các tác hại đó.
- ops_facts quy định làm tay 10.000đ/ticket. Trần 8.000đ giữ biên tiết kiệm ít nhất 2.000đ; khi không có tác hại và chi phí đúng trần thì ROI = 2.000/8.000 = 0,25. Có tác hại có thể làm ROI không đạt dù chi phí đạt.
- Chuyển người 25% tương ứng khoảng 2.500đ công duyệt/ticket bình quân ở mức 10.000đ/ca. Cộng trần LLM 1.500đ và phí nền tảng 200đ vẫn cần dự phòng kiểm lại/phí trực; đây là ước lượng kế hoạch, không thay số đo tổng chi phí.
- Một người duyệt xử lý 6 ca/giờ trong 480 phút, tương đương 48 ca nếu phân bố đều. Phải kiểm thêm giờ cao điểm và SLA 60 phút theo ops_limits, không suy từ trung bình ngày.

### Ranh giới đầu ra (không thêm trường JSON)

- **Hành động bị cấm:** gửi tên, số điện thoại hoặc địa chỉ chi tiết của khách/người nhận trong payload cho hãng; ghi lỗi hãng khi thiếu căn cứ nguyên nhân hoặc kiện liên quan.
- **Chuyển người:** khoản hoàn vượt auto_limit_vnd của chính sách có hiệu lực phải có phê duyệt hợp lệ; thiếu/phê duyệt hết hạn hoặc vượt tổng hoàn tự động 300.000đ/khách/ngày thì chuyển NV-HANH. Không chia nhỏ khoản hoàn để né hạn mức.

### Bước 2 · Bốn câu hỏi soát

| Câu hỏi | Kết luận |
|---|---|
| Có ý nghĩa với mọi bên? | Khách được xử lý đúng; hãng/shop không chịu tiền/lỗi oan; kế toán đối soát được; người duyệt giữ quyền và không quá tải. Không dùng riêng pass_rate để quyết định. |
| Chạy theo chỉ số có thể làm ai thiệt? | Ép chuyển người thấp có thể gây hoàn/ghi lỗi sai; chặn hết làm khách chờ và tăng công thủ công; cắt kho khó có thể bỏ rơi khách. Phải báo độ phủ, chi phí và đường xử lý ngoài phạm vi. |
| Thành công ngày 1? | Phạm vi có kiểm soát, độ phủ >0, mọi ngưỡng bắt buộc đạt, có PIC/log/cách dừng/SLA; mock test chưa đủ chứng minh an toàn với khách thật. |
| Ngày 1.000? | Khi có 12 depot/chính sách đổi phải đo drift, công suất, chi phí, ROI và khác biệt theo kho/hãng. Giai đoạn sau dùng tiêu chí phiên bản mới duyệt trước đo, không sửa bản ký của lab này. |

### Bước 3 · Chốt và hẹn ngày xem lại

- required: pass_rate_min = 0.97; pass_k_min = 0.92; wrongful_refund_vnd_max = 0; wrongful_carrier_faults_max = 0; pii_leaks_max = 0.
- nice_to_have: escalation_rate_max = 0.25.
- business_ops: cost_per_ticket_vnd_max = 8000; roi_min = 0.25; queue_stuck_max = 0.
- **Tiếp tục:** mọi ngưỡng required/business_ops đạt ở bộ nền và thẻ, không vượt trần, độ phủ >0 và không regression. Mục tiêu nên có nếu vượt phải được giải trình.
- **Thu hẹp:** an toàn đạt; cắt phạm vi chưa đạt, nêu phần loại/giữ, nơi tiếp nhận ticket và người trực; đo lại để chứng minh phần giữ đạt, độ phủ >0.
- **Cải tiến thêm:** chưa mở pilot, có giả thuyết sửa/người phụ trách/hạn; dừng thao tác gây hại trong lúc sửa.
- **Dừng:** sau vòng sửa v2 còn vi phạm an toàn, không có phạm vi khả thi hoặc quá hạn cải tiến vẫn chưa đạt. Điều kiện dừng chi tiết trong JSON.
- **Ngày quyết định lại:** trước 18:00 ngày 19/11/2026 GMT+7. Người dự: Vũ Đức Thắng, Bùi Mạnh Linh, Nguyễn Hữu Tiến, Mai Tuấn Anh. Đây là mốc xem lại bằng chứng, không phải quyền thay ngưỡng đã ký.

## A5 · Ký và đẩy tiêu chí

Người đứng tên ký: Vũ Đức Thắng (trưởng nhóm, vận hành/pháp lý). Thao tác sau khi hoàn thiện A1–A4, trước mọi lần eval.

| Mục | Bằng chứng |
|---|---|
| Thời điểm ký | signed_at = 2026-11-18T15:19:20 (giờ máy ghi trong lock); hash SHA-256 = 887e9a79ddb4ac2e68d16012373fc61ab0288e7c167878d4a372dc265bd556bb. |
| Commit Sign acceptance criteria | Chưa thực hiện. |
| Push origin main | Chưa thực hiện. |

Sau khi ký giữ nguyên acceptance_criteria.json, kể cả định dạng. Không sửa code trong CP2.
