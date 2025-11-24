<template>
  <div id="app-layout">
    
    <header class="w-full shadow-md p-4 sticky top-0 z-10" style="background-color: #dcfce7;">
      <!-- Header vacío -->
    </header>

    <!-- Portada en todas las páginas -->
    <SearchHero @search="handleSearch" />

    <!-- Menú dropdown debajo de la portada -->
    <div class="px-4 py-6" style="background-color: #ecfdf5;">
      <div class="max-w-7xl mx-auto">
        <div style="display: grid; grid-template-columns: auto 1fr auto; align-items: center; width: 100%;">
        <!-- Menú principal -->
        <div class="relative">
          <button 
            @click="showDropdown = !showDropdown"
            class="px-4 py-2 text-gray-700 rounded-lg"
            style="background-color: #bbf7d0;"
            @mouseover="$event.target.style.backgroundColor='#a7f3d0'"
            @mouseout="$event.target.style.backgroundColor='#bbf7d0'"
          >
            Menú
          </button>
          
          <div v-if="showDropdown" class="absolute top-full mt-2 bg-white rounded-lg shadow-lg border min-w-48 z-20">
            <div class="py-2" style="display: flex; flex-direction: column;">
              <router-link to="/" class="block px-4 py-2 text-gray-700 hover:bg-green-100" style="display: block; width: 100%;">
                🏠 Inicio
              </router-link>
              
              <router-link to="/sites-list" class="block px-4 py-2 text-gray-700 hover:bg-green-100" style="display: block; width: 100%;">
                🏛️ Sitios Históricos
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Espacio vacío -->
        <div></div>
        
        <!-- Botones de usuario a la derecha -->
        <div class="flex items-center gap-2">
          <template v-if="loading">
            <span class="text-gray-500 text-sm">Cargando...</span>
          </template>
          
          <template v-else-if="loggedIn">
            <div class="relative">
              <button 
                @click="showUserDropdown = !showUserDropdown"
                class="text-gray-700 hover:text-blue-600 text-sm"
              >
                👤 {{ user?.name || 'Mi Perfil' }}
              </button>
              
              <div v-if="showUserDropdown" class="absolute top-full right-0 mt-2 bg-white rounded-lg shadow-lg border min-w-48 z-20">
                <div class="py-2 user-dropdown">
                  <router-link to="/mi-perfil" class="block w-full px-4 py-2 text-gray-700 hover:bg-green-100 text-right">
                    👤 Mi Perfil
                  </router-link>
                  <button @click="logout" class="block w-full text-right px-4 py-2 text-gray-700 hover:bg-green-100">
                    🚪 Cerrar Sesión
                  </button>
                </div>
              </div>
            </div>
          </template>
          
          <template v-else>
            <button @click="login" class="text-gray-700 hover:text-green-600 text-sm">
              🔑 Iniciar Sesión
            </button>
          </template>
        </div>
        </div>
      </div>
    </div>

    <main class="max-w-7xl mx-auto p-4">
      <RouterView /> 
    </main>

  </div>
</template>

<script setup>
// --- 1. Importaciones ---
import { ref } from 'vue'
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import SearchHero from '@/components/SearchHero.vue'

const { loggedIn, user, loading, login, logout } = useAuth()
const showDropdown = ref(false)
const showUserDropdown = ref(false)
const router = useRouter()

// Función de búsqueda
const handleSearch = (query) => {
  router.push({
    name: 'sites-list',
    query: { q: query }
  })
}
</script>

<style>
/* Aquí puedes importar tus estilos globales si es necesario */
/* @import '@/assets/main.css'; */ 

/* Forzar layout vertical en dropdowns */
.user-dropdown {
  display: flex !important;
  flex-direction: column !important;
}

.user-dropdown > * {
  display: block !important;
  width: 100% !important;
  text-align: right !important;
  padding: 0.5rem 1rem !important;
  margin: 0 !important;
  border: none !important;
  background: none !important;
}
</style>