import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    include: ['date-fns/locale/tr', 'date-fns/_lib/format/longFormatters'],
  },
})
