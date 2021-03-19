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
    this.response = await Api.get("bet/");
    // await Api.post("bet/",{"title":"bet04",
    // "description":"bla",
    // "choice1":"Oui",
    // "choice2":"Non"});
  },
  data() {
      return {
      response:{},
      }
  }
});
</script>
