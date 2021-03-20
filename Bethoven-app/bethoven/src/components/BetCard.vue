<!-- TEMPLATE -->
<template>
  <div>
    <v-card class="ma-1">
      <!-- Title and text -->
      <v-card-title>{{ bet.title }}</v-card-title>
      <v-card-text>{{ bet.description }}</v-card-text>

      <!-- 'bet' part with choices and bet buttons -->
      <v-card-subtitle class="pa-0 text-center">
        Total votes : {{ bet.bet_ratio.total }}
      </v-card-subtitle>
      <v-progress-linear
        background-color="teamA"
        color="teamB"
        :value="bet.bet_ratio.ratio[0]"
      ></v-progress-linear>

      <!-- Tab -->
      <v-row no-gutters>
        <v-col>
          <!--Choice 1-->
          <v-card outlined tile>
            <v-col class="text-right">
              <v-card-subtitle class="pa-1">{{ bet.choice1 }}</v-card-subtitle>
              <v-card-subtitle class="pa-1"
                >{{ bet.bet_ratio.ratio[0] }} %</v-card-subtitle
              >
            </v-col>
          </v-card>
        </v-col>
        <v-col>
          <!--Choice 2-->
          <v-card outlined tile>
            <v-col class="text-left">
              <v-card-subtitle class="pa-1">{{ bet.choice2 }}</v-card-subtitle>
              <v-card-subtitle class="pa-1"
                >{{ bet.bet_ratio.ratio[1] }} %</v-card-subtitle
              >
            </v-col>
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