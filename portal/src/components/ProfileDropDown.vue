<template>
  <div class="relative" ref="dropdownRef">
    
    <!-- BOTÓN (email + avatar) -->
    <button
      @click="toggleDropdown"
      class="flex items-center space-x-2 px-3 py-1 rounded-full hover:bg-gray-100 transition text-sm"
    >

      <!-- Email -->
      <span class="text-gray-700 truncate max-w-[120px]">
        {{ user?.email }}
      </span>
    </button>

    <!-- DROPDOWN -->
    <div
      v-if="open"
      class="absolute right-0 mt-2 w-44 bg-white shadow-lg rounded-md border py-2 text-sm"
    >
      <router-link
        to="/mi-perfil"
        class="flex items-center px-3 py-2 hover:bg-gray-100 cursor-pointer"
      >
        <span class="material-icons text-base mr-2"></span>
        Mi perfil
      </router-link>

      <button
        @click="$emit('logout')"
        class="flex items-center w-full text-left px-3 py-2 hover:bg-gray-100"
      >
        <span class="material-icons text-base mr-2"></span>
        Cerrar sesión
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const props = defineProps({
  user: Object,
});

const open = ref(false);
const dropdownRef = ref(null);

const toggleDropdown = () => {
  open.value = !open.value;
};

// Cerrar al hacer click afuera
const handleClickOutside = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
    open.value = false;
  }
};

onMounted(() => document.addEventListener("click", handleClickOutside));
onBeforeUnmount(() => document.removeEventListener("click", handleClickOutside));
</script>
