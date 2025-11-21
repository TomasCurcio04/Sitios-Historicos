<template>
  <div>

    <!-- Empty state -->
    <p v-if="!loading && favorites.length === 0" class="text-center text-gray-500">
      Aún no marcaste ningún sitio como favorito.
    </p>

    <p v-if="loading">Cargando favoritos...</p>

    <div v-else class="space-y-3">
      <div
        v-for="f in favorites"
        :key="f.id"
        class="bg-white rounded shadow p-3"
      >
        <p class="font-semibold">{{ f.name }}</p>
        <p class="text-sm text-gray-500">{{ f.description }}</p>
      </div>

      <Pagination :meta="meta" @page-change="$emit('page-change', $event)" />
    </div>

  </div>
</template>

<script setup>
defineProps({
  favorites: Array,
  meta: Object,
  loading: Boolean
});
</script>
