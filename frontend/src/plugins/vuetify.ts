import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { createVuetify } from "vuetify";

export default createVuetify({
  defaults: {
    VBtn: { variant: "flat" },
    VTextField: { variant: "outlined", density: "comfortable" },
  },
});
