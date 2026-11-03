// ==============================================================================
// ShalaConnect Telemetry Poller & Real-time Metrics Client
// Author: Yash Janardan Sabale | PRN: 202301040087 | MITAOE Pune
// ==============================================================================

async function fetchTelemetry() {
    try {
        const [healthRes, metricsRes] = await Promise.all([
            fetch('/api/health'),
            fetch('/api/metrics')
        ]);

        if (healthRes.ok) {
            const health = await healthRes.json();
            const uptimeElem = document.getElementById('uptimeDisplay');
            const heapElem = document.getElementById('heapDisplay');
            const requestsElem = document.getElementById('requestsDisplay');
            const podElem = document.getElementById('podNameDisplay');
            const nsElem = document.getElementById('namespaceDisplay');

            if (uptimeElem) uptimeElem.innerText = formatUptime(health.uptimeSeconds);
            if (heapElem) heapElem.innerText = health.heapMemoryUsedMB + ' MB';
            if (requestsElem) requestsElem.innerText = health.totalRequestsProcessed;
            if (podElem && health.podName) podElem.innerText = health.podName;
            if (nsElem && health.namespace) nsElem.innerText = health.namespace;
        }

        if (metricsRes.ok) {
            const metrics = await metricsRes.json();
            const threadsElem = document.getElementById('threadsDisplay');
            if (threadsElem) threadsElem.innerText = metrics.liveThreadCount + ' active';
        }
    } catch (err) {
        console.warn("Telemetry fetch error (probing local container):", err);
    }
}

function formatUptime(seconds) {
    if (!seconds || seconds < 60) return (seconds || 0) + 's';
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    if (m < 60) return m + 'm ' + s + 's';
    const h = Math.floor(m / 60);
    return h + 'h ' + (m % 60) + 'm';
}

// Initial fetch and 3-second periodic poll
fetchTelemetry();
setInterval(fetchTelemetry, 3000);
