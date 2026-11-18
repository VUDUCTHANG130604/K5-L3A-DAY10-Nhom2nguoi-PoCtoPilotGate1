# Bổ sung hồ sơ CP3 — ngày 18/11/2026

Tài liệu tổng hợp sau khi nhóm đã nhận S8. Không phải biên bản viết trước khi biết thẻ; không thay đổi tiêu chí, snapshot vòng 1 hoặc quyết định v1 ở B8.

## Đã có bằng chứng

- Tiêu chí đã ký: commit `395b881`, hash tiêu chí `887e9a79`; kiểm tra hash và lịch sử ký hợp lệ.
- Checkpoint: `config/round1.lock`, `lab10/guards_round1.py`, `config/operating_gates.round1.json`; trạng thái hợp lệ, hash tổng `21ef0483`, taken_at `2026-11-18T16:27:53`.
- B0 đã bổ sung số liệu từ các report thực có, giữ nguyên note gốc và ghi rõ hạn chế về thí nghiệm một thay đổi.
- B1–B2: report baseline `R-base-before-20261118-153905-bde05c` từ máy thành viên, đủ 110 trace; `T-002@55` hoàn sai 20.000đ và ghi 1 lỗi oan.
- B3–B6 đã có nội dung. Nhóm đã xác nhận ba ưu tiên pre-mortem; checklist vẫn giữ Chưa đối với điều kiện chưa được kiểm chứng.
- B7.1–B7.2 có ba cổng và quy tắc giữ bộ kiểm tra; B7.3 có hai ticket hiểm và kết quả được ghi, ticket 1 có output terminal do người dùng cung cấp.
- B7.4: config hiện tại có business, đã đính chính cách hiểu ROI trong phiếu. Ngân sách máy 1.500đ khác ngưỡng tổng chi phí 8.000đ trong tiêu chí.
- B7.5–B7.6 có operations/legal và runbook: PIC NV-TUNG, approver NV-HANH, 1 người/6 ca mỗi giờ, SLA 60 phút, ghi chú bật, kiểm mẫu 10%.
- B8 đã có quyết định v1 Tiếp tục, PIC và thời điểm xem lại; giữ nguyên bản lịch sử, chưa đánh dấu đã đối chiếu đủ vì thiếu report gốc.

## Bằng chứng cần nhận từ người chạy

| Mã lần chạy | Được trích ở đâu | Cần bổ sung |
|---|---|---|
| R-base-after-20261118-154301-d8c618 | B7.1 | Thư mục report.json/traces và dòng journal nguyên gốc |
| R-base-before-20261118-161648-0db83f | B8 | Thư mục report.json/traces và dòng journal nguyên gốc |
| R-base-prepared-20261118-163302-79c1d8 | B8 | Thư mục report.json/traces và dòng journal nguyên gốc; sau đối chiếu mới bổ sung số vào dòng prepared B0 |
| R-base-before-20261118-153905-bde05c | B0–B1 | Report/110 trace đã có; còn thiếu dòng journal nguyên gốc từ máy người chạy |

Gộp nhật ký theo run_id, tránh trùng và giữ nội dung nguyên gốc. Nếu cùng run_id có hai nội dung khác nhau thì giữ nguồn riêng để đối chiếu, không tự chọn/xóa. Không tái tạo journal từ report hoặc chỉnh timestamp nhằm hợp thức hóa thứ tự.

## Các giới hạn phải giữ rõ

1. Bản chốt `operating_gates.round1.json` vẫn để `business.daily_refund_cap_vnd`, `cost_budget_per_ticket_vnd`, `roi_min` là null. Config hiện tại đã điền là trạng thái khác; không sửa snapshot/lock hoặc tuyên bố các trần hiện tại đã tồn tại khi chốt.
2. R-after 16:03 đạt bộ nền nhưng không thay thế report prepared 16:33 đang được B8 viện dẫn. Các report lịch sử không tự chứng minh trạng thái code hiện tại.
3. Các lần đánh giá hiện có chưa chứng minh từng lần chỉ đổi một yếu tố; B0 ghi đúng phạm vi bằng chứng. Không tạo thêm thử nghiệm sau S8 rồi gọi là thử nghiệm trước khi biết thẻ.
4. B3 còn cần Mai Tuấn Anh rà lại schema: ticket ở `data/tickets.jsonl`; `auto_limit_vnd` và `fault_causes` là khóa trực tiếp của policy, không nằm trong `late`; phê duyệt cần cả ticket/đơn/khách, hạn mức, trạng thái, thời hạn. Các giả định về người cập nhật dữ liệu thực phải phân biệt với dữ kiện mock.
5. Kiểm thử hai lời khai không thay thế thử chỉ thị giả mạo/phê duyệt không hợp lệ; chưa có thử tải gấp ba và chứng minh chống ghi lặp.
6. Báo cáo S8 grade `R-S8-grade-20261118-170453-79c1d8` có integrity=false. Bản round1 vẫn hợp lệ; integrity còn liệt kê nhiều file khóa và gói thẻ thiếu/khác manifest. Đây là vấn đề riêng cần kiểm tra nguồn gói và định dạng byte với bản chính thức; không sửa manifest/hash hoặc snapshot để bỏ qua. Chưa kết luận nguyên nhân là chỉnh sửa nội dung hay khác dòng kết thúc.

## Lệnh đo bổ sung nếu không còn report gốc

Chỉ dùng khi nhóm cần một phép đo mới của bản prepared đã khóa; lần chạy này diễn ra sau khi nhận S8, không thay thế bằng chứng lịch sử của B8:

```powershell
python -m lab10.eval --suite base --stage prepared --note "Đo bổ sung bản prepared đã khóa sau khi nhận S8; không thay report lịch sử B8"
```

Sau khi có mã mới, đối chiếu bằng:

```powershell
python -m lab10.gate --run runs/<ma-moi>/report.json
```

Không chạy lại checkpoint, không đổi criteria, round1.lock hoặc hai snapshot. Mã phép đo mới phải được ghi với đúng thời điểm thực tế ở phần bổ sung.

## Bàn giao

- Nguyễn Hữu Tiến: nhận report/journal các máy, đối chiếu B0/B7.1/B8 và số prepared.
- Mai Tuấn Anh: rà B3/B7.4 và sự khác biệt business hiện tại với snapshot; giải thích quyết định trên đúng phạm vi bằng chứng.
- Bùi Mạnh Linh: giữ snapshot, bổ sung bằng chứng kiểm quyền hạn/ghi lặp ở vòng 2 theo nguyên nhân chung.
- Vũ Đức Thắng: tổng hợp thiếu sót, giữ B8 lịch sử, cập nhật checklist vòng 2 ở C11; không đánh dấu CP3 đủ bằng chứng cho tới khi các report được đối chiếu hoặc giới hạn được giải trình rõ.

## Cập nhật sau hoàn thiện hồ sơ

Đã có phép đo prepared bổ sung `R-base-prepared-20261118-204525-c522a1` và grade `R-S8-grade-20261118-205236-536bf2`. Một số ghi chú “chưa chạy” ở trên là trạng thái lần rà trước, xem docs/evidence-status.md để biết kết quả hiện tại và tham chiếu lịch sử còn thiếu. Giữ nguyên snapshot/B8.
