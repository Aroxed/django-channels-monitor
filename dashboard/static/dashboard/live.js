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

  attachSse();
})();
