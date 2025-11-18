<template>
  <div>
    <button v-if="!loggedIn" @click="loginWithGoogle">
      Registrarse / Iniciar sesión con Google
    </button>

    <div v-else>
      <p>Sesión iniciada como: {{ user?.email }}</p>

      <img 
        v-if="user?.picture" 
        :src="user.picture" 
        alt="Foto de perfil"
        style="width: 40px; height: 40px; border-radius: 50%;"
      />

      <button @click="logout">
        Cerrar sesión
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// URL del backend tomada desde .env
const API_URL = import.meta.env.VITE_API_URL

const loggedIn = ref(false)
const user = ref(null)

// Consultar estado de sesión
onMounted(async () => {
  const res = await fetch(`${API_URL}/google/status`, {
    credentials: 'include'
  })
  const data = await res.json()

  loggedIn.value = data.logged_in
  user.value = data.user || null
})

// Iniciar sesión
const loginWithGoogle = () => {
  const current = window.location.href
  window.location.href = `${API_URL}/google/login?next=${encodeURIComponent(current)}`
}

// Cerrar sesión
const logout = () => {
  const current = window.location.href
  window.location.href = `${API_URL}/google/logout?next=${encodeURIComponent(current)}`
}
</script>

<style scoped>
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
