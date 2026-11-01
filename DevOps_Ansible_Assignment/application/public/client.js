// ShalaConnect Live Health Telemetry Poller (Java Spring Boot Backend)
document.addEventListener('DOMContentLoaded', () => {
  const uptimeEl = document.getElementById('uptime-val');
  const memValEl = document.getElementById('mem-val');
  const memPctEl = document.getElementById('mem-pct');
  const platformEl = document.getElementById('platform-val');
  const healthJsonEl = document.getElementById('health-json');
  const btnRefresh = document.getElementById('btn-refresh');

  async function fetchTelemetry() {
    try {
      const res = await fetch('/api/health');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      // Update UI metrics
      uptimeEl.textContent = `${data.uptime_seconds}s`;
      memValEl.textContent = `${data.memory.used_mb} MB / ${data.memory.total_mb} MB`;
      memPctEl.textContent = `JVM Free Heap: ${data.memory.free_mb} MB`;
      platformEl.textContent = `${data.runtime.java_version} (${data.runtime.framework})`;

      // Pretty print JSON response
      healthJsonEl.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      console.error('Failed to query /api/health:', err);
      healthJsonEl.textContent = `Error fetching telemetry: ${err.message}`;
    }
  }

  // Initial fetch and 5s polling interval
  fetchTelemetry();
  setInterval(fetchTelemetry, 5000);

  if (btnRefresh) {
    btnRefresh.addEventListener('click', (e) => {
      e.preventDefault();
      fetchTelemetry();
    });
  }
});
