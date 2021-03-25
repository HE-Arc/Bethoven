<template>
  <v-container fill-height fluid>
    <v-row align="start" justify="start">
      <v-col align="center">
        <img alt="Vue logo" src="../assets/bethoven.png" width="200" />
        <p>Ooooops nothing to show !</p>
        <p>{{ this.response }}</p>
      </v-col></v-row
    ></v-container
  >
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";

export default Vue.extend({
  name: "Home",
  async beforeMount () {
    this.response = await Api.get("bets/?number=5");
  },
  data() {
      return {
      response:{},
      }
  }
});
</script>
