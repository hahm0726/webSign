import Vue from 'vue'
import router from "/src/router/router.js"
import vuetify from './plugins/vuetify'
import Root from './App.vue'
import VueSignaturePad from 'vue-signature-pad';

Vue.use(VueSignaturePad);
//Vue.config.productionTip = false


new Vue({
  vuetify,
  router,
  render: h => h(Root)
}).$mount('#app')
