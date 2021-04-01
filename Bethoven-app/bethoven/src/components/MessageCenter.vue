<template>
  <v-col class="foreground" cols="12">
    <v-alert  dense :type="type" :value="activated" dismissible @display-alert="activate" @click="activated=false">
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
        eventBus.$on("alert-event", this.activate);
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
            this.type = level;
            this.message = message;
            this.activated = true;
            setTimeout(() => {
                if (this.activated) this.activated = false;
            }, 10000);
        },
    },
};
</script>

<style>
.foreground{
  position: fixed;  
  z-index:100;
}
</style>