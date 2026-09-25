/**
 * SentinelAI - AI-Powered Financial Fraud Detection Platform
 * Primary Node.js / Express Server & RESTful API Service.
 */

const express = require('express');
const cors = require('cors');
const path = require('node:path');
const fs = require('node:fs');
const { getSettings } = require('./src/config');
const { getTransactionStats } = require('./src/database');

const authRoutes = require('./src/routes/authRoutes');
const statsRoutes = require('./src/routes/statsRoutes');
const transactionRoutes = require('./src/routes/transactionRoutes');
const ruleRoutes = require('./src/routes/ruleRoutes');
const userRoutes = require('./src/routes/userRoutes');
const modelRoutes = require('./src/routes/modelRoutes');
const settingsRoutes = require('./src/routes/settingsRoutes');

const app = express();
const config = getSettings();
const PORT = config.port || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    if (req.path.startsWith('/api')) {
      console.log(`[REST API] ${req.method} ${req.originalUrl} -> ${res.statusCode} (${duration}ms)`);
    }
  });
  next();
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  try {
    const stats = getTransactionStats();
    res.json({
      status: 'healthy',
      system: 'SentinelAI Financial Surveillance Engine',
      version: '2.4.0-node',
      uptime_seconds: process.uptime(),
      timestamp: new Date().toISOString(),
      database: {
        status: 'connected',
        type: 'SQLite3 (node:sqlite WAL)',
        transactions_count: stats.total_count
      }
    });
  } catch (err) {
    res.status(500).json({
      status: 'unhealthy',
      error: err.message
    });
  }
});

// Mount REST API Routers
app.use('/api/auth', authRoutes);
app.use('/api/stats', statsRoutes);
app.use('/api/transactions', transactionRoutes);
app.use('/api/rules', ruleRoutes);
app.use('/api/users', userRoutes);
app.use('/api/models', modelRoutes);
app.use('/api/settings', settingsRoutes);

// Serve Frontend Static Assets
const publicDir = path.join(__dirname, 'public');
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}
app.use(express.static(publicDir));

// Fallback to index.html for single-page client routing
app.use((req, res, next) => {
  if (req.method === 'GET' && !req.path.startsWith('/api')) {
    const indexPath = path.join(publicDir, 'index.html');
    if (fs.existsSync(indexPath)) {
      return res.sendFile(indexPath);
    }
  }
  next();
});

// Global Error Handler
app.use((err, req, res, next) => {
  console.error('[Unhandled Server Error]:', err);
  res.status(500).json({
    status: 'error',
    message: err.message || 'Internal server error occurred.'
  });
});

// Start Server
if (require.main === module) {
  app.listen(PORT, '0.0.0.0', () => {
    console.log('================================================================');
    console.log('  SENTINELAI — AI-POWERED FINANCIAL FRAUD DETECTION SYSTEM');
    console.log('================================================================');
    console.log(`  [+] Node.js Backend Server Active on: http://localhost:${PORT}`);
    console.log(`  [+] RESTful API Endpoints available at: http://localhost:${PORT}/api/`);
    console.log(`  [+] Health check: http://localhost:${PORT}/api/health`);
    console.log(`  [+] Interactive UI: http://localhost:${PORT}/`);
    console.log('================================================================');
  });
}

module.exports = app;
