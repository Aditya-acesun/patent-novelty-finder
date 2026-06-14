import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': { target: 'http://backend:4000', changeOrigin: true },
      '/ai':  { target: 'http://ai-service:8000', changeOrigin: true, rewrite: p => p.replace(/^\/ai/, '') },
    },
  },
});
