import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isUserLogged: false,
    tokenUser: null
  },
  mutations: {
    logUser(state, token){
      state.isUserLogged = true;
      state.tokenUser = token;
      return state;
    },
    logout(state){
      state.isUserLogged = false;
      state.tokenUser = null;
      return state;
    },
  },
  actions: {
    logUser(state, token) {
      state.commit('logUser',token);
    },
    logout(state) {
      state.commit('logout');
    }
  },
  modules: {
  }
})
