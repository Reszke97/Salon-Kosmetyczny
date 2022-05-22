<template>
  <v-app 
    id="app"
  >
    <div 
      style="
        padding: 0px !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
      "
    >
      <nav-bar></nav-bar>
      <v-container fill-height>
        <router-view></router-view>
      </v-container>
      <Footer></Footer>
    </div >
  </v-app>
</template>

<script>
import { AUTH_API } from './authorization/AuthAPI'
import NavBar from './components/navigation/NavBar.vue'
import Footer from './components/navigation/Footer.vue'

export default {
  name: 'employee',
  components: {
    NavBar,
    Footer
  },

  created(){
    // sprawdzenie czy refresh token istnieje
    if(localStorage.getItem('refreshToken')){
      try {
        const NOW = Math.ceil(Date.now() / 1000);
        const REFRESH_TOKEN_PARTS = JSON.parse(atob(localStorage.getItem('refreshToken').split('.')[1]));
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
          .then(() => {
            this.$store.commit('setRefreshToken')
            this.$store.commit('setIsAuthenticated', true)
          })
          .then(() => {
            AUTH_API.get('/api/v1/user/getuserrole/')
            .then(response=>{
              this.$store.commit('setRole', response.data.role)
            })
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
}
</script>

<style>

</style>
