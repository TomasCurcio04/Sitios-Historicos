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
        <p class="text-xs text-gray-500">Fecha: {{ formatDate(f.date) }}</p>
      </div>

      <Pagination :meta="meta" @page-change="$emit('page-change', $event)" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  favorites: Array,
  meta: Object,
  loading: Boolean,
  order: {
    type: String,
    default: 'desc'
  }
})

const localOrder = ref(props.order)

watch(() => props.order, (newVal) => {
  localOrder.value = newVal
})

function formatDate(dateStr) {
  if (!dateStr) return 'Sin fecha'

  const date = new Date(dateStr)
  if (isNaN(date)) return 'Fecha inválida'

  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()

  return `${day}/${month}/${year}`
}
</script>
