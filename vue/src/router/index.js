import Vue from 'vue'
import VueRouter from 'vue-router'
import navigation from '../components/userPanels/Navigation.vue'

import Register from '../components/authentication/Register.vue'
import Login from '../components/authentication/Login.vue'
import Logout from '../components/authentication/Logout.vue'
import PasswordChange from '../components/authentication/PasswordChange.vue'
import ResetPassword from '../components/authentication/ResetPassword.vue'
import PasswordResetEmail from '../components/authentication/ResetPasswordEmail.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/panel/:type?',
    name: 'Navigation',
    component: navigation
  },
  {
    path: '/',
    name: 'Configure',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../components/configure/Stepper.vue')
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
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router