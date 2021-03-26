<template>
    <v-container fill-height fluid>
        <Feed initialQuery="bets/mybet">
        </Feed>
    </v-container>
</template>

<script>
import Feed from "../components/Feed.vue";
export default {
    name: "FeedMybet",
    components : {
        Feed,
    },
}
</script>

<style>

</style>