<template>
   <!-- <div v-if="!reviewsEnabled" class="reviews-disabled-message">
        <div class="disabled-icon">🚫</div>
        <h3>Reseñas no disponibles</h3>
        <p>{{ disabledMessage || 'Las reseñas están temporalmente deshabilitadas.' }}</p>
        <button type="button" class="btn-cancel" @click="cancel">
          Cerrar
        </button>
      </div> -->
  <div v-if="!reviewsEnabled" class="reviews-disabled-message">
    <div class="disabled-icon">🚫</div>
      <h3>Reseñas no disponibles</h3>
        <p>{{ disabledMessage }}</p>
        <button type="button" class="btn-inicio" @click="goBack">
          Inicio
        </button>
  </div>
  <div v-else class="site-reviews-section">
    <h3>Reseñas del sitio</h3>

    <p v-if="loading">Cargando reseñas...</p>

    <p v-else-if="reviews.length === 0" class="text-center text-gray-500">
      Aún no hay reseñas para este sitio.
    </p>

    <div v-else class="reviews-grid">
      <div
        v-for="r in reviews"
        :key="r.id"
        class="review-card"
      >
        <div class="card-header"> 
          <h4 class="card-title">{{ r.user_name }}</h4>
          <span class="review-date">{{ formatDate(r.inserted_at) }}</span>
        </div>

        <div class="card-body">
          <div class="rating-section">
            <div class="stars">
              <span v-for="n in 5" :key="n" :class="n <= r.rating ? 'star-filled' : 'star-empty'">★</span>
            </div>
            <span class="rating-text">{{ r.rating }}/5</span>
          </div>

          <p class="review-comment">{{ r.comment }}</p>
        </div>
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
import { ref, watch, onMounted } from "vue";
import { useApi } from '@/composables/useApi'

const { getReviewsStatus } = useApi()

const reviewsEnabled = ref(true)
const disabledMessage = ref("")

const emit = defineEmits(['goBack']) 

onMounted(() => {
  checkReviewsStatus()
})
const props = defineProps({
  reviews: Array,
  meta: Object,
  loading: Boolean
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

const goBack = () => {
  emit('goBack')
}
const checkReviewsStatus = async () => {
  try {
    const response = await getReviewsStatus()
    reviewsEnabled.value = response.data.enabled
    disabledMessage.value = response.data.message || ''
  } catch (err) {
    console.error('Error checking reviews status:', err)
    // En caso de error, permitir reviews por defecto
    reviewsEnabled.value = true
  }
}
</script>

<style scoped>
.site-reviews-section h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.review-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.review-date {
  font-size: 0.75rem;
  color: #9ca3af;
}

.card-body {
  padding: 1rem;
}

.rating-section {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.stars {
  display: flex;
  margin-right: 0.5rem;
}

.star-filled {
  color: #fbbf24;
}

.star-empty {
  color: #d1d5db;
}

.rating-text {
  font-size: 0.875rem;
  color: #6b7280;
}

.review-comment {
  color: #374151;
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .reviews-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>
