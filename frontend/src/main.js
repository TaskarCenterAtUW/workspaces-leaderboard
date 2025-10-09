import { createApp } from "vue";
import App from "./App.vue";
import { router } from "@/helpers/router";

const app = createApp(App);
const components = import.meta.glob('./components/*.vue', { eager: true });

Object.entries(components).forEach(([path, definition]) => {
  const componentName = path.split('/').pop().replace(/\.\w+$/, '')

  // Register component on this Vue instance
  app.component(componentName, definition.default)
})

app.use(router);
app.mount("#app");