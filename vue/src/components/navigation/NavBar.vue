<template>
  <div>
    <v-app-bar class="indigo white--text">
      <v-toolbar-title>Home</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="d-none d-sm-flex">
        <v-btn
          class="elevation-0 indigo white--text"
          flat
          v-for="item in menuItems"
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
        <v-list-item-group>
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
  </div>
</template>

<script>
    export default {
      data(){
        return {
          drawer: false,
          tab: null,
          items: [
            'web', 'shopping', 'videos', 'images', 'news',
          ],
          menuItems: [
            { title: 'Home', path: '/', icon: 'mdi-home' },
            { title: 'login', path: '/login', icon: 'mdi-login' },
            { title: 'register', path: '/register', icon: 'mdi-account-plus ' }
          ],
        }
      },
    }
</script>