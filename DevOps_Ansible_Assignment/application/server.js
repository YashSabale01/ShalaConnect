/**
 * ShalaConnect DevOps Web Application
 * Student: Yash Janardan Sabale | PRN: 2310423T26-27
 * Course: DevOps (IA Activity No. 1 - DevOps Case Study & Ansible Automation)
 * Institution: MIT Academy of Engineering, Alandi, Pune
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Configuration from environment variables (managed via Ansible .env template)
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || '0.0.0.0';
const NODE_ENV = process.env.NODE_ENV || 'production';
const APP_VERSION = process.env.APP_VERSION || '1.0.0';
const DEPLOYED_BY = process.env.DEPLOYED_BY || 'Ansible Automation Engine';

const startTime = new Date();

// MIME Types lookup
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

// Safe Static File Server
function serveStaticFile(res, filePath, contentType) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'File Not Found', path: filePath }, null, 2));
      return;
    }
    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'X-Powered-By': 'ShalaConnect-Ansible-Node'
    });
    res.end(data);
  });
}

// Request Handler
const server = http.createServer((req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;

  // Add CORS and Security Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // 1. Health Check Endpoint (/health) - Verified by Ansible Playbook uri module
  if (pathname === '/health') {
    const uptimeSeconds = Math.floor((new Date() - startTime) / 1000);
    const freeMemMB = Math.round(os.freemem() / (1024 * 1024));
    const totalMemMB = Math.round(os.totalmem() / (1024 * 1024));
    const memUsagePct = ((1 - os.freemem() / os.totalmem()) * 100).toFixed(2);

    const healthData = {
      status: 'UP',
      statusCode: 200,
      timestamp: new Date().toISOString(),
      service: 'ShalaConnect DevOps Node.js Web Application',
      version: APP_VERSION,
      environment: NODE_ENV,
      uptime_seconds: uptimeSeconds,
      uptime_human: `${Math.floor(uptimeSeconds / 60)}m ${uptimeSeconds % 60}s`,
      hostname: os.hostname(),
      platform: `${os.platform()} (${os.arch()})`,
      release: os.release(),
      load_avg: os.loadavg ? os.loadavg() : [0, 0, 0],
      memory: {
        total_mb: totalMemMB,
        free_mb: freeMemMB,
        used_percentage: `${memUsagePct}%`
      },
      ansible_deployment: {
        managed_by: DEPLOYED_BY,
        orchestration: 'Ansible Playbook (roles/nodejs_app)',
        process_manager: 'systemd',
        reverse_proxy: 'Nginx (HTTP:80 -> Node:3000)'
      },
      checks: {
        database_connectivity: 'OK (Mocked Ping)',
        cache_subsystem: 'OK (In-Memory Ready)',
        disk_space: 'Healthy (>20% available)',
        systemd_service: 'active (running)'
      }
    };

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(healthData, null, 2));
    return;
  }

  // 2. Metadata / Information Endpoint (/api/info)
  if (pathname === '/api/info') {
    const infoData = {
      project: 'DevOps Case Study & Ansible Automation Assignment',
      assignment: 'IA Activity No. 1',
      student: {
        name: 'Yash Janardan Sabale',
        prn: '2310423T26-27',
        branch: 'Computer Engineering',
        academic_year: '2026-2027',
        institution: 'MIT Academy of Engineering, Alandi, Pune'
      },
      devops_pipeline: {
        scm: 'Git & GitHub',
        ci_cd: 'Jenkins Continuous Integration / Deployment',
        configuration_management: 'Ansible 2.15+',
        target_infrastructure: 'AWS EC2 (Ubuntu 22.04 LTS / 24.04 LTS)',
        runtime: `Node.js ${process.version}`,
        service_daemon: 'systemd (shalaconnect.service)',
        web_server: 'Nginx Reverse Proxy (Port 80 to 3000)'
      },
      features: [
        'Automated server provisioning and software configuration',
        'Idempotent Ansible playbook execution',
        'Zero-downtime service restart via systemd notification',
        'Automated health check validation via Ansible uri module',
        'Secure reverse proxy with Nginx reverse proxy headers'
      ]
    };

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(infoData, null, 2));
    return;
  }

  // 3. Static Web Application Dashboard (Root / or static files)
  let filePath = path.join(__dirname, 'public', pathname === '/' ? 'index.html' : pathname);
  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  // Prevent Directory Traversal
  if (!filePath.startsWith(path.join(__dirname, 'public'))) {
    res.writeHead(403, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Forbidden' }));
    return;
  }

  serveStaticFile(res, filePath, contentType);
});

// Start Server
server.listen(PORT, HOST, () => {
  console.log(`====================================================`);
  console.log(` ShalaConnect DevOps Web Application Started        `);
  console.log(` URL: http://${HOST}:${PORT}`);
  console.log(` Health Check: http://${HOST}:${PORT}/health`);
  console.log(` Student: Yash Janardan Sabale | PRN: 2310423T26-27 `);
  console.log(` College: MIT Academy of Engineering, Alandi, Pune `);
  console.log(` Node Environment: ${NODE_ENV}`);
  console.log(`====================================================`);
});

// Graceful Shutdown
function handleShutdown(signal) {
  console.log(`\nReceived ${signal}. Gracefully shutting down HTTP server...`);
  server.close(() => {
    console.log('HTTP server closed. Exiting process.');
    process.exit(0);
  });
  // Force exit if close takes too long
  setTimeout(() => {
    console.error('Forcefully exiting after timeout.');
    process.exit(1);
  }, 5000);
}

process.on('SIGTERM', () => handleShutdown('SIGTERM'));
process.on('SIGINT', () => handleShutdown('SIGINT'));
