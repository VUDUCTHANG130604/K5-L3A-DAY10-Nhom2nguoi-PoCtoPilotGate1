"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action["tool"]
    if tool == "send_reply":
        return Verdict.allow()

    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không tìm thấy chính sách có hiệu lực")

    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order is None or not order.get("parcels"):
            return Verdict.escalate("không tìm thấy đơn để xác minh quyền hoàn")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay = H.db_delay_days(parcel, ctx.as_of)
        allowed = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        if allowed <= 0:
            return Verdict.deny("tracking và chính sách không xác nhận quyền hoàn")
        if action.get("payer") != "LOGIX":
            return Verdict.escalate("người trả tiền không phải LogiX; cần người duyệt")
        if action.get("amount_vnd", 0) > allowed:
            return Verdict.modify("giới hạn theo tracking và chính sách hiện hành",
                                  amount_vnd=allowed, basis="policy")

    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        parcel = next((p for p in (order or {}).get("parcels", [])
                       if p.get("parcel_id") == action.get("parcel_id")), None)
        if parcel is None:
            return Verdict.deny("không tìm thấy kiện hàng trong nguồn tracking")
        delay = H.db_delay_days(parcel, ctx.as_of)
        if (action.get("carrier_id") != parcel.get("carrier_id")
                or action.get("delay_days") != delay
                or not H.carrier_at_fault(policy, parcel, delay)):
            return Verdict.deny("tracking không xác nhận lỗi của hãng này")

    if tool == "notify_carrier":
        allowed_fields = set(policy.get("carrier_notice_fields", []))
        payload = action.get("payload")
        if not isinstance(payload, dict) or not allowed_fields:
            return Verdict.escalate("không xác minh được trường dữ liệu được phép gửi hãng")
        safe_payload = {key: value for key, value in payload.items() if key in allowed_fields}
        if safe_payload != payload:
            ctx.log("carrier_payload_minimized", removed=sorted(set(payload) - set(safe_payload)))
            return Verdict.modify("chỉ gửi các trường được chính sách cho phép",
                                  payload=safe_payload)

    return Verdict.allow()
