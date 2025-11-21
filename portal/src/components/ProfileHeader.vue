<template>
  <div class="flex items-center gap-4 p-4 bg-white rounded shadow">
    <img
      v-if="user?.picture"
      :src="user.picture"
      class="w-16 h-16 rounded-full object-cover border"
    />

    <div>
      <p class="text-lg font-bold">{{ user?.name }}</p>
      <p class="text-sm text-gray-600">{{ user?.email }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  user: Object
});
</script>
