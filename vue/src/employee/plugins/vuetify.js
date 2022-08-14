import Vuetify from 'vuetify';
import Vue from 'vue';
import 'vuetify/dist/vuetify.min.css';
import light from "./theme"

Vue.use(Vuetify);
export default new Vuetify(
  {
    icons: {iconfont:'mdi'},
    theme: { 
      themes: {
        light
      },
    }
  }
)