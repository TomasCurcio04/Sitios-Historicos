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

    <p v-if="loading">Cargando reseñas...</p>

    <p v-else-if="reviews.length === 0" class="text-center text-gray-500">
      Aún no escribiste reseñas.
    </p>

    <div v-else class="space-y-3">
      <div
        v-for="r in reviews"
        :key="r.id"
        class="bg-white rounded shadow p-3"
      >
        <p class="font-semibold">{{ r.site_name }}</p>
        <p class="text-sm text-yellow-600">⭐ {{ r.rating }}/5</p>
        <p class="text-xs text-gray-500">Fecha: {{ formatDate(r.inserted_at) }}</p>
        <p class="mt-1 text-sm line-clamp-2">
          {{ r.comment }}
        </p>
      </div>
    </div>

    <!-- Paginación -->
    <div
      v-if="meta && meta.total_pages > 1"
      class="flex justify-between items-center mt-4"
    >
      <button
        class="px-3 py-1 border rounded disabled:opacity-50"
        :disabled="meta.current_page <= 1"
        @click="$emit('page-change', meta.current_page - 1)"
      >
        Anterior
      </button>

      <span class="text-sm text-gray-600">
        Página {{ meta.current_page }} de {{ meta.total_pages }}
      </span>

      <button
        class="px-3 py-1 border rounded disabled:opacity-50"
        :disabled="meta.current_page >= meta.total_pages"
        @click="$emit('page-change', meta.current_page + 1)"
      >
        Siguiente
      </button>
    </div>
  </div>
</template>
<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  reviews: Array,
  meta: Object,
  loading: Boolean,
  order: {
    type: String,
    default: "desc" 
  }
});

// Inicializamos con la prop "order" o 'desc' por defecto
const localOrder = ref(props.order || "desc");

// Si la prop cambia desde el padre, actualizamos localOrder
watch(() => props.order, (newVal) => {
  localOrder.value = newVal || "desc";
});

function formatDate(dateStr) {
  if (!dateStr) return 'Sin fecha';

  const date = new Date(dateStr);

  if (isNaN(date)) return 'Fecha inválida';

  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();

  return `${day}/${month}/${year}`;
}
</script>
