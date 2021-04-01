<template>
  <v-container>
    <v-card v-if="this.user != null" class="ma-2 pt-1">
      <v-row align="center">
        <v-col align="center" cols="3">
          <avatar :uname="this.user.username"></avatar>
        </v-col>
        <v-col cols="5">
          <v-card-title v-if="this.user != null"
            >{{ this.user.username }}
          </v-card-title>
          <v-card-subtitle v-if="this.user != null">
            {{ this.user.coins }}
            <v-icon>mdi-alpha-b-circle</v-icon>
          </v-card-subtitle>
        </v-col>
        <v-col
          align="center"
          cols="4"
          v-if="
            this.$store.state.isUserLogged &&
            this.$store.state.user.id != this.user.id
          "
        >
          <v-btn
            v-if="this.$store.state.user.following.includes(this.user.id)"
            v-on:click="this.unfollow"
            ><v-icon>mdi-account-remove</v-icon></v-btn
          >
          <v-btn v-else v-on:click="this.follow"
            ><v-icon>mdi-account-plus</v-icon></v-btn
          >
        </v-col>
        <v-col
          align="center"
          cols="4"
          v-else-if="!this.$store.state.isUserLogged"
        >
          <v-btn v-on:click="this.follow"
            ><v-icon>mdi-account-plus</v-icon></v-btn
          >
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
import Avatar from "./Avatar.vue";
import Api from "@/api/ApiRequester";

export default {
  components: { Avatar },
  props: {
    user: {},
  },
  methods: {
    async follow() {
      if (this.$store.state.isUserLogged) {
        try {
          await Api.get("users/" + this.user.id + "/follow/");
          Api.updateUserInformations();
        } catch (e) {
          console.log(e);
        }
      } else {
        this.$router.push({ name: "Login" });
      }
    },
    async unfollow() {
      if (this.$store.state.isUserLogged) {
        try {
          await Api.get("users/" + this.user.id + "/unfollow/");
          Api.updateUserInformations();
        } catch (e) {
          console.log(e);
        }
      } else {
        this.$router.push({ name: "Login" });
      }
    },
  },
};
</script>