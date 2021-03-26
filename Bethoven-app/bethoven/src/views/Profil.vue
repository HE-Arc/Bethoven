<template>
  <v-container fill-height fluid>
    <v-row align="start" justify="start"> <v-col align="center"> 
        <avatar v-if="this.user!=null" :uname="this.user.user.username"></avatar>
        </v-col></v-row
  ></v-container>
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";
import Avatar from "../components/Avatar.vue";

// /api/users/{id}
export default Vue.extend({
  components: { Avatar },
  name: "Profil",
  async mounted() {
    this.user = await Api.get("users/"+this.idUserProfil);
  },
  props :{
      id:null,
  },
  data() {
    return {
      user: null,
      idUserProfil:this.id,
    };
  },
});
</script>
