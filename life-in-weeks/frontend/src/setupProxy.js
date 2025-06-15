
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/events',
    createProxyMiddleware({
      target: 'http://localhost:8000', // Your backend URL
      changeOrigin: true,
    })
  );
};