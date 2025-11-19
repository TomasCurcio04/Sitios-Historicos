<template>
  <div class="flex justify-between mt-4">
    <button
      class="px-3 py-1 border rounded disabled:opacity-40"
      :disabled="meta.page <= 1"
      @click="$emit('page-change', meta.page - 1)"
    >
      Anterior
    </button>

    <span class="text-sm">Página {{ meta.page }} / {{ totalPages }}</span>

    <button
      class="px-3 py-1 border rounded disabled:opacity-40"
      :disabled="meta.page >= totalPages"
      @click="$emit('page-change', meta.page + 1)"
    >
      Siguiente
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  meta: Object
});

const totalPages = computed(() =>
  Math.ceil(props.meta.total / props.meta.per_page)
);
</script>
