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
    }

    // "LOGIN": (state, token) => state.tokenUser = token,
    // "LOGOUT": (state) => state.tokenUser = null,
  },
  actions: {
    logUser(state, token) {
      state.commit('logUser',token);
    }
  },
  modules: {
  }
})
