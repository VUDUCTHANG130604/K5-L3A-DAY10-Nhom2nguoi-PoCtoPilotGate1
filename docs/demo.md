# Demo và phản biện — nhóm 4 người, thẻ S8

Kịch bản và lệnh dưới đây đã được chạy trên máy; output gốc ở `docs/demo-evidence/`. Đây không phải xác nhận đã demo trước Coach. Giữ nguyên criteria, snapshot và cấu hình cuối khi trình bày.

## Vũ Đức Thắng — vấn đề, vận hành và kết luận

Trình bày: trợ lý dùng mã duyệt không đúng phạm vi khiến trưởng ca phải đứng tên giải trình. Nhân viên chuyển sang kiểm tay 100%, tạo 36 ca ùn, chờ tối đa 216 phút, chi phí 11.325đ/ticket. B6 đã dự báo từng rủi ro nhưng cổng vòng 1 chưa xử lý chuỗi dùng duyệt sai → mất lòng tin → kiểm toàn bộ → ùn và tăng công.

Sau sửa: giữ một người duyệt, công suất 6 ca/giờ, mẫu 10%, đúng NV-HANH và có ghi chú. Khi điều kiện lòng tin đạt, mô phỏng không còn ca ùn, chờ tối đa 5 phút. NV-TUNG điều phối/dừng, NV-HANH duyệt, NV-OANH đối soát. Cảnh báo/quy trình này chưa phải hệ thống nhắn tin tự động đã triển khai thật.

Quyết định hồ sơ: Cải tiến thêm, chưa mở pilot thật. Các số chất lượng/chi phí đã đạt nhưng toàn vẹn còn thiếu gói chính thức; không dùng kết quả visible xanh để bỏ qua điều kiện này.

## Bùi Mạnh Linh — cổng và ca đối chứng

Chỉ ba lần chạy cùng ticket S8-02: base, prepared, after. Base/prepared dùng A-2802 hết hạn để hoàn 230.000đ; after chuyển người trước khi ghi tiền. Cổng kiểm trạng thái valid, đúng ticket/đơn/khách/người duyệt, ngày hết hạn và max_vnd. Không viết nhánh theo mã ticket.

```powershell
python -m lab10.trace --suite S8 --stage base --ticket S8-02 --seed 11
python -m lab10.trace --suite S8 --stage prepared --ticket S8-02 --seed 11
python -m lab10.trace --suite S8 --stage after --ticket S8-02 --seed 11
python -m lab10.trace --suite S8 --stage after --ticket S8-05 --seed 11
python -m lab10.trace --suite S8 --stage after --ticket S8-43 --seed 11
```

S8-05 chứng minh không chặn hết: mã hợp lệ vẫn hoàn 230.000đ. Với khách C-16, S8-40..42 đã hoàn tổng 282.000đ; khoản tiếp theo 104.000đ sẽ vượt 300.000đ/ngày nên S8-43 chuyển người. Không đổi trần ngày để chỉ khớp bộ thử.

Giới hạn cần nói: gate kiểm dữ liệu hiện có trong mô hình tuần tự; chưa chứng minh dữ liệu thu hồi cập nhật tức thời, idempotency đầy đủ hoặc kiểm/ghi nguyên tử khi nhiều yêu cầu đồng thời.

## Nguyễn Hữu Tiến — bằng chứng đo, hồi quy và monitor

Dùng `submission/runs/grade-report.md` và JSON tương ứng. Grade cuối hiện có: `R-S8-grade-20261118-205236-536bf2`, code_hash `536bf24a371d...`.

- S8 after 260/260 lượt đạt; bộ nền after 110/110, không ca mới hỏng.
- Hoàn sai, lỗi hãng oan, PII bằng 0; độ phủ 100%.
- `approval_usage_rate`: nền 0.045455, S8 0.115385. Đo việc đề xuất/dùng mã, không kết luận mã sai. Event xuất hiện trước gate nên giá trị after có thể không giảm dù giao dịch sai đã bị chặn.
- `recheck_rate`: S8 từ 1.0 xuống 0.076923; đây là 4/52 ticket bị kiểm lại. Khác với cấu hình 10% của các quyết định tự động còn lại; không lẫn mẫu số.
- Visible/regression/monitor đạt. Hidden chưa có trên máy. Integrity còn false vì thiếu 28 file, không phải đã qua toàn bộ chấm.

Nếu chạy lại grade trong demo, phải giữ output/mã mới và gom bài lại. Không giả vờ mã mới là lần chạy trước khi nhận thẻ.

## Mai Tuấn Anh — hiệu quả và quyết định

Trình bày so prepared → after: 11.325đ → 2.952đ/ticket, ROI -2.44 → 2.39; công kiểm tay giảm, một người trực giữ nguyên. Bộ nền 4.456đ/ticket, ROI 1.24. Chi phí tổng khác tiền máy tối đa 1.500đ/ticket. ROI = tiết kiệm ròng / tổng chi phí; không phải phần trăm trên giá làm tay.

Phân khúc cần nói rõ: S8 DN đắt nhất sau sửa 3.200đ/ticket vẫn dưới ngưỡng tổng chi phí; nhóm `?` của bộ nền 10.359đ/ticket còn chưa có hiệu quả riêng, phải xác minh nguồn/kênh tiếp nhận trước pilot, không dùng an toàn để bù chi phí.

## Câu hỏi có thể gặp

| Câu hỏi | Cách trả lời có căn cứ |
|---|---|
| Vì sao không tăng nhiều người duyệt? | Có thể giảm chờ nhưng không sửa lỗi dùng duyệt sai và tăng phí trực. Bản sửa giữ 1 người, xử lý nguyên nhân, đo lại SLA/ROI. |
| Vì sao mọi số đã đạt mà chưa Tiếp tục? | Integrity là điều kiện riêng để bài qua. Thiếu gói chính thức thì chưa nghiệm thu toàn vẹn; quyết định Cải tiến thêm có người phụ trách và hạn. |
| 6.845.000đ có vượt ngân sách ngày 2 triệu không? | Đây là tổng hoàn sai qua 5 seed, không phải tổng tự động của một ngày. Phải đối chiếu chỉ số/ngày; không trộn mẫu số. |
| Chỉ đặt mẫu 10% có làm hàng chờ giảm không? | Không. Khi còn khoản dùng duyệt sai, mô hình ép kiểm 100%. Chỉ giảm khi đồng thời đủ điều kiện lòng tin. |
| Có bảo đảm không lỗi ngoài lab? | Không. Bảo đảm chỉ theo dữ liệu/luồng đã thử; dữ liệu trễ, race, kiểm tay ngoài log và tải đột biến là rủi ro còn mở. |
| Chứng minh không chặn hết thế nào? | Coverage=1, S8-05 hợp lệ vẫn được hoàn; các ca không đủ quyền chuyển người, không biến scope thành 0. |

## Sau demo

Nếu không đổi code/config thì giữ bộ nộp đã kiểm. Nếu đổi thử, trả về đúng bản đã chọn, chạy grade rồi collect lại; kiểm tra code_hash, signatures và manifest. Mỗi thành viên tự nộp link repo trên LMS; các tài liệu này không phải bằng chứng đã thực hiện việc đó.
