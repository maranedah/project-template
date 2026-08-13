import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Dev-server proxy only (production nginx has its own /api proxy — nginx.conf).
// Port must match APP_BACKEND_PORT from the root .env:
//   APP_BACKEND_PORT=8110 npm run dev
const backendPort = process.env.APP_BACKEND_PORT ?? "8100";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": `http://localhost:${backendPort}`,
    },
  },
});
