<template>
  <v-container fill-height fluid>
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

        <v-btn-toggle borderless v-model="ordering">
        <v-layout row justify-center align-center class="mr-3">
          <v-icon>mdi-alpha-b-circle</v-icon>
          <div>Ordering</div>
        </v-layout>

        <v-btn value="asc">
          <span class="hidden-sm-and-down">Asc</span>
          <v-icon right>
            mdi-format-align-left
          </v-icon>
        </v-btn>
        <v-btn value="desc">
          <span class="hidden-sm-and-down">Desc</span>
          <v-icon right>
            mdi-format-align-right
          </v-icon>
        </v-btn>
      </v-btn-toggle>

      </v-col>
    </v-row>
    <v-row align="center" justify="center">
      <v-col cols="8">
        <div v-for="user in users" :key="user.id">
          <h2>{{ user.username }} coins : {{user.coins}}</h2>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
//import Feed from "../components/Feed.vue";
import Api from "@/api/ApiRequester";

export default {
  name: "Search",
  components: {
    //Feed,
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