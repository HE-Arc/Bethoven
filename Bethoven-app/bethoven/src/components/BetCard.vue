<!-- TEMPLATE -->
<template>
  <div>
    <v-card>
      <!-- Title and text -->
      <v-card-title>{{ bet.title }}</v-card-title>
      <v-card-text>{{ bet.description }}</v-card-text>

      <!-- 'bet' part with choices and bet buttons -->
      <v-row no-gutters>
        <v-col>
          <v-card class="pa-2" outlined tile> 
            One 
          </v-card>
        </v-col>
        <v-col>
          <v-card class="pa-2" outlined tile> 
            Two 
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>


<!-- SCRIPT -->
<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";

export default Vue.extend({
  name: "BetCard",
  props: {
    bet: {},
  },
  computed: {},
  methods: {
    getID() {
      return this.bet.id;
    },
  },
});
</script> 