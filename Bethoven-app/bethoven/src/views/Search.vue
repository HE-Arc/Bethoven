<template>
    <v-container fill-height fluid>
        <v-row align="center" justify="center">
            <v-col cols=6>
                <v-text-field
                label="Search friend"
                placeholder="Rajinth-xXx"
                outlined
                dense
                append-icon="mdi-magnify"
                v-model="unameQuery"
                @keyup="finishedTyping"
            ></v-text-field>
            </v-col>
        </v-row>
        <v-row align="center" justify="center">
            <v-col cols=8>
                <div v-for="user in users" :key="user.id">
                    <v-text>{{user}}</v-text>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
//import Feed from "../components/Feed.vue";
export default {
    name: "Search",
    components : {
        //Feed,
    },
    data() {
        return {
            users : {},
            unameQuery : "",
            delayedSearch : {},
        };
    },
    methods: {
        search(uname){
            return;
        },
        finishedTyping(){
            
        },
    }
}
</script>

<style>

</style>