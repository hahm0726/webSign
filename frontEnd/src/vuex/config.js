import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

import toast from "./modules/toast";
import userStore from "./modules/userStore";
Vue.use(Vuex);

// 사용할 모듈들 임포트

const debug = process.env.NODE_ENV !== "production";

export const store = new Vuex.Store({
  modules: {
    toast,
    userStore,
  },

  strict: debug,

  plugins: [
    createPersistedState({
      storage: window.sessionStorage,
    }),
  ],
});

export default store;
