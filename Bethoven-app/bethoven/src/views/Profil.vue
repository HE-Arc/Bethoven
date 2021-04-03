<template>
  <v-container class="ma-0 pa-0" fill-height fluid>
    <profil-card v-if="this.user != null" :user="this.user.user"> </profil-card>
    <statistics-card
      v-if="this.user != null"
      :statistics="this.user.statistics"
    >
    </statistics-card>
    <follows-card
      v-if="this.user != null"
      :follows="this.user.follows"
    ></follows-card>
    <last-users-bets-card
      v-if="this.user != null"
      :bets="this.user.lastBets"
    ></last-users-bets-card>
  </v-container>
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";
import Avatar from "../components/Avatar.vue";
import ProfilCard from "../components/ProfilCard.vue";
import StatisticsCard from "../components/StatisticsCard.vue";
import FollowsCard from "../components/FollowsCard.vue";
import LastUsersBetsCard from "../components/LastUsersBetsCard.vue";

// /api/users/{id}
export default Vue.extend({
  components: {
    Avatar,
    ProfilCard,
    StatisticsCard,
    FollowsCard,
    LastUsersBetsCard,
  },
  name: "Profil",
  async beforeMount() {
    try {
      this.user = await Api.get(`users/${this.idUserProfil}`);
    } catch (e) {
      console.log(e);
    }
  },
  props: {
    id: null,
  },
  data() {
    return {
      user: null,
      idUserProfil: this.id,
    };
  },
});
</script>