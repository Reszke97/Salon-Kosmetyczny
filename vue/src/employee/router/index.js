import Vue from 'vue';
import VueRouter from 'vue-router';

import Register from '../components/registration/Register.vue';
import Login from '../components/authentication/Login.vue';
import Logout from '../components/authentication/Logout.vue';
import PasswordChange from '../components/authentication/PasswordChange.vue';
import ResetPassword from '../components/authentication/ResetPassword.vue';
import PasswordResetEmail from '../components/authentication/ResetPasswordEmail.vue';
import Calendar from '../components/employee/views/Calendar.vue';
import Service from "../components/service/views/Service.vue";
import SettingsPanel from '../components/Settings/views/SettingsPanel.vue';
import BusinessActivity from "../components/BusinessActivity/views/BusinessActivity.vue";
import store from "../store/index";
import { AUTH_API } from '../authorization/AuthAPI';

Vue.use(VueRouter)

const routes = [
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
    path: '/settings',
    name: 'Settings',
    component: SettingsPanel
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
    path: '/business-activity/manage',
    name: 'BusinessActivity',
    component: BusinessActivity,
  },


  // Calendar Start
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar,
    props: {
      calendarType: "monthly"
    },
  },

  //Calendar End

  //Service Start
  {
    path: "/defineservice",
    name: "Service",
    component: Service,
  },
  //Service End

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL + 'employee/',
  routes
})

async function authenticate(){
  // sprawdzenie czy refresh token istnieje
  if(localStorage.getItem('employeeRefreshToken')){
    try {
      const NOW = Math.ceil(Date.now() / 1000);
      const REFRESH_TOKEN_PARTS = JSON.parse(atob(localStorage.getItem('employeeRefreshToken').split('.')[1]));
      // sprawdź czy refresh token wygasł
      if(REFRESH_TOKEN_PARTS.exp < NOW ){
        const API = await AUTH_API();
        await API.post('/api/v1/token/refresh/', {
          refresh: localStorage.getItem('employeeRefreshToken')
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
          token: localStorage.getItem('employeeRefreshToken')
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

router.beforeEach( async (to, from, next) => {
  if(store.state.isAuthenticated){
    if(to.path === "/"){
      window.location.assign("/employee/calendar");
    } else {
      next();
    }
  } else {
    await authenticate();
    if(store.state.isAuthenticated){
      if(to.path === "/"){
        window.location.assign("/employee/calendar");
      } else {
        next();
      }
    } else {
      if(to.path === "/login" || to.path == "/register"){
        next();
      } else {
        window.location.assign("/employee/login");
      }
    }
  }
})

export default router