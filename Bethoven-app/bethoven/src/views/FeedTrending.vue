<template>
    <v-container fill-height fluid >
        <v-row justify="start" align="start">
            <v-col cols="auto">
                <v-select
                    v-model="select"
                    :hint="`${select.hint}`"
                    :items="items"
                    item-text="value"
                    item-value="value"
                    label="Ordering"
                    return-object
                    persistent-hint
                    outlined
                    v-on:change="changeOrder"
                ></v-select>
            </v-col>
        </v-row>
        <!-- Bets should always take as much place as possible to avoid the select button beeing in the middle -->
        <v-container fill-height fluid>
            <Feed initialQuery="bets" ref="feedComponent">
            </Feed>
        </v-container>
    </v-container>
</template>

<script>
import Feed from "../components/Feed.vue";
export default {
    name: "FeedTrending",
    components : {
        Feed,
    },
    beforeMount(){
        this.currentSelection = this.select;
    },
    data () {
      return {
        items: [
            { value: 'trending', hint: 'Most popular bets' },
            { value: 'hot', hint: 'Lastly created bets' },
        ],
        select: { value: 'trending', hint: 'Most popular bets' },
        currentSelection : "",
        initialQuery : "bets",
      }
    },
    methods: {
        changeOrder() {
            //avoid changing if not necessary
            if(this.select != this.currentSelection){
                this.$refs.feedComponent.updateParameters({
                    "order" : this.select.value,
                });
            }
        },
    }
}
</script>

<style>

</style>