import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from "fs";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        port: 80,
        watch: {
            // usePolling: true
        },
        // https: {
        //     key: fs.readFileSync('./credentials/key.pem'),
        //     cert: fs.readFileSync('./credentials/cert.pem')
        // }
    }
})
