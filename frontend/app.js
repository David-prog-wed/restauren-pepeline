function getBases() {
  return {
    auth: document.getElementById("authBase").value.trim(),
    res: document.getElementById("resBase").value.trim(),
    ord: document.getElementById("ordBase").value.trim(),
  };
}

function showOutput(title, data, isError = false) {
  const output = document.getElementById("output");
  const payload =
    typeof data === "string" ? data : JSON.stringify(data, null, 2);
  output.textContent = `[${new Date().toLocaleString()}] ${title}\n\n${payload}`;
  output.className = isError ? "error" : "";
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch {
    data = { raw: text };
  }
  if (!response.ok) {
    throw new Error(
      `${response.status} ${response.statusText} - ${JSON.stringify(data)}`,
    );
  }
  return data;
}

function formDataObject(form) {
  return Object.fromEntries(new FormData(form).entries());
}

document
  .getElementById("registerForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const { auth } = getBases();
    const body = formDataObject(e.target);
    try {
      const data = await requestJson(`${auth}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      showOutput("Registro exitoso", data);
    } catch (err) {
      showOutput("Error en registro", err.message, true);
    }
  });

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const { auth } = getBases();
  const body = formDataObject(e.target);
  try {
    const data = await requestJson(`${auth}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    showOutput("Login exitoso", data);
  } catch (err) {
    showOutput("Error en login", err.message, true);
  }
});

document
  .getElementById("availabilityForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const { res } = getBases();
    const body = formDataObject(e.target);
    const query = new URLSearchParams({
      date: body.date,
      time: body.time,
      party_size: body.party_size,
    });
    try {
      const data = await requestJson(
        `${res}/api/reservations/availability?${query.toString()}`,
      );
      showOutput("Disponibilidad", data);
    } catch (err) {
      showOutput("Error en disponibilidad", err.message, true);
    }
  });

document
  .getElementById("createReservationForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const { res } = getBases();
    const body = formDataObject(e.target);
    body.customer_id = Number(body.customer_id);
    body.party_size = Number(body.party_size);
    try {
      const data = await requestJson(`${res}/api/reservations/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      showOutput("Reserva creada", data);
    } catch (err) {
      showOutput("Error al crear reserva", err.message, true);
    }
  });

document
  .getElementById("getReservationForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const { res } = getBases();
    const { rid } = formDataObject(e.target);
    try {
      const data = await requestJson(
        `${res}/api/reservations/${encodeURIComponent(rid)}`,
      );
      showOutput("Reserva consultada", data);
    } catch (err) {
      showOutput("Error al consultar reserva", err.message, true);
    }
  });

document
  .getElementById("cancelReservationForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const { res } = getBases();
    const { rid } = formDataObject(e.target);
    try {
      const data = await requestJson(
        `${res}/api/reservations/${encodeURIComponent(rid)}/cancel`,
        {
          method: "PUT",
        },
      );
      showOutput("Reserva cancelada", data);
    } catch (err) {
      showOutput("Error al cancelar reserva", err.message, true);
    }
  });

document.getElementById("menuForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const { ord } = getBases();
  try {
    const data = await requestJson(`${ord}/api/menu/`);
    showOutput("Menú", data);
  } catch (err) {
    showOutput("Error al obtener menú", err.message, true);
  }
});

document
  .getElementById("createOrderForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const { ord } = getBases();
    const body = formDataObject(e.target);
    let items;
    try {
      items = JSON.parse(body.items);
    } catch {
      showOutput(
        "Error de formato",
        "El campo Items debe ser un JSON válido",
        true,
      );
      return;
    }
    const payload = {
      customer_id: Number(body.customer_id),
      items,
    };
    try {
      const data = await requestJson(`${ord}/api/orders/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      showOutput("Pedido creado", data);
    } catch (err) {
      showOutput("Error al crear pedido", err.message, true);
    }
  });

document
  .getElementById("confirmOrderForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const { ord } = getBases();
    const { oid } = formDataObject(e.target);
    try {
      const data = await requestJson(
        `${ord}/api/orders/${encodeURIComponent(oid)}/confirm`,
        {
          method: "PUT",
        },
      );
      showOutput("Pedido confirmado", data);
    } catch (err) {
      showOutput("Error al confirmar pedido", err.message, true);
    }
  });

document
  .getElementById("getOrderForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const { ord } = getBases();
    const { oid } = formDataObject(e.target);
    try {
      const data = await requestJson(
        `${ord}/api/orders/${encodeURIComponent(oid)}`,
      );
      showOutput("Pedido consultado", data);
    } catch (err) {
      showOutput("Error al consultar pedido", err.message, true);
    }
  });
