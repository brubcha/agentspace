const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api/agent",
    createProxyMiddleware({
      target: "http://localhost:5000",
      pathRewrite: { "^/api/agent": "/agent" },
      changeOrigin: true,
    }),
  );
};
