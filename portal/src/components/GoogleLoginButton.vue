<template>
  <div>
    <button 
      v-if="!loggedIn" 
      @click="$emit('login')" 
      class="btn-google btn-login"
    >
      Registrarse / Iniciar sesión con Google
    </button>

    <div v-else class="flex items-center space-x-2">
      

      <button 
        @click="$emit('logout')" 
        class="btn-google btn-logout"
      >
        Cerrar sesión
      </button> 
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'


const props = defineProps({
  // Estado de la sesión, manejado por useAuth y pasado por el padre
  loggedIn: {
    type: Boolean,
    default: false
  },
  // Información del usuario, manejada por useAuth y pasada por el padre
  user: {
    type: Object,
    default: null
  }
})


const emit = defineEmits([
  'login', 
  'logout' 
])

</script>

<style scoped> 
.btn-google {
  display: inline-flex; 
  align-items: center; 
  justify-content: center; 
  padding: 10px 16px; 
  border: 1px solid #ccc; 
  border-radius: 4px; 
  cursor: pointer; 
  font-weight: 500;
  transition: all 0.2s;
} 
.btn-login {
  background: white; 
  color: #4285F4; /* Azul de Google */
}
.btn-login:hover { 
  background: #f5f5f5; 
} 
.btn-logout {
  background: #DB4437; /* Rojo para Logout */
  color: white;
  border-color: #DB4437;
}
.btn-logout:hover {
  background: #c33a32;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
}
.user-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}
</style>