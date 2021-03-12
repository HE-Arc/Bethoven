<!-- TEMPLATE -->
<template>
  <div>
    <v-app-bar color="primary" dark fixed>
      <v-toolbar-title to="/" >Bethoven</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <!-- TODO add v-if logged -->
      <v-btn icon>
        <span> 25 </span> 
        <v-icon>mdi-alpha-b-circle</v-icon>
      </v-btn>

      <v-menu left bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-account-circle-outline</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item to="/register">
            <v-list-item-title >Register</v-list-item-title>
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

export default Vue.extend({
  name: "Header",
  methods: {
    toggleDrawer: function () {
      this.$typedStore.commit("DRAWER_TOGGLE");
    },
    goToRegister: function(){
      this.$router.push({ name: 'Register' });
    },
    goToLogin: function(){
      this.$router.push({ name: 'Login' });
    }
    
  },
});
</script>
