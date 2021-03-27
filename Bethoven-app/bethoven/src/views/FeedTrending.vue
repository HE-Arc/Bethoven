<template>
    <v-container fill-height fluid>
        <Feed initialQuery="bets">
        </Feed>
    </v-container>
</template>

<script>
import Feed from "../components/Feed.vue";
export default {
    name: "FeedTrending",
    components : {
        Feed,
    },
}
</script>

<style>

</style>