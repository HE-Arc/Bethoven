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
            ></v-text-field>
            </v-col>
        </v-row>
        <v-row align="center" justify="center">
            <v-col cols=8>
                
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
}

</script>

<style>

</style>