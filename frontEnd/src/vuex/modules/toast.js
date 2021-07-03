const toast = {
    state: {
        message: "",
        snackbar: false,
        color: "",
        timeout:"2000",
    },
    getters: {
        getMessage: function (state) {
            return state.message;
        },
        getSnackbar: function (state) {
            return state.snackbar;
        },
        getColor: function (state) {
            return state.color;
        },
    },
    mutations: {
        setMessage: function (state, msg) {
            state.message = msg;
        },
        setSnackbar: function (state, val) {
            state.snackbar = val;
        },
        setColor: function (state, color) {
            state.color = color;
        },
    },
    actions: {
        callToast: function ({ commit }, payload) {
            commit("setMessage", payload.msg);
            //성공
            if (payload.result === "success") {
                commit("setColor", "success");
            }//실패
            else if (payload.result === "fail" || payload.result === "error") {
                commit("setColor", "error");
            }
            commit("setSnackbar", true);
        }
    },
};

export default toast;
