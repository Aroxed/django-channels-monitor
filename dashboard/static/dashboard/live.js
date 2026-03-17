(function () {
  const config = window.DASHBOARD_CONFIG || {};
  const cpuValue = document.getElementById("cpu-value");
  const ramValue = document.getElementById("ram-value");
  const connectionsValue = document.getElementById("connections-value");
  const statusEl = document.getElementById("status");

  function updateUi(payload) {
    cpuValue.textContent = `${payload.cpu_percent.toFixed(1)}%`;
    ramValue.textContent = `${payload.ram_percent.toFixed(1)}%`;
    connectionsValue.textContent = `${payload.open_connections}`;
    statusEl.textContent = `Last update: ${new Date(payload.timestamp).toLocaleTimeString()}`;
  }

  function attachWebSocket() {
    const socket = new WebSocket(config.wsUrl);
    socket.onopen = function () {
      statusEl.textContent = "WebSocket connected.";
    };
    socket.onmessage = function (event) {
      const payload = JSON.parse(event.data);
      updateUi(payload);
    };
    socket.onclose = function () {
      statusEl.textContent = "WebSocket disconnected. Reconnecting...";
      setTimeout(attachWebSocket, 1500);
    };
    socket.onerror = function () {
      socket.close();
    };
  }

  function attachSse() {
    const source = new EventSource(config.sseUrl);
    source.onopen = function () {
      statusEl.textContent = "SSE connected.";
    };
    source.onmessage = function (event) {
      const payload = JSON.parse(event.data);
      updateUi(payload);
    };
    source.onerror = function () {
      statusEl.textContent = "SSE reconnecting...";
    };
  }

  if (config.transport === "sse") {
    attachSse();
  } else {
    attachWebSocket();
  }
})();
