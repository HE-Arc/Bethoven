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
  async mounted() {
        var bodyFormData = new FormData();
        bodyFormData.append('grant_type', "password");
        bodyFormData.append('client_id', "dhVqxxKFZYhvItVvOOU2KtD6EnKJYERcjcvdq8Kh");
        bodyFormData.append('client_secret', "VaBmlKbzvDtVwDkyzUzcQa6nMU8osXQnLg1D21B859TR2IronyqWGRRPtjUouhSywKx3lEsDD5f33bYr2p9rbKrCesws3G0kHm3oEl02VtWSMyS2uPqZ1x7cGB7CjMit");
        bodyFormData.append('username', "toto");
        bodyFormData.append('password', "1234");
        this.response = await Api.login(bodyFormData); 

        console.log(bodyFormData);
        // this.response = await Api.login({grant_type:"password", client_id:"dhVqxxKFZYhvItVvOOU2KtD6EnKJYERcjcvdq8Kh", client_secret:"VaBmlKbzvDtVwDkyzUzcQa6nMU8osXQnLg1D21B859TR2IronyqWGRRPtjUouhSywKx3lEsDD5f33bYr2p9rbKrCesws3G0kHm3oEl02VtWSMyS2uPqZ1x7cGB7CjMit",username:"toto", password:"1234"}); 
    },
  data() {
      return {
      // response:{},
      }
  }
});
</script>
