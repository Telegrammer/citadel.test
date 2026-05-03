<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { loginForm } from "@/api/client";
import { setStoredAccessToken } from "@/api/storage";

const router = useRouter();

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref<string | null>(null);

async function submit() {
  error.value = null;
  loading.value = true;
  try {
    const data = await loginForm(username.value, password.value);
    setStoredAccessToken(data.access_token);
    await router.push("/profile");
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Не удалось войти";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <v-card max-width="480" class="mx-auto pa-6">
    <v-card-title>Вход</v-card-title>
    <v-card-text>
      <v-alert v-if="error" type="error" density="compact" class="mb-4">
        {{ error }}
      </v-alert>
      <v-form @submit.prevent="submit">
        <v-text-field v-model="username" label="Email" type="email" autocomplete="username" />
        <v-text-field v-model="password" label="Пароль" type="password" autocomplete="current-password" />
        <v-btn type="submit" color="primary" class="mt-2" block :loading="loading"> Войти </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>
