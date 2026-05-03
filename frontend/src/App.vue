<script setup lang="ts">
import { ref, watch } from "vue";
import { useRoute } from "vue-router";
import { getStoredAccessToken } from "./api/storage";

const route = useRoute();
const hasToken = ref(Boolean(getStoredAccessToken()));
watch(
  () => route.fullPath,
  () => {
    hasToken.value = Boolean(getStoredAccessToken());
  },
);
</script>

<template>
  <v-app>
    <v-app-bar color="primary" density="comfortable">
      <v-app-bar-title>Citadel</v-app-bar-title>
      <v-spacer />
      <v-btn to="/register" variant="text">Регистрация</v-btn>
      <v-btn to="/login" variant="text">Вход</v-btn>
      <v-btn to="/profile" variant="text" :disabled="!hasToken">Профиль</v-btn>
      <v-btn to="/admin/vm" variant="text" :disabled="!hasToken">Админ ВМ</v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid class="py-6">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>
