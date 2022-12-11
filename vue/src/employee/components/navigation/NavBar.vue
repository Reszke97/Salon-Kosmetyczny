<template>
  <v-container
    fluid
    style="padding:0"
    id="custom-navbar"
  >
    <v-app-bar class="indigo white--text">
      <v-toolbar-title v-if="isAuthenticated">Salon Kosmetyczny</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items 
        class="d-none d-sm-flex"
      >
        <v-btn
          class="elevation-0 indigo white--text"
          v-for="item in menuItemsLoaded"
          :key="item.title"
          :to="item.path">
          <v-icon left dark>{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
      <v-app-bar-nav-icon
        @click="drawer = true" 
        class="d-flex d-sm-none indigo white--text"
      ></v-app-bar-nav-icon>
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary
    >
      <v-list
        nav
        dense
      >
        <v-list-item-group
        >
          <v-list-item 
            v-for="item in menuItems"
            :key="item.title"
            :to="item.path"
          >
            <v-list-item-title>
              <v-icon left>{{ item.icon }}</v-icon>
              {{ item.title }}
            </v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </v-container>
</template>

<script>
    import { mapState } from "vuex"
    export default {
      data(){
        return {
          drawer: false,
          tab: null,
          loaded: false,
          menuItems: [
            { title: "login", path: "login", icon: "mdi-login" },
          ],
        }
      },

      computed: {
        ...mapState({
          isAuthenticated: (state) => state.isAuthenticated,
          role: (state) => state.role
        }),
        auth(){
          return this.isAuthenticated
          ? { title: 'wyloguj', path: '/logout', icon: 'mdi-logout' }
          : { title: 'login', path: '/login', icon: 'mdi-login' }
        },

        menuItemsLoaded(){
          let menuItems = [...this.menuItems];
          if(this.role && this.isAuthenticated){
            menuItems = [
              ...menuItems,
              { title: "Usługi", path: "/defineservice", icon: "mdi-plus" },
              { title: "Ustawienia", path: "/settings", icon: "mdi-cog-outline" },
            ]
            if(this.role == "owner"){
              menuItems.splice(2,0, 
                { title: "Moja firma", path: "/business-activity/manage", icon: "mdi-office-building-cog" }
              )
            }
          } return menuItems
        }
      },

    }
</script>