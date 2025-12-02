<template>
  <div class="review-modal-overlay" @click="cancel">
    <div class="review-modal" @click.stop>
      <div class="modal-header">
        <h2>Escribir reseña para {{ siteName }}</h2>
        <button class="close-btn" @click="cancel">×</button>
      </div>

      <form @submit.prevent="submitReview" class="review-form">
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
            :maxlength="500"
            rows="4"
          ></textarea>
          <div class="char-counter">
            {{ comment.length }}/500 caracteres
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
            {{ isSubmitting ? 'Enviando...' : 'Enviar reseña' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useApi } from '@/composables/useApi'

const props = defineProps({
  siteId: {
    type: Number,
    required: true
  },
  siteName: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['submitted', 'cancel'])

const { createReview } = useApi()

const rating = ref(0)
const hoverRating = ref(0)  
const comment = ref('')
const isSubmitting = ref(false)
const error = ref('')

const isFormValid = computed(() => {
  const commentLength = comment.value.trim().length
  return rating.value >= 1 && rating.value <= 5 && commentLength >= 30 && commentLength <= 500
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

    const response = await createReview(props.siteId, reviewData)

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
    } else if (err.response?.status === 500) {
      error.value = 'Error interno del servidor. Inténtalo más tarde.'
    } else {
      error.value = err.message || 'Error al enviar la reseña.'
    }
  } finally {
    isSubmitting.value = false
  }
}

const cancel = () => {
  emit('cancel')
}
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

@media (max-width: 640px) {
  .review-modal-overlay {
    padding: 0.5rem;
  }

  .modal-header,
  .review-form {
    padding: 1rem;
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
