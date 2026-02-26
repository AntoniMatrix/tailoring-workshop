/**
 * Read a cookie by name (used for CSRF token).
 */
function getCookie(name) {
  const m = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return m ? decodeURIComponent(m[2]) : "";
}

/**
 * Lightweight wrapper over fetch() for JSON APIs.
 * - Adds CSRF token automatically for non-GET requests
 * - Throws Error with a human-readable message on non-2xx
 */
async function apiFetch(url, { method = "GET", body = null } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (method !== "GET") headers["X-CSRFToken"] = getCookie("csrftoken");

  const res = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }

  if (!res.ok) {
    const msg = data && data.error ? data.error : "Server request failed";
    throw new Error(msg);
  }
  return data;
}

/**
 * Basic HTML escape to prevent injection when rendering strings into innerHTML.
 */
function esc(s) {
  return (s ?? "")
    .toString()
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}