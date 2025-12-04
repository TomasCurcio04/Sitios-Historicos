<template>
  <div class="container mx-auto py-10 max-w-3xl">

    <div v-if="loading" class="text-center py-10">
      <p class="text-gray-600 text-lg">Cargando perfil...</p>
    </div>

    <div v-else-if="!loggedIn" class="text-center space-y-4">
      <h2 class="text-3xl font-bold">Mi Perfil</h2>

      <p class="text-gray-600">
        Inicia sesión para ver tu perfil, tus reseñas y tus favoritos.
      </p>

      <div class="flex justify-center">
        <GoogleLoginButton 
          :logged-in="loggedIn" 
          :user="user" 
          @login="login" 
          @logout="logout" 
        />
      </div>
    </div>

    <div v-else class="space-y-8">

      <div class="border-b flex gap-6">
        <button
          @click="activeTab = 'profile'"
          :class="[
            'pb-2 font-semibold transition-colors',
            activeTab === 'profile'
              ? 'border-b-2 border-green-600 text-green-600'
              : 'text-gray-600 hover:text-gray-800'
          ]"
        >
          Mi Perfil
        </button>

        <button
          @click="activeTab = 'reviews'"
          :class="[
            'pb-2 font-semibold transition-colors',
            activeTab === 'reviews'
              ? 'border-b-2 border-green-600 text-green-600'
              : 'text-gray-600 hover:text-gray-800'
          ]"
        >
          Mis Reseñas
        </button>

        <button
          @click="activeTab = 'favorites'"
          :class="[
            'pb-2 font-semibold transition-colors',
            activeTab === 'favorites'
              ? 'border-b-2 border-green-600 text-green-600'
              : 'text-gray-600 hover:text-gray-800'
          ]"
        >
          Mis Favoritos
        </button>
      </div>

      <div class="pt-4">
        <div v-if="activeTab === 'profile'">
          <div class="bg-white shadow-md rounded-xl p-6 flex items-center gap-6">
            <img
              :src="user.picture"
              alt="Foto de usuario"
              class="w-20 h-20 rounded-full object-cover shadow"
            />

            <div class="flex-1">
              <h2 class="text-2xl font-bold">{{ user.name }}</h2>
              <p class="text-gray-600">{{ user.email }}</p>
            </div>

            <GoogleLoginButton 
              :logged-in="loggedIn" 
              :user="user" 
              @login="login"
              @logout="logout"
            />
          </div>
        </div>
        <div v-if="activeTab === 'reviews'">
          <ReviewsList
            :reviews="sortedReviews"
            :meta="reviewsMeta"
            :loading="reviewsLoading"
            @page-change="loadReviews"
            @order-change="changeReviewsOrder"
          />
        </div>

        <div v-if="activeTab === 'favorites'">
          <div v-if="favoritesLoading" class="text-center py-8">
            <p class="text-gray-600">Cargando favoritos...</p>
          </div>
          
          <div v-else-if="sortedFavorites.length === 0" class="text-center py-8">
            <p class="text-gray-600">No tienes sitios favoritos aún.</p>
          </div>
          
          <div v-else>
            <div class="sites-grid">
              <SiteCard 
                v-for="favorite in sortedFavorites" 
                :key="favorite.id" 
                :site="favorite"
              />
            </div>
            
            <!-- Paginación -->
            <div v-if="favoritesMeta.total_pages > 1" class="flex justify-center mt-8">
              <button 
                v-for="page in favoritesMeta.total_pages" 
                :key="page"
                @click="loadFavorites(page)"
                :class="[
                  'px-3 py-1 mx-1 rounded',
                  page === favoritesMeta.current_page 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                ]"
              >
                {{ page }}
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import GoogleLoginButton from '../components/GoogleLoginButton.vue'
import ReviewsList from '../components/UserReviewsList.vue'
import SiteCard from '../components/SiteCard.vue'
import { useAuth } from '../composables/useAuth'
import { useApi } from '../composables/useApi'

const Api = useApi()


const { loggedIn, user, loading, login, logout } = useAuth() 

const API_URL = import.meta.env.VITE_API_URL


const activeTab = ref('profile')
const reviews = ref([])
const reviewsMeta = ref({})
const reviewsLoading = ref(false)
const reviewsOrder = ref('desc')
const favorites = ref([])
const favoritesMeta = ref({})
const favoritesLoading = ref(false)
const favoritesOrder = ref('desc')


const loadReviews = async (page = 1) => {
  if (!loggedIn.value) return;

  reviewsLoading.value = true;

  try {
    const res = await Api.getMyReviews({ page });    
    const data = res.data || {}
    reviews.value = (data.data || []).map(r => ({
      ...r,
      date: r.inserted_at
    }))
    
    const meta = data.meta || {}
    reviewsMeta.value = {
      current_page: meta.page || 1,
      total_pages: Math.ceil((meta.total || 0) / (meta.per_page || 20)),
      total: meta.total || 0
    }
  } catch (error) {
    console.error("Error loading reviews:", error)
  } finally {
    reviewsLoading.value = false
  }
}


const changeReviewsOrder = (order) => {
  reviewsOrder.value = order
}


const loadFavorites = async (page = 1) => {
  if (!loggedIn.value) return;

  favoritesLoading.value = true;

  try {
    const res = await Api.getMyFavorites({ page });


    const data = res.data;

    favorites.value = (data.data || []).map(f => {

      return {
        ...f,
        date: f.inserted_at
      }
    })
    
    const meta = data.meta || {};

    favoritesMeta.value = {
      current_page: meta.page || 1,
      total_pages: Math.ceil((meta.total || 0) / (meta.per_page || 20)),
      total: meta.total || 0
    };
  } catch (error) {
    console.error("Error loading favorites:", error);
  } finally {
    favoritesLoading.value = false;
  }
};

const changeFavoritesOrder = (order) => {
  favoritesOrder.value = order
}


const sortedReviews = computed(() => {
  return [...reviews.value].sort((a, b) => {
    const d1 = new Date(a.date)
    const d2 = new Date(b.date)
    return reviewsOrder.value === 'desc' ? d2 - d1 : d1 - d2
  })
})

const sortedFavorites = computed(() => {
  return [...favorites.value].sort((a, b) => {
    const d1 = new Date(a.date)
    const d2 = new Date(b.date)
    return favoritesOrder.value === 'desc' ? d2 - d1 : d1 - d2
  })
})



watch(loggedIn, async (isLoggedIn) => {
  if (isLoggedIn) {
    // Si el usuario acaba de iniciar sesión, cargamos los datos
    // await Api.getToken();
    await loadReviews()
    await loadFavorites()
  } else {
    // Si el usuario cierra sesión, limpiamos la lista
    reviews.value = []
    favorites.value = []
  }
}, { 
  // 'immediate: true' garantiza que se ejecute al inicio, una vez que useAuth 
  // ha determinado el estado inicial de la sesión.
  immediate: true 
})
</script>

<style scoped>
.sites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .sites-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1rem;
  }
}
</style>