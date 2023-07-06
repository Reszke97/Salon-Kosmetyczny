<template>
  <v-app 
    id="app"
  >
    <div
      id="custom-container"
      style="
        padding: 0px !important;
        height: 100vh;
        display: flex;
        flex-direction: column;
        background-color: #0844a4!important;
      "
    >
      <nav-bar></nav-bar>
      <v-container fill-height :style="containerStyles">
        <router-view></router-view>
      </v-container>
      <Footer id="custom-footer"></Footer>
    </div >
  </v-app>
</template>

<script>
import { AUTH_API } from './authorization/AuthAPI'
import NavBar from './components/navigation/NavBar.vue'
import Footer from './components/navigation/Footer.vue'

export default {
  name: 'client',
  components: {
    NavBar,
    Footer
  },
  data: () => ({
    screenHeight: 0,
    screenWidth: 0,
    navBarHeight: 0,
    footerHeight: 0,
  }),
  provide(){
    const screenSize = {};
    const navBarSize = {};
    const footerSize = {};
    Object.defineProperty(screenSize, "screenHeight", {
      enumerable: true,
      get: () => this.screenHeight
    })
    Object.defineProperty(screenSize, "screenWidth", {
      enumerable: true,
      get: () => this.screenWidth
    })
    Object.defineProperty(navBarSize, "navBarHeight", {
      enumerable: true,
      get: () => this.navBarHeight
    })
    Object.defineProperty(footerSize, "footerHeight", {
      enumerable: true,
      get: () => this.footerHeight
    })
    return {
      screenSize,
      navBarSize,
      footerSize,
    }
  },

  computed: {
    containerStyles(){
      if(this.screenHeight == 0) return "height:100%!important"
      return `height:${this.screenHeight}px!important`
    }
  },

  mounted(){
    this.$nextTick(() => {
      this.watchScreenHeightResize()
      this.watchScreenWidthResize()
    })
  },
  methods: {
    watchScreenHeightResize() {
      const observer = new ResizeObserver((entries) => {
        this.screenHeight = 
          document.getElementById("custom-container").offsetHeight 
          - entries[0].contentRect.height - document.getElementById("custom-footer").offsetHeight;
        this.navBarHeight = entries[0].contentRect.height;
        this.footerHeight = document.getElementById("custom-footer").offsetHeight;
      });
      observer.observe(document.getElementById("custom-navbar"));
    },
    watchScreenWidthResize() {
      const observer = new ResizeObserver((entries) => {
        this.screenWidth = document.querySelector("body").offsetWidth
      });
      observer.observe(document.querySelector("body"));
    }
  }
}
</script>

<style>
 body {
  overflow: hidden;
 }
</style>