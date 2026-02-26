/**
 * Load all orders for staff and render list.
 */
async function loadStaffOrders() {
  const box = document.querySelector("#ordersList");
  try {
    const data = await apiFetch("/api/orders/staff/list/");
    box.innerHTML =
      data.orders
        .map(
          (o) => `
      <div class="card" style="margin-bottom:10px">
        <div><b>#${o.id}</b> - ${esc(o.title)}</div>
        <div class="small">
          Customer: ${esc(o.customer)} |
          Status: <span class="badge">${esc(o.status_label)}</span> |
          Total: ${o.total_price}
        </div>
        <div style="margin-top:10px">
          <a class="btn secondary" href="/panel/orders/${o.id}/">Manage</a>
        </div>
      </div>
    `
        )
        .join("") || "<div class='small'>No orders.</div>";
  } catch (e) {
    box.innerHTML = `<div class="error">${esc(e.message)}</div>`;
  }
}

loadStaffOrders();