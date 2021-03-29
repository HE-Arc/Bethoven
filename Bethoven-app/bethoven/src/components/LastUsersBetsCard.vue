<template>
  <v-container >
        <v-card class="ma-2 pt-1">
            <v-list>
                <v-list-item v-for="bet in bets" :key="bet.id">
                    <bet-card :bet="bet" :detail="true" :clickable="true"></bet-card>
                </v-list-item>
            </v-list>
        </v-card>
    </v-container>
</template>

<script>
import BetCard from './BetCard.vue'
export default {
  components: { BetCard },
    props:{
        bets:null,
    }
}
</script>

<style>

</style>