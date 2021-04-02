<template>
  <v-container class="ma-0 pa-0">
    <v-list class="ma-0 pa-0">
      <v-list-item class="ma-0 pa-0" v-for="bet in bets" :key="bet.id">
          <v-col xl="8"   cols="12">
        <bet-card :bet="bet" :detail="true" :clickable="true"></bet-card>
        </v-col>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import BetCard from "./BetCard.vue";
export default {
  components: { BetCard },
  props: {
    bets: null,
  },
};
</script>

<style>
</style>