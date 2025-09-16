import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
	build: {
		outDir: 'dist', // Output directory for the production build
   		sourcemap: true, // Generate sourcemaps for debugging
   		minify: 'esbuild', // Minification strategy (terser or esbuild)
		rollupOptions: {
			output: {
				globals: {
					vue: "Vue",
				},
			},
		},
	},
	plugins: [vue()],
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "./src"),
		},
	},
});
