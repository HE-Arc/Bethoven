<template>
  <v-container fill-height fluid>
    <v-row align="center" justify="center">
      <v-col align="center">
        <v-card class="mx-auto" max-width="450">
          <v-card-text>
            <v-text-field
              label="Username"
              :rules="[rules.required]"
              v-model="username"
              :disabled="loading"
              prepend-icon="mdi-account"
              class="my-5"
            ></v-text-field>
            <v-spacer></v-spacer>
            <v-text-field
              :append-icon="showPassord ? 'mdi-eye' : 'mdi-eye-off'"
              prepend-icon="mdi-lock"
              :disabled="loading"
              :rules="[rules.required, rules.min]"
              :type="showPassord ? 'text' : 'password'"
              label="Password"
              v-model="password"
              class="my-5"
              @keydown.enter="login"
              @click:append="showPassord = !showPassord"
            ></v-text-field>
            <p v-if="errorPost.length > 0" class="red--text">{{ errorPost }}</p>
          </v-card-text>
          <v-btn
            elevation="4"
            x-large
            class="primary white--text my-3"
            large
            rounded
            :loading="loading"
            v-on:click="login"
            >Login</v-btn
          >
          <v-spacer></v-spacer>
          <v-btn to="/register" text color="accent  mb-5 mt-0">
            Create an account
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Vue from "vue";
import Api from "@/api/ApiRequester";

export default Vue.extend({
  name: "Login",
  methods: {
    login: async function () {
      this.loading = true;
      try {
        await Api.login({
          username: this.username,
          password: this.password,
        });
        this.errorPost = "";

        this.$router.push({ name: "Home" });
      } catch (e) {
        this.errorPost = e.message;
      } finally {
        this.loading = false;
      }
    },
  },
  data() {
    return {
      loading: false,
      errorPost: "",
      password: "",
      username: "",
      showPassord: false,
      rules: {
        required: (value) => !!value || "Required",
        min: (v) => v.length >= 6 || "Minimum 6 characters",
      },
    };
  },
});
</script>