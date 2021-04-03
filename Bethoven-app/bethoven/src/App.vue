<template>
  <v-app>
    <Header />
    <v-main>
      <message-center />
      <router-view></router-view>
    </v-main>
    <Navbar />
  </v-app>
</template>

<script>
import Vue from "vue";
import Header from "@/components/Header.vue";
import Navbar from "@/components/Navbar.vue";
import MessageCenter from "@/components/MessageCenter.vue";
import "@/assets/styles/main.scss";

export default Vue.extend({
  name: "App",
  components: { Header, Navbar, MessageCenter },
});
</script>