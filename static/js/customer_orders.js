/**
 * Load current user's orders and render them into the page.
 */
async function loadOrders() {
  const box = document.querySelector("#ordersList");
  try {
    const data = await apiFetch("/api/orders/mine/");

    if (!data.orders.length) {
      box.innerHTML = "<div class='small'>No orders yet.</div>";
      return;
    }

    box.innerHTML = data.orders
      .map(
        (o) => `
      <div class="card" style="margin-bottom:10px">
        <div><b>#${o.id}</b> - ${esc(o.title)}</div>
        <div class="small">
          Status: <span class="badge">${esc(o.status_label)}</span> |
          Total: ${o.total_price} |
          Deposit: ${o.deposit_amount}
        </div>
        <div style="margin-top:10px">
          <a class="btn secondary" href="/orders/${o.id}/">Details</a>
        </div>
      </div>
    `
      )
      .join("");
  } catch (e) {
    box.innerHTML = `<div class="error">${esc(e.message)}</div>`;
  }
}

/**
 * Create a new order using a simple MVP form (1 item).
 */
async function createOrder() {
  const title = document.querySelector("#title").value.trim();
  const item = {
    product_type: document.querySelector("#product_type").value.trim(),
    qty: Number(document.querySelector("#qty").value || 1),
    size_range: document.querySelector("#size_range").value.trim(),
    fabric_type: document.querySelector("#fabric_type").value.trim(),
    notes: document.querySelector("#notes").value.trim(),
  };

  try {
    const data = await apiFetch("/api/orders/create/", {
      method: "POST",
      body: { title, items: [item] },
    });

    alert("Order created. ID: " + data.order_id);
    location.href = "/orders/" + data.order_id + "/";
  } catch (e) {
    alert(e.message);
  }
}

loadOrders();