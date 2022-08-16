import { createStore } from "vuex";
// import { Vue } from "vue";

export default createStore({
  state: {
    login: false,
    name: "",
  },
  getters: {},
  mutations: {
    login(state) {
      // Vue.set(state,"login",true)
      state.login = true;
    },
    logout(state) {
      // Vue.set(state)
      state.login = false;
    },
    name(state, name) {
      state.name = name;
    },
  },
  actions: {},
  modules: {},
});
