<!-- TEMPLATE -->
<template>
  <div>
    <v-app-bar color="primary" dark fixed>
      <v-toolbar-title to="/">Bethoven</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn v-if="logged" icon>
        <span> {{ userCoins }} </span>
        <v-icon>mdi-alpha-b-circle</v-icon>
      </v-btn>

      <v-menu left bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-account-circle-outline</v-icon>
          </v-btn>
        </template>

        <v-list v-if="logged">
          <!-- TODO ADD SETTINGS -->
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
  </div>
</template>


<!-- SCRIPT -->
<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";

export default Vue.extend({
  name: "Header",
  computed: {
    logged() {
      return this.$store.state.isUserLogged;
    },
    userCoins() {
      return this.$store.state.user.coins;
    },
  },
  methods: {
    logout: async function () {
      await Api.logout();
    },
  },
});
</script>
