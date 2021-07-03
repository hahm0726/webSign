import Vue from "vue";
import Vuex from "vuex";

import toast from "./modules/toast";

Vue.use(Vuex);

// 사용할 모듈들 임포트

const debug = process.env.NODE_ENV !== "production";


export const store = new Vuex.Store({
  modules: {
      toast,
  },
  strict: debug,
  
  
});

export default store;
