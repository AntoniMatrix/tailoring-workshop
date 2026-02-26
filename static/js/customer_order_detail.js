/**
 * Load a single order detail for the customer and render:
 * - order header
 * - messages (non-internal)
 * - payments
 */
async function loadDetail() {
  const box = document.querySelector("#orderBox");
  const msgs = document.querySelector("#msgs");
  const payments = document.querySelector("#payments");

  try {
    const data = await apiFetch(`/api/orders/${window.ORDER_ID}/detail/`);
    const o = data.order;

    box.innerHTML = `
      <div><b>${esc(o.title)}</b></div>
      <div class="small">Status: <span class="badge">${esc(o.status_label)}</span></div>
      <div class="small">Total: ${o.total_price} | Deposit: ${o.deposit_amount}</div>
    `;

    msgs.innerHTML =
      data.messages
        .map(
          (m) => `
      <div style="margin:8px 0; padding:10px; border:1px solid #2a2f3d; border-radius:10px;">
        <div class="small"><b>${esc(m.sender)}</b> - ${new Date(m.created_at).toLocaleString("fa-IR")}</div>
        <div>${esc(m.message)}</div>
      </div>
    `
        )
        .join("") || "<div class='small'>No messages.</div>";

    payments.innerHTML =
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
 * Send a customer message to the order thread.
 */
async function sendMsg() {
  const text = document.querySelector("#msgText").value.trim();
  if (!text) return;

  try {
    await apiFetch(`/api/orders/${window.ORDER_ID}/message/`, {
      method: "POST",
      body: { message: text },
    });
    document.querySelector("#msgText").value = "";
    await loadDetail();
  } catch (e) {
    alert(e.message);
  }
}

loadDetail();