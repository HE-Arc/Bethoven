<template>
  <v-app>
    <!-- <Drawer :avatarTimestamp="this.$typedStore.state.avatarTimestamp"/> -->
    <Header />
    <v-main>
      <router-view></router-view>
    </v-main>
    <Navbar />
  </v-app>
</template>

<script>
import Vue from "vue";
import Header from "@/components/Header.vue";
import Navbar from "@/components/Navbar.vue";
import "@/assets/styles/main.scss";

export default Vue.extend({
  name: "App",
  components: { Header, Navbar },
});
</script>
