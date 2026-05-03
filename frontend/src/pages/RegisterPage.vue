<script setup lang="ts">
import { ref } from "vue";
import { fetchJson } from "@/api/client";

const email = ref("");
const password = ref("");
const confirm = ref("");
const loading = ref(false);
const sent = ref(false);
const error = ref<string | null>(null);

async function submit() {
  error.value = null;
  if (password.value !== confirm.value) {
    error.value = "Пароли не совпадают.";
    return;
  }
  loading.value = true;
  try {
    await fetchJson<{ id: string }>("/users/", {
      method: "POST",
      body: JSON.stringify({ email: email.value, password: password.value }),
    });
    sent.value = true;
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Не удалось зарегистрироваться";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <v-card max-width="480" class="mx-auto pa-6">
    <v-card-title>Регистрация</v-card-title>
    <v-card-text>
      <v-alert v-if="sent" type="success" density="compact" class="mb-4">
        Письмо с ключом отправлено на почту.
      </v-alert>
      <v-alert v-if="error" type="error" density="compact" class="mb-4">
        {{ error }}
      </v-alert>
      <v-form @submit.prevent="submit">
        <v-text-field v-model="email" label="Email" type="email" autocomplete="email" />
        <v-text-field v-model="password" label="Пароль" type="password" autocomplete="new-password" />
        <v-text-field
          v-model="confirm"
          label="Повтор пароля"
          type="password"
          autocomplete="new-password"
        />
        <v-btn type="submit" color="primary" class="mt-2" block :loading="loading" :disabled="sent">
          Зарегистрироваться
        </v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>
