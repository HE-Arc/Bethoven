<template>
  <v-col cols="12" >
      <div  v-on:argless="test">a</div>
    <v-alert dense :type="type" :value="activated" dismissible @display-alert="activate" @test="test">
      {{ message }}
    </v-alert>
  </v-col>
</template>

<script>

import Api from "@/api/ApiRequester";

export default {
    Level : {
        Warning: "warning",
        Success: "success",
        Info: "info",
        Error: "Error",
    },
    beforeMount(){
        let eventBus = Api.getEventBus();
        eventBus.$on("test", this.test);
        
    },
    data() {
        return {
        type: "success",
        message: "Placeholder",
        activated: false,
        };
    },
    methods: {
        activate(level, message) {
            console.log("Coucou from activate");
            this.type = level;
            this.message = message;
            this.activated = true;
            setTimeout(() => {
                if (this.activated) this.activated = false;
            }, 2500);
        },
        test : function() {
            console.log("without arguments");
        }
    },
};
</script>

<style>

</style>