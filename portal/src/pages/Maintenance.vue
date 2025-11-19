<template>
  <div class="maintenance-container">
    <div class="maintenance-content">
      <div class="maintenance-icon">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L13.09 8.26L22 9L13.09 9.74L12 16L10.91 9.74L2 9L10.91 8.26L12 2Z" stroke="currentColor" stroke-width="2" fill="none"/>
          <path d="M12 12L13.09 18.26L22 19L13.09 19.74L12 26L10.91 19.74L2 19L10.91 18.26L12 12Z" stroke="currentColor" stroke-width="2" fill="none"/>
        </svg>
      </div>
      
      <h1 class="maintenance-title">Portal en Mantenimiento</h1>
      
      <div class="maintenance-message">
        <p v-if="message">{{ message }}</p>
        <p v-else>
          Estamos realizando tareas de mantenimiento. 
          Por favor, inténtalo de nuevo más tarde.
        </p>
      </div>
      
      <div class="maintenance-actions">
        <button @click="checkStatus" class="retry-button" :disabled="checking">
          <span v-if="checking">Verificando...</span>
          <span v-else>Verificar Estado</span>
        </button>
      </div>
      
      <div class="maintenance-footer">
        <p>Gracias por tu paciencia</p>
      </div>
    </div>
  </div>
</template>

<script>
import { getPortalStatus } from '../services/featureFlags.js'

export default {
  name: 'MaintenancePage',
  
  props: {
    message: {
      type: String,
      default: null
    }
  },
  
  data() {
    return {
      checking: false
    }
  },
  
  methods: {
    async checkStatus() {
      this.checking = true
      try {
        const status = await getPortalStatus()
        if (status.enabled) {
          // Portal está disponible, recargar la página
          window.location.reload()
        }
      } catch (error) {
        console.error('Error checking portal status:', error)
      } finally {
        this.checking = false
      }
    }
  }
}
</script>

<style scoped>
.maintenance-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.maintenance-content {
  background: white;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.maintenance-icon {
  color: #667eea;
  margin-bottom: 24px;
}

.maintenance-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 16px;
}

.maintenance-message {
  color: #4a5568;
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 32px;
}

.maintenance-actions {
  margin-bottom: 24px;
}

.retry-button {
  background: #667eea;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-button:hover:not(:disabled) {
  background: #5a67d8;
  transform: translateY(-1px);
}

.retry-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.maintenance-footer {
  color: #718096;
  font-size: 0.9rem;
}

@media (max-width: 640px) {
  .maintenance-content {
    padding: 24px;
  }
  
  .maintenance-title {
    font-size: 1.5rem;
  }
  
  .maintenance-message {
    font-size: 1rem;
  }
}
</style>