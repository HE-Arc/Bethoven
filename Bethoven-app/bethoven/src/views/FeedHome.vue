<template>
    <v-container fill-height fluid>
        <Feed initialQuery="bets/home">
        </Feed>
    </v-container>
</template>

<script>
import Feed from "../components/Feed.vue";
export default {
    name: "FeedHome",
    components : {
        Feed,
    },
}
</script>

<style>

</style>