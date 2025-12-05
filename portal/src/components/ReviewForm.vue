<template>
  <div class="review-modal-overlay" @click="cancel">
    <div class="review-modal" @click.stop>
      <div class="modal-header">
        <h2>{{ isEditing ? 'Editar reseña' : 'Escribir reseña' }} para {{ siteName }}</h2>
        <button class="close-btn" @click="cancel">×</button>
      </div>

      <div v-if="!reviewsEnabled" class="reviews-disabled-message">
        <div class="disabled-icon">🚫</div>
        <h3>Reseñas no disponibles</h3>
        <p>{{ disabledMessage || 'Las reseñas están temporalmente deshabilitadas.' }}</p>
        <button type="button" class="btn-cancel" @click="cancel">
          Cerrar
        </button>
      </div>

      <form v-else @submit.prevent="submitReview" class="review-form">
        <div class="form-group">
          <label class="rating-label">Calificación:</label>
          <div class="stars-container">
            <button
              v-for="n in 5"
              :key="n"
              type="button"
              class="star-btn"
              :class="{ active: n <= (hoverRating || rating) }"
              @click="setRating(n)"
              @mouseover="setHover(n)"
              @mouseleave="clearHover"

            >
              ★
            </button>
          </div>
          <span class="rating-text">{{ rating }}/5</span>
        </div>

        <div class="form-group">
          <label for="comment">Comentario:</label>
          <textarea
            id="comment"
            v-model="comment"
            placeholder="Comparte tu experiencia visitando este sitio histórico..."
            :maxlength="1000"
            rows="4"
          ></textarea>
          <div class="char-counter" :class="{ 'char-counter-invalid': comment.trim().length < 20 && comment.trim().length > 0 }">
            {{ comment.length }}/1000 caracteres
            <span v-if="comment.trim().length < 20 && comment.trim().length > 0" class="min-chars-warning">
              (mínimo 20 caracteres)
            </span>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <div class="form-actions">
          <button type="button" class="btn-cancel" @click="cancel" :disabled="isSubmitting">
            Cancelar
          </button>
          <button type="submit" class="btn-submit" :disabled="!isFormValid || isSubmitting">
            {{ isSubmitting ? (isEditing ? 'Actualizando...' : 'Enviando...') : (isEditing ? 'Actualizar reseña' : 'Enviar reseña') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const props = defineProps({
  siteId: {
    type: Number,
    required: true
  },
  siteName: {
    type: String,
    required: true
  },
  existingReview: {
    type: Object,
    default: null
  },
  isEditing: {
    type: Boolean,
    default: false
  },
  useProfileEndpoint: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submitted', 'cancel'])

const { createReview, updateReview, updateMyReview, getReviewsStatus } = useApi()

const rating = ref(0)
const hoverRating = ref(0)  
const comment = ref('')
const isSubmitting = ref(false)
const error = ref('')
const reviewsEnabled = ref(true)
const disabledMessage = ref('')

const isFormValid = computed(() => {
  const commentLength = comment.value.trim().length
  return rating.value >= 1 && rating.value <= 5 && commentLength >= 20 && commentLength <= 1000
})

const setRating = (newRating) => {
  rating.value = newRating
}
const setHover = (n) => {
  hoverRating.value = n
}

const clearHover = () => {
  hoverRating.value = 0
}

const submitReview = async () => {
  if (!isFormValid.value) {
    error.value = 'Por favor verifica los datos del formulario.'
    return
  }

  isSubmitting.value = true
  error.value = ''

  try {
    const reviewData = {
      rating: rating.value,
      comment: comment.value.trim()
    }

    let response
    if (props.isEditing && props.existingReview) {
      if (props.useProfileEndpoint) {
        response = await updateMyReview(props.siteId, props.existingReview.id, reviewData)
      } else {
        response = await updateReview(props.siteId, props.existingReview.id, reviewData)
      }
    } else {
      response = await createReview(props.siteId, reviewData)
    }

    if (response.status === 201 || response.status === 200) {
      emit('submitted', response.data)
    } else {
      throw new Error('Respuesta inesperada del servidor')
    }
  } catch (err) {
    if (err.response?.status === 401) {
      error.value = 'Sesión expirada. Por favor inicia sesión nuevamente.'
    } else if (err.response?.status === 400) {
      error.value = err.response.data?.error?.message || 'Datos inválidos.'
    } else if (err.response?.status === 409) {
      error.value = err.response.data?.error?.message || 'Ya tienes una reseña para este sitio.'
    } else if (err.response?.status === 403) {
      error.value = err.response.data?.error?.message || 'No tienes permisos para realizar esta acción.'
    } else if (err.response?.status === 500) {
      error.value = 'Error interno del servidor. Inténtalo más tarde.'
    } else {
      error.value = err.message || (props.isEditing ? 'Error al actualizar la reseña.' : 'Error al enviar la reseña.')
    }
  } finally {
    isSubmitting.value = false
  }
}

const cancel = () => {
  emit('cancel')
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

onMounted(() => {
  checkReviewsStatus()
  
  // Si estamos editando, cargar los datos existentes
  if (props.isEditing && props.existingReview) {
    rating.value = props.existingReview.rating
    comment.value = props.existingReview.comment
  }
})
</script>

<style scoped>
.review-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.review-modal {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #f3f4f6;
}

.review-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.rating-label {
  margin-bottom: 0.75rem;
}

.stars-container {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.star-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #d1d5db;
  transition: color 0.2s;
  padding: 0.25rem;
  border-radius: 0.25rem;
}

.star-btn:hover,
.star-btn.active {
  color: #fbbf24;
}

.rating-text {
  font-size: 0.875rem;
  color: #6b7280;
}

textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
  transition: border-color 0.2s;
}

textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.char-counter {
  text-align: right;
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.char-counter-invalid {
  color: #dc2626;
}

.min-chars-warning {
  color: #dc2626;
  font-weight: 500;
}

.error-message {
  background-color: #fef2f2;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
}

.btn-cancel,
.btn-submit {
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-cancel {
  background-color: #f3f4f6;
  color: #374151;
}

.btn-cancel:hover:not(:disabled) {
  background-color: #e5e7eb;
}

.btn-submit {
  background-color: #3b82f6;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-submit:disabled,
.btn-cancel:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.reviews-disabled-message {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.disabled-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.reviews-disabled-message h3 {
  margin: 0 0 1rem 0;
  color: #374151;
  font-size: 1.25rem;
}

.reviews-disabled-message p {
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
}

@media (max-width: 640px) {
  .review-modal-overlay {
    padding: 0.5rem;
  }

  .modal-header,
  .review-form {
    padding: 1rem;
  }

  .reviews-disabled-message {
    padding: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-cancel,
  .btn-submit {
    width: 100%;
  }
}
</style>
