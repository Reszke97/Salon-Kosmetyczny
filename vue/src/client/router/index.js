import Vue from 'vue'
import VueRouter from 'vue-router'


import Register from '../components/registration/Register.vue'
import Login from '../components/authentication/Login.vue'
import Logout from '../components/authentication/Logout.vue'
import PasswordChange from '../components/Settings/components/PasswordChange.vue'
import ResetPassword from '../components/authentication/ResetPassword.vue'
import PasswordResetEmail from '../components/authentication/ResetPasswordEmail.vue'
import SearchForService from '../components/appointment/views/SearchForService.vue'
import SettingsPanel from '../components/Settings/views/SettingsPanel.vue'
// import Calendar from '../components/employee/views/Calendar.vue'
// import Service from "../components/service/views/Service.vue"

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: SearchForService
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

  // {
  //   path: '/calendar/monthly',
  //   name: 'CalendarMonthly',
  //   component: Calendar,
  //   props: {
  //     calendarType: "monthly"
  //   },
  // },
  // {
  //   path: '/calendar/weekly',
  //   name: 'CalendarWeekly',
  //   component: Calendar,
  //   props: {
  //     calendarType: "weekly"
  //   },
  // },
  // {
  //   path: '/calendar/daily',
  //   name: 'CalendarDaily',
  //   component: Calendar,
  //   props: {
  //     calendarType: "daily"
  //   },
  // },
  // {
  //   path: "/defineservice",
  //   name: "Service",
  //   component: Service,
  //   // props: {
  //   //   calendarType: "daily"
  //   // },
  // },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL + 'client/',
  routes
})

export default router