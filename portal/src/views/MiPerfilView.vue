<template>
  <div class="container mx-auto py-10">

    <!-- Cargando estado de sesión -->
    <div v-if="loading" class="text-center">
      <p class="text-gray-600">Cargando...</p>
    </div>

    <!-- SI NO ESTÁ LOGUEADO -->
    <div v-else-if="!loggedIn" class="text-center">
      <h2 class="text-2xl font-bold mb-4">Mi Perfil</h2>
      <p class="mb-4 text-gray-600">
        Inicia sesión para ver tu perfil, tus reseñas y tus favoritos.
      </p>

      <GoogleLoginButton />
    </div>

    <!-- SI ESTÁ LOGUEADO -->
    <div v-else>

      <!-- Información del usuario -->
      <div class="flex items-center gap-4 mb-8">
        <img 
          :src="user.picture" 
          alt="Foto de usuario"
          class="w-16 h-16 rounded-full object-cover"
        />

        <div>
          <h2 class="text-xl font-bold">{{ user.name }}</h2>
          <p class="text-gray-600">{{ user.email }}</p>
        </div>
      </div>

      <!-- Reviews -->
      <h3 class="text-lg font-semibold mb-2">Mis Reseñas</h3>
      <ReviewsList />

      <!-- Favoritos -->
      <h3 class="text-lg font-semibold mt-10 mb-2">Mis Favoritos</h3>
      <FavoritesList />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import GoogleLoginButton from '../components/GoogleLoginButton.vue'
import ReviewsList from '../components/UserReviewsList.vue'
import FavoritesList from '../components/UserFavoritesList.vue'

const API_URL = import.meta.env.VITE_API_URL

const loggedIn = ref(false)
const user = ref(null)
const loading = ref(true)

// Función de consulta reutilizable
const checkSession = async () => {
  const res = await fetch(`${API_URL}/google/status`, {
    credentials: 'include'
  })

  const data = await res.json()

  loggedIn.value = data.logged_in
  user.value = data.user
}

onMounted(async () => {
  // Primer llamada
  await checkSession()

  // Si no está logueado, hacer retry
  if (!loggedIn.value) {
    setTimeout(async () => {
      await checkSession()
      loading.value = false
    }, 300)
  } else {
    loading.value = false
  }
})
</script>
