/**
 * Load full order details for staff and render:
 * - order header
 * - status/pricing controls (UI may still show; API enforces permissions)
 * - internal notes/messages
 * - payments
 */
async function loadStaffDetail() {
  const box = document.querySelector("#orderBox");
  const msgs = document.querySelector("#msgs");
  const pays = document.querySelector("#payments");

  try {
    const data = await apiFetch(`/api/orders/staff/${window.ORDER_ID}/detail/`);
    const o = data.order;

    box.innerHTML = `
      <div><b>${esc(o.title)}</b></div>
      <div class="small">Customer: ${esc(o.customer)}</div>
      <div class="small">Status: <span class="badge">${esc(o.status_label)}</span></div>
      <div class="small">Total: ${o.total_price} | Deposit: ${o.deposit_amount}</div>
      <div class="small">Capabilities:
        status=${data.can_change_status} |
        pricing=${data.can_set_pricing} |
        financial=${data.can_view_financial}
      </div>
    `;

    document.querySelector("#statusSelect").value = o.status;
    document.querySelector("#total_price").value = o.total_price;
    document.querySelector("#deposit_amount").value = o.deposit_amount;

    msgs.innerHTML =
      data.messages
        .map(
          (m) => `
      <div style="margin:8px 0; padding:10px; border:1px solid #2a2f3d; border-radius:10px;">
        <div class="small">
          <b>${esc(m.sender)}</b> - ${new Date(m.created_at).toLocaleString("fa-IR")}
          ${m.is_internal ? "<span class='badge'>Internal</span>" : "<span class='badge'>Customer</span>"}
        </div>
        <div>${esc(m.message)}</div>
      </div>
    `
        )
        .join("") || "<div class='small'>No messages.</div>";

    pays.innerHTML =
      data.payments
        .map(
          (p) => `
      <div style="margin:8px 0; padding:10px; border:1px solid #2a2f3d; border-radius:10px;">
        <div><b>${p.amount}</b> - <span class="badge">${esc(p.status_label)}</span></div>
        <div class="small">${new Date(p.created_at).toLocaleString("fa-IR")}</div>
      </div>
    `
        )
        .join("") || "<div class='small'>No payments.</div>";
  } catch (e) {
    box.innerHTML = `<div class="error">${esc(e.message)}</div>`;
  }
}

/**
 * Change order status (API enforces permission).
 */
async function changeStatus() {
  try {
    const status = document.querySelector("#statusSelect").value;
    await apiFetch(`/api/orders/staff/${window.ORDER_ID}/status/`, {
      method: "POST",
      body: { status },
    });
    await loadStaffDetail();
    alert("Status updated.");
  } catch (e) {
    alert(e.message);
  }
}

/**
 * Update pricing fields (API enforces permission).
 */
async function setPricing() {
  try {
    const total_price = Number(document.querySelector("#total_price").value || 0);
    const deposit_amount = Number(document.querySelector("#deposit_amount").value || 0);
    await apiFetch(`/api/orders/staff/${window.ORDER_ID}/pricing/`, {
      method: "POST",
      body: { total_price, deposit_amount },
    });
    await loadStaffDetail();
    alert("Pricing updated.");
  } catch (e) {
    alert(e.message);
  }
}

/**
 * Add an internal note for staff (audit trail).
 */
async function addNote() {
  try {
    const message = document.querySelector("#noteText").value.trim();
    if (!message) return;

    await apiFetch(`/api/orders/staff/${window.ORDER_ID}/note/`, {
      method: "POST",
      body: { message },
    });
    document.querySelector("#noteText").value = "";
    await loadStaffDetail();
  } catch (e) {
    alert(e.message);
  }
}

/**
 * Add a payment record (API enforces financial permission).
 */
async function addPayment() {
  try {
    const amount = Number(document.querySelector("#pay_amount").value || 0);
    const method = document.querySelector("#pay_method").value.trim() || "card";
    const status = document.querySelector("#pay_status").value;

    await apiFetch(`/api/orders/staff/${window.ORDER_ID}/payment/`, {
      method: "POST",
      body: { amount, method, status },
    });
    await loadStaffDetail();
    alert("Payment added.");
  } catch (e) {
    alert(e.message);
  }
}

loadStaffDetail();