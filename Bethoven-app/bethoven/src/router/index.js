import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import store from '@/store'
import Api from "@/api/ApiRequester";

Vue.use(VueRouter)

//SI ACCESSIBLE PAR TOUS :
// RIEN A FAIRE

//SI SEUELEMENT ACCESSIBLE PAR LES UTILISATEURS NON LOGUE
// meta: {
//   onlyUnlogged: true
// }

//SI SEUELEMENT ACCESSIBLE PAR LES UTILISATEURS LOGUE
// meta: {
//   onlyLogged: true
// }


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      onlyUnlogged: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      onlyUnlogged: true
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


/**
 * Get session from sessionStorage if user reload page
 *
 * @return {*}  {boolean} true if session stored in sessionStorage; false otherwise
 */
function loadSessionFromStorage() {
  if (window.sessionStorage.getItem("token") != null) {
    Api.setToken(window.sessionStorage.getItem("token"));
    return true;
  } else {
    return false;
  }
}

/**
* Define if user is logged in Vuex ou sessionStorage
*
* @return {*}  {boolean} true if user is logged in; false otherwise
*/
function isLogged() {
  // Not connected by login action
  if (!store.state.isUserLogged) {
    if (loadSessionFromStorage()) {
      return true;
    }
    return false;
  }
  return true;
}
/**
 * Define autorisation for each routes
 */
router.beforeEach((to, from, next) => {
  if (to.matched.some((route) => route.meta.onlyLogged)) {
    if (!isLogged()) {
      next({ name: "Login" });
    } else {
      next();
    }
  } else if (to.matched.some((route) => route.meta.onlyUnlogged)) {
    if (isLogged()) {
      next({ name: "Home" });
    } else {
      next();
    }
  } else {
    loadSessionFromStorage();
    next();
  }
});





export default router
