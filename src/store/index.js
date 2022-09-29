import { createStore } from "vuex";

export default createStore({
  state: {
    login: false,
    name: "",
    admin: {
      login: false,
      authkey: "",
      last: 0,
    },
  },
  getters: {},
  mutations: {
    login(state) {
      state.login = true;
    },
    logout(state) {
      state.login = false;
    },
    name(state, name) {
      state.name = name;
    },
    admin(state, log, authkey) {
      state.admin.login = log;
      if (log) {
        state.admin.authkey = authkey;
        state.admin.last = new Date().getTime() / 1000;
      }
    },
  },
  actions: {},
  modules: {},
});
