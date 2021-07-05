const userStore = {
  state: {
    id: "",
    userType: "",
    access_token: "",
    refresh_token: "",
  },
  getters: {
    getUser: function(state) {
      return state;
    },
  },
  mutations: {
    setUser: function(state, payload) {
      state.id = payload.user_id;
      state.userType = payload.userType;
      state.access_token = payload.tokens.access_token;
      state.refresh_token = payload.tokens.refresh_token;
    },
  },
  actions: {},
};

export default userStore;
