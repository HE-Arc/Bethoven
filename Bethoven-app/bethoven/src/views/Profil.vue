<template>
  <v-container >
    <profil-card :user="this.user">
      <statistics-card></statistics-card>


    </profil-card>
  </v-container>
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";
import Avatar from "../components/Avatar.vue";
import ProfilCard from "../components/ProfilCard.vue";
import StatisticsCard from "../components/StatisticsCard.vue";

// /api/users/{id}
export default Vue.extend({
  components: { Avatar, ProfilCard, StatisticsCard },
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
