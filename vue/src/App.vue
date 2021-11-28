<template>
  <v-app>
    <div id="app">
      <nav-bar></nav-bar>
      <router-view></router-view>
      <Footer></Footer>
    </div>
  </v-app>
</template>

<script>
import { AUTH_API } from './authorization/AuthAPI'
import NavBar from './components/navigation/NavBar.vue'
import Footer from './components/navigation/Footer.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    Footer
  },

  created(){
    // sprawdzenie czy refresh token istnieje
    console.log(localStorage.getItem('refreshToken'))
    if(localStorage.getItem('refreshToken')){
      try {
        //const REFRESH_TOKEN_PARTS2 = JSON.parse(atob(localStorage.getItem('token').split('.')[1]));
        //console.log(REFRESH_TOKEN_PARTS2)
        const NOW = Math.ceil(Date.now() / 1000);
        const REFRESH_TOKEN_PARTS = JSON.parse(atob(localStorage.getItem('refreshToken').split('.')[1]));
        console.log(REFRESH_TOKEN_PARTS)
        // sprawdź czy refresh token wygasł
        if(REFRESH_TOKEN_PARTS.exp < NOW ){
          AUTH_API.post('/api/v1/token/refresh/', {
            refresh: localStorage.getItem('refreshToken')
          })
          .then(response => {
            this.$store.commit('setToken', {
              access: response.data.access,
              refresh: response.data.refresh
            })
            this.$store.commit('setIsAuthenticated', true)
          })
          .catch(error => {
            console.log(error)
          })
        }
        // sprawdzenie czy token jest legitny
        else{
          AUTH_API.post('/api/v1/token/verify/', {
            token: localStorage.getItem('refreshToken')
          })
          .then(response => {
            this.$store.commit('setRefreshToken')
            this.$store.commit('setIsAuthenticated', true)
          })
          .catch(error => {
            console.log(error)
          })
        }
      } catch( error ){
        console.log(error)
        return
      }
    }  
    // jeśli nie ma refresh tokena to z automatu isAuthenticated zostaje na false
    else{
      return
    }
  },
  updated(){
    // console.log(document.getElementById("image"))
  }
}
</script>

<style>

</style>
