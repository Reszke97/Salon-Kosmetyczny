import Vue from 'vue'
import VueRouter from 'vue-router'


import Register from '../components/registration/Register.vue';
import Login from '../components/authentication/Login.vue';
import Logout from '../components/authentication/Logout.vue';
import PasswordChange from '../components/Settings/components/PasswordChange.vue';
import ResetPassword from '../components/authentication/ResetPassword.vue';
import PasswordResetEmail from '../components/authentication/ResetPasswordEmail.vue';
import AllBusinesses from '../components/SearchForService/views/AllBusinesses.vue';
import SettingsPanel from '../components/Settings/views/SettingsPanel.vue';
import DisplayVisits from "../components/Visits/DisplayVisits.vue";
import store from "../store/index";
import { AUTH_API } from '../authorization/AuthAPI';

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: AllBusinesses
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },

  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  
  {
    path: '/emailactivation/:activated',
    redirect: to =>{
      return {
        name: "Login",
        params: { activated: to.params.activated },
      }
    },
  },

  {
    path: '/passwordreset',
    name: 'PasswordReset',
    component: ResetPassword
  },

  {
    path: '/passwordresetemailsend',
    name: 'PasswordResetEmail',
    component: PasswordResetEmail
  },


  {
    path: '/passwordchangeaccepted/:uidb64/:token',
    redirect: to =>{
      return {
        name: "PasswordReset",
        params: { 
          uidb64: to.params.uidb64,
          token: to.params.token
        },
      }
    },
  },


  {
    path: '/register',
    name: 'Register',
    component: Register,
  },

  {
    path: '/passwordchange',
    name: 'PasswordChange',
    component: PasswordChange
  },

  {
    path: '/settings',
    name: 'Settings',
    component: SettingsPanel
  },

  {
    path: '/visits',
    name: 'Visits',
    component: DisplayVisits
  },
]

async function authenticate(){
  // sprawdzenie czy refresh token istnieje
  if(localStorage.getItem('clientRefreshToken')){
    try {
      const NOW = Math.ceil(Date.now() / 1000);
      const REFRESH_TOKEN_PARTS = JSON.parse(atob(localStorage.getItem('clientRefreshToken').split('.')[1]));
      // sprawdź czy refresh token wygasł
      if(REFRESH_TOKEN_PARTS.exp < NOW ){
        const API = await AUTH_API();
        await API.post('/api/v1/token/refresh/', {
          refresh: localStorage.getItem('clientRefreshToken')
        })
        .then(response => {
          store.commit('setToken', {
            access: response.data.access,
            refresh: response.data.refresh
          })
          store.commit('setIsAuthenticated', true)
        })
        .catch(error => {
          console.log(error)
        })
      }
      // sprawdzenie czy token jest legitny
      else{
        const API = await AUTH_API();
        await API.post('/api/v1/token/verify/', {
          token: localStorage.getItem('clientRefreshToken')
        })
        .then(() => {
          store.commit('setRefreshToken')
          store.commit('setIsAuthenticated', true)
        })
        .then( async () => {
          const API = await AUTH_API();
          await API.get('/api/v1/user/getuserrole/')
          .then(response=>{
            store.commit('setRole', response.data.role)
          })
        })
        .catch(error => {
          console.log(error)
        })
      }
      return
    } catch( error ){
      console.log(error)
      return
    }
  }
}

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL + 'client/',
  routes
})

router.beforeEach( async (to, from, next) => {
  await authenticate();
  if(store.state.isAuthenticated){
    next();
  } else {
    if(["/register", "/passwordreset", "/passwordresetemailsend"].includes(to.path)){
      next();
    } else if(["/visits", "/settings"].includes(to.path)){
      window.location.assign("/client/login");
    } else {
      next();
    }
  }
})

export default router