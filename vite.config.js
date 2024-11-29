import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// https://vite.dev/config/
export default defineConfig({
  server: {
    proxy: {
      '/get-loan-by-customer': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
      },
      '/generate': 'http://127.0.0.1:5000',
      '/bpi': 'http://127.0.0.1:5000',
    },
  },
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate', // This will register the service worker
      manifest: {
        name: 'BizAI: Your Financial Assistant',
        short_name: 'BizAI',
        description: 'An AI assistant that helps you with your financial needs.',
        theme_color: '#500000',
        icons: [
          {
            src: '/icons/icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/icons/icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ],
        start_url: '/',
        display: 'standalone', // Makes the app look like a native app
        background_color: '#500000',
      },
    }),
  ],
})
