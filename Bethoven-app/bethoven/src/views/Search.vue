<template>
  <v-container fill-height fluid class="pa-0 pt-3">
    <v-row align="center" justify="center">
      <v-col cols="6">
          <!-- search text field -->
        <v-text-field
          label="Search friend"
          placeholder="Rajinth-xXx"
          outlined
          dense
          append-icon="mdi-magnify"
          v-model="unameQuery"
          @keyup="finishedTyping"
        ></v-text-field>

        <v-btn-toggle borderless v-model="ordering" class="px-2">
        <v-layout row justify-center align-center class="mr-3">
          <v-icon>mdi-alpha-b-circle</v-icon>
          <div>Ordering</div>
        </v-layout>

        <v-btn value="asc" @click="finishedTyping">
          <span class="hidden-sm-and-down">Asc</span>
          <v-icon right>
            mdi-arrow-up-bold-circle-outline
          </v-icon>
        </v-btn>
        <v-btn value="desc" @click="finishedTyping">
          <span class="hidden-sm-and-down">Desc</span>
          <v-icon right>
            mdi-arrow-down-bold-circle-outline
          </v-icon>
        </v-btn>
      </v-btn-toggle>

      </v-col>
    </v-row>
    <v-container fill-height fluid class="ma-0 pa-0">
      <v-row align="center" justify="center">
        <v-col cols="12">
          <div v-for="user in users" :key="user.id">
              <profil-card :user="user" :clickable="true">
              </profil-card>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
//import Feed from "../components/Feed.vue";
import Api from "@/api/ApiRequester";
import ProfilCard from "../components/ProfilCard.vue";

export default {
  name: "Search",
  components: {
    ProfilCard,
  },
  data() {
    return {
      users: [],
      unameQuery: "",
      delayedSearch: null,
      searchDelayMilliseconds : 150,
      ordering : "",
    };
  },
  methods: {
    async search() {
        this.unameQuery = this.unameQuery.trim();
        this.delayedSearch = null;
        if(!this.unameQuery){
            //clear users anyway
            this.users = [];
            return;
        } 
        //call search and update users
        let orderingQuery = "";
        if(this.ordering){
            orderingQuery = "&coins=" + this.ordering;
        }
        this.users = await Api.get("users/search/?username=" + this.unameQuery + orderingQuery);
    },
    finishedTyping() {
        if (this.delayedSearch != null) {
            clearTimeout(this.delayedSearch);
        }
        setTimeout(this.search, this.searchDelayMilliseconds);
    },
  },
};
</script>

<style>
</style>