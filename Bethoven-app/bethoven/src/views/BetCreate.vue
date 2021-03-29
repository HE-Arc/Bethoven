<template>
<bet-create-card></bet-create-card>
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";
import BetCreateCard from "../components/BetCreateCard.vue";
export default Vue.extend({
  components: { BetCreateCard },
    name: "Home",
});
</script>

<style>

</style>