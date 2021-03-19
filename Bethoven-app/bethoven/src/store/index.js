import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isUserLogged: false,
    tokenUser: null,
    refreshTokenUser: null
  },
  mutations: {
    logUser(state, token, refreshToken){
      state.isUserLogged = true;
      state.tokenUser = token;
      state.refreshTokenUser = refreshToken;
      return state;
    },
    logout(state){
      state.isUserLogged = false;
      state.tokenUser = null;
      state.refreshTokenUser = null;
      return state;
    },
  },
  actions: {
    logUser(state, token, refreshToken) {
      state.commit('logUser',token, refreshToken);
    },
    logout(state) {
      state.commit('logout');
    }
  },
  modules: {
  }
})
