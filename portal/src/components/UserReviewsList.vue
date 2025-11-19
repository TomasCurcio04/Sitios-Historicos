<template>
  <div>

    <!-- Orden -->
    <div class="flex justify-end mb-2">
      <select
        class="border p-1 text-sm rounded"
        v-model="localOrder"
        @change="$emit('order-change', localOrder)"
      >
        <option value="desc">Más recientes</option>
        <option value="asc">Más antiguas</option>
      </select>
    </div>

    <!-- Loading -->
    <p v-if="loading">Cargando reseñas...</p>

    <!-- Empty state -->
    <p v-else-if="reviews.length === 0" class="text-center text-gray-500">
      Aún no escribiste reseñas.
    </p>

    <!-- Listado -->
    <div v-else class="space-y-3">
      <div
        v-for="r in reviews"
        :key="r.id"
        class="bg-white rounded shadow p-3"
      >
        <p class="font-semibold">{{ r.site_name }}</p>
        <p class="text-sm text-yellow-600">⭐ {{ r.rating }}/5</p>
        <p class="text-xs text-gray-500">Fecha: {{ formatDate(r.date_created) }}</p>

        <p class="mt-1 text-sm line-clamp-2">
          {{ r.comment }}
        </p>
      </div>

      <Pagination :meta="meta" @page-change="$emit('page-change', $event)" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Pagination from "./Pagination.vue";

const props = defineProps({
  reviews: Array,
  meta: Object,
  loading: Boolean,
  order: String
});

const localOrder = ref(props.order);

function formatDate(date) {
  return new Date(date).toLocaleDateString("es-AR");
}
</script>
