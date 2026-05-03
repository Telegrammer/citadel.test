<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { fetchJson } from "@/api/client";
import { clearStoredAccessToken } from "@/api/storage";

const router = useRouter();

type Profile = { email: string; created_at: string; is_admin: boolean };

const profile = ref<Profile | null>(null);
const loading = ref(false);
const error = ref<string | null>(null);
const keyMsg = ref<string | null>(null);
const passCurrent = ref("");
const passNew = ref("");
const passMsg = ref<string | null>(null);

async function load() {
  error.value = null;
  loading.value = true;
  try {
    profile.value = await fetchJson<Profile>("/users/profile", { auth: true });
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Ошибка загрузки профиля";
    if (/Некорректные учетные данные|401|unauthorized/i.test(error.value)) {
      await router.push("/login");
    }
  } finally {
    loading.value = false;
  }
}

async function refreshKey() {
  keyMsg.value = null;
  error.value = null;
  try {
    await fetchJson<{ email: string }>("/users/activation-key", { method: "PATCH", auth: true });
    keyMsg.value = "Ключ обновлён; новое значение отправлено на почту.";
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Не удалось обновить ключ";
  }
}

async function changePassword() {
  passMsg.value = null;
  error.value = null;
  try {
    await fetchJson("/users/password", {
      method: "PATCH",
      auth: true,
      body: JSON.stringify({
        current_password: passCurrent.value,
        new_password: passNew.value,
      }),
    });
    passMsg.value = "Пароль изменён.";
    passCurrent.value = "";
    passNew.value = "";
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Не удалось сменить пароль";
  }
}

function logout() {
  clearStoredAccessToken();
  void router.push("/login");
}

onMounted(() => {
  void load();
});
</script>

<template>
  <div class="mx-auto" style="max-width: 520px">
    <v-alert v-if="error" type="error" density="compact" class="mb-4">{{ error }}</v-alert>

    <v-card v-if="loading" variant="flat" class="pa-8 text-center">
      Загрузка…
    </v-card>

    <template v-else-if="profile">
      <v-card class="pa-6 mb-4">
        <v-card-title>Профиль</v-card-title>
        <v-card-text>
          <div><strong>Email:</strong> {{ profile.email }}</div>
          <div class="mt-2"><strong>Администратор:</strong> {{ profile.is_admin ? "да" : "нет" }}</div>
          <div class="mt-2 text-caption">Создан: {{ profile.created_at }}</div>
          <div class="mt-4 d-flex flex-wrap ga-2">
            <v-btn color="secondary" @click="refreshKey"> Обновить ключ </v-btn>
            <v-btn variant="text" @click="logout"> Выйти </v-btn>
          </div>
          <v-alert v-if="keyMsg" type="success" density="compact" class="mt-4">{{ keyMsg }}</v-alert>
        </v-card-text>
      </v-card>

      <v-card class="pa-6">
        <v-card-title>Смена пароля</v-card-title>
        <v-card-text>
          <v-text-field v-model="passCurrent" label="Текущий пароль" type="password" autocomplete="current-password" />
          <v-text-field v-model="passNew" label="Новый пароль" type="password" autocomplete="new-password" />
          <v-btn color="primary" class="mt-2" @click="changePassword"> Сменить пароль </v-btn>
          <v-alert v-if="passMsg" type="success" density="compact" class="mt-4">{{ passMsg }}</v-alert>
        </v-card-text>
      </v-card>
    </template>
  </div>
</template>
