<template>
    <v-app>
        <!-- <Drawer :avatarTimestamp="this.$typedStore.state.avatarTimestamp"/> -->
        <v-main>
            <Header />
            <router-view></router-view>
            <Navbar />
        </v-main>
    </v-app>
</template>

<script>
import Vue from "vue";
import Header from "@/components/Header.vue";
import Navbar from "@/components/Navbar.vue";
import "@/assets/styles/main.scss";

export default Vue.extend({
    name: "App",
    components: { Header,Navbar }
});
</script>
