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


def _approval_problem(ctx, approval_id, action, order, amount_vnd):
    approvals = ctx.tools.lookup_approvals(approval_id=approval_id)
    if len(approvals) != 1:
        return "không tìm thấy đúng một mã phê duyệt"

    approval = approvals[0]
    if approval.get("status") != "valid":
        return "mã phê duyệt không còn hiệu lực"
    if (action.get("ticket_id") != ctx.ticket.get("ticket_id")
            or approval.get("ticket_id") != ctx.ticket.get("ticket_id")
            or action.get("order_id") != ctx.ticket.get("order_id")
            or approval.get("order_id") != action.get("order_id")
            or approval.get("customer_id") != order.get("customer_id")
            or order.get("customer_id") != ctx.ticket.get("customer_id")):
        return "mã phê duyệt không khớp ticket, đơn hoặc khách hàng"
    approver_id = ctx.gates.get("operations", {}).get("approver_id")
    if approver_id and approval.get("approver_id") != approver_id:
        return "mã phê duyệt không do người duyệt được chỉ định cấp"
    max_vnd = approval.get("max_vnd")
    if isinstance(max_vnd, bool) or not isinstance(max_vnd, int) or max_vnd < amount_vnd:
        return "số tiền vượt hạn mức của mã phê duyệt"
    try:
        expired = H.d(approval["expires_at"]) < H.d(ctx.as_of)
    except (KeyError, TypeError, ValueError):
        return "ngày hết hạn của mã phê duyệt thiếu hoặc không hợp lệ"
    if expired:
        return "mã phê duyệt đã hết hạn"
    return None


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
        if (action.get("order_id") != ctx.ticket.get("order_id")
                or order.get("customer_id") != ctx.ticket.get("customer_id")):
            return Verdict.escalate("đơn không khớp ticket hoặc chủ đơn")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay = H.db_delay_days(parcel, ctx.as_of)
        allowed = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        if allowed <= 0:
            return Verdict.deny("tracking và chính sách không xác nhận quyền hoàn")
        requested = action.get("amount_vnd")
        if isinstance(requested, bool) or not isinstance(requested, int) or requested <= 0:
            return Verdict.escalate("số tiền hoàn không hợp lệ")
        if action.get("payer") != "LOGIX":
            return Verdict.escalate("người trả tiền không phải LogiX; cần người duyệt")
        amount = min(requested, allowed)
        changes = {}
        if amount != requested:
            changes.update(amount_vnd=amount, basis="policy")

        auto_limit = policy.get("auto_limit_vnd")
        if isinstance(auto_limit, bool) or not isinstance(auto_limit, int) or auto_limit < 0:
            return Verdict.escalate("không xác minh được hạn mức hoàn tự động")

        approval_id = action.get("approval_id")
        if approval_id:
            problem = _approval_problem(ctx, approval_id, action, order, amount)
            if problem:
                ctx.log("approval_rejected", approval_id=approval_id, reason=problem)
                return Verdict.escalate("phê duyệt không hợp lệ: " + problem)
        elif amount > auto_limit:
            return Verdict.escalate("hoàn vượt hạn mức tự động nhưng không có mã phê duyệt")
        else:
            customer_limit = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
            if (isinstance(customer_limit, bool) or not isinstance(customer_limit, int)
                    or customer_limit < 0):
                return Verdict.escalate("không xác minh được trần hoàn tự động mỗi khách mỗi ngày")
            refunded_today = sum(
                row["amount_vnd"]
                for row in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                if not row.get("approval_id")
            )
            if refunded_today + amount > customer_limit:
                ctx.log("customer_daily_refund_cap", customer_id=order["customer_id"],
                        limit_vnd=customer_limit, refunded_today_vnd=refunded_today, asked_vnd=amount)
                return Verdict.escalate("vượt trần hoàn tự động tích lũy mỗi khách trong ngày")
        if changes:
            return Verdict.modify("giới hạn theo tracking và chính sách hiện hành", **changes)

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
