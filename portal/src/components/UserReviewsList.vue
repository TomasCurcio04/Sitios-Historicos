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

    <div v-else class="reviews-grid">
      <div
        v-for="r in reviews"
        :key="r.id"
        class="review-card"
      >
        <div class="card-header">
          <h3 class="card-title">{{ r.site_name }}</h3>
          <span 
            class="status-badge"
            :class="{
              'status-approved': isApproved(r.state || r.status),
              'status-pending': isPending(r.state || r.status),
              'status-rejected': isRejected(r.state || r.status)
            }"
          >
            {{ r.state || r.status || 'Pendiente' }}
          </span>
        </div>
        
        <div class="card-body">
          <div class="rating-section">
            <div class="stars">
              <span v-for="n in 5" :key="n" :class="n <= r.rating ? 'star-filled' : 'star-empty'">★</span>
            </div>
            <span class="rating-text">{{ r.rating }}/5</span>
          </div>
          
          <p class="review-comment">{{ r.comment }}</p>
          
          <p class="review-date">{{ formatDate(r.inserted_at) }}</p>
          
          <div class="review-actions">
            <button 
              @click="editReview(r)"
              class="action-btn edit-btn"
              :disabled="loading"
            >
              Editar
            </button>
            <button 
              @click="deleteReview(r.id)"
              class="action-btn delete-btn"
              :disabled="loading"
            >
              Eliminar
            </button>
            <router-link 
              :to="`/sites/${r.site_id}`"
              class="action-btn view-btn"
            >
              Ver sitio
            </router-link>
          </div>
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

const emit = defineEmits(['edit-review', 'delete-review', 'order-change', 'page-change']);

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

function isApproved(status) {
  return status === 'approved' || status === 'Aprobada';
}

function isPending(status) {
  return status === 'pending' || status === 'Pendiente' || !status;
}

function isRejected(status) {
  return status === 'rejected' || status === 'Rechazada';
}

function editReview(review) {
  emit('edit-review', review);
}

function deleteReview(reviewId) {
  if (confirm('¿Estás seguro de que quieres eliminar esta reseña?')) {
    emit('delete-review', reviewId);
  }
}
</script>

<style scoped>
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
  text-decoration: none;
  color: inherit;
  display: block;
  cursor: pointer;
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

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-approved {
  background-color: #22c55e !important;
  color: white !important;
}

.status-pending {
  background-color: #f59e0b !important;
  color: white !important;
}

.status-rejected {
  background-color: #ef4444 !important;
  color: white !important;
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

.review-date {
  font-size: 0.75rem;
  color: #9ca3af;
  margin: 0 0 1rem 0;
}

.review-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.edit-btn {
  background-color: #3b82f6;
  color: white;
}

.edit-btn:hover:not(:disabled) {
  background-color: #2563eb;
}

.delete-btn {
  background-color: #ef4444;
  color: white;
}

.delete-btn:hover:not(:disabled) {
  background-color: #dc2626;
}

.view-btn {
  background-color: #6b7280;
  color: white;
}

.view-btn:hover {
  background-color: #4b5563;
  text-decoration: none;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .reviews-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .review-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style>
