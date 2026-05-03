<script setup lang="ts">
import { ref } from "vue";
import { fetchJson } from "@/api/client";


const API_VIRTUAL_MACHINES_FREE_ALL = "/virtual-machines/free";

const PROTOCOLS = ["http", "socks5", "https"] as const;

const name = ref("");
const host = ref("");
const port = ref<number | null>(null);
const protocol = ref<(typeof PROTOCOLS)[number]>("http");

const loadingAdd = ref(false);
const loadingFree = ref(false);
const createdOk = ref(false);
const error = ref<string | null>(null);
const freeOk = ref<string | null>(null);

async function addVm() {
  error.value = null;
  createdOk.value = false;
  if (!name.value.trim() || !host.value.trim() || port.value == null || port.value < 1) {
    error.value = "Заполните имя, хост и порт.";
    return;
  }
  loadingAdd.value = true;
  try {
    await fetchJson<{ id: string }>("/virtual-machines/", {
      method: "POST",
      auth: true,
      body: JSON.stringify({
        name: name.value.trim(),
        host: host.value.trim(),
        port: Math.floor(Number(port.value)),
        protocol: protocol.value,
      }),
    });
    createdOk.value = true;
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Не удалось добавить ВМ";
  } finally {
    loadingAdd.value = false;
  }
}

async function freeVm() {
  error.value = null;
  freeOk.value = null;
  loadingFree.value = true;
  try {
    await fetchJson(API_VIRTUAL_MACHINES_FREE_ALL, { method: "POST", auth: true });
    freeOk.value = "Все занятые ВМ освобождены.";
    createdOk.value = false;
  } catch (e) {
    error.value = e instanceof Error ? e.message : "Не удалось освободить ВМ";
  } finally {
    loadingFree.value = false;
  }
}
</script>

<template>
  <v-card class="mx-auto pa-6" max-width="560">
    <v-card-title>Администрирование ВМ</v-card-title>
    <v-card-text>
      <v-alert v-if="error" type="error" density="compact" class="mb-4">{{ error }}</v-alert>
      <v-alert v-if="freeOk" type="success" density="compact" class="mb-4">{{ freeOk }}</v-alert>
      <v-alert v-if="createdOk" type="success" density="compact" class="mb-4"> ВМ добавлена. </v-alert>

      <h3 class="text-subtitle-1 mb-2">Добавить ВМ</h3>
      <v-text-field v-model="name" label="Имя" />
      <v-text-field v-model="host" label="Хост" />
      <v-text-field v-model.number="port" label="Порт" type="number" min="1" />
      <v-select v-model="protocol" :items="PROTOCOLS" label="Протокол" />

      <v-btn color="primary" class="mb-6" :loading="loadingAdd" @click="addVm"> Добавить </v-btn>

      <h3 class="text-subtitle-1 mb-2">Освободить все занятые ВМ</h3>
      <v-btn color="secondary" :loading="loadingFree" @click="freeVm"> Освободить все </v-btn>
    </v-card-text>
  </v-card>
</template>
