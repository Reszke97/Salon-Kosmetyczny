<template>
    <v-footer
        dark
        padless
        bottom 
        fixed
        style="position:relative!important;margin-top: auto;"
    >
        <v-card
            flat
            tile
            width="100%"
            class="indigo white--text text-center"
        >

            <v-card-text class="white--text">
                {{ new Date().getFullYear() }} — <strong>Marcin Reszke</strong>
            </v-card-text>
        </v-card>
  </v-footer>
</template>

<script>
    export default {
      data(){
        return {
        //   footerItems: [
        //     { path: 'https://www.facebook.com/', icon: 'mdi-facebook' },
        //     { path: 'https://twitter.com/', icon: 'mdi-twitter' },
        //     { path: 'https://www.linkedin.com/', icon: 'mdi-linkedin' },
        //     { path: 'https://www.instagram.com/', icon: 'mdi-instagram ' },
        //   ],
        }
      },

      methods:{

      }
    }
</script>
<style scoped>
    .textDecoration{
        text-decoration: none!important;
    }
</style>
