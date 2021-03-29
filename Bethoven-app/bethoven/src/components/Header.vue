<!-- TEMPLATE -->
<template>
  <v-app-bar color="primary" dark fixed app>
    <v-btn icon to="/trending">
      <img alt="Vue logo" src="../assets/bethoven.png" height="40px"/>
    </v-btn>
    <v-toolbar-title to="/">Bethoven</v-toolbar-title>
    <v-spacer></v-spacer>


    <v-row align="center" justify="end" class="mx-3">
      <v-btn icon to="/search">
            <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <span v-if="logged">
          <span class="mx-2" v-if="$vuetify.breakpoint.mdAndUp">{{ uname }}</span>
          <span class="ml-1">{{ userCoins }}</span>
          <v-icon class="mx-1">mdi-alpha-b-circle</v-icon>
      </span>
    </v-row>

    <v-menu left class="mx-3">
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-if="logged" icon v-bind="attrs" v-on="on">
          <avatar :uname="uname"></avatar>
        </v-btn>
        <v-btn v-else icon v-bind="attrs" v-on="on">
          <v-icon >mdi-account-circle-outline</v-icon>
        </v-btn>
      </template>

      <v-list v-if="logged">
        <!-- TODO ADD SETTINGS -->
        <v-list-item v-on:click="MyProfil()">
          <v-list-item-title>My Profil</v-list-item-title>
        </v-list-item>
        <v-list-item v-on:click="logout()">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
      <v-list v-else>
        <v-list-item to="/register">
          <v-list-item-title>Register</v-list-item-title>
        </v-list-item>
        <v-list-item to="/login">
          <v-list-item-title>Login</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>


<!-- SCRIPT -->
<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";

import Avatar from "../components/Avatar.vue";

export default Vue.extend({
  name: "Header",
  components: { Avatar },
  computed: {
    logged() {
      return this.$store.state.isUserLogged;
    },
    userCoins() {
      return this.$store.state.user.coins;
    },
    uname(){
      return this.$store.state.user.username;
    },
  },
  methods: {
    logout: async function () {
      await Api.logout();
    },
    MyProfil() {
      this.$router.push({path:"/profil/"+this.$store.state.user.id+"/"})
    },
    
  },
});
</script>
