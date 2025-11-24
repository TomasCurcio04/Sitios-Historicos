<template>
  <div id="app-layout">
    
    <header class="w-full bg-white shadow-md p-4 sticky top-0 z-10">
      <div class="flex justify-between items-center max-w-7xl mx-auto">
        
        <router-link to="/" class="btn btn-primary">
          Inicio
        </router-link>

        <div class="flex items-center space-x-4">
          
          <template v-if="loading">
            <span class="text-gray-500 text-sm">Cargando...</span>
          </template>
          
          <template v-else>
            <ProfileDropdown
              v-if="loggedIn"
              :user="user"
              @logout="logout"  
            />

            <GoogleLoginButton 
              v-else
              :logged-in="loggedIn" 
              :user="user" 
              @login="login" 
              @logout="logout" 
            />
          </template>

        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto p-4">
      <RouterView /> 
    </main>

  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuth } from '@/composables/useAuth' 
import GoogleLoginButton from '@/components/GoogleLoginButton.vue' 
import ProfileDropdown from '@/components/ProfileDropDown.vue' 
import { onMounted } from 'vue'

const auth = useAuth()

const { loggedIn, user, loading, login, logout, checkSession } = auth

onMounted(() => {
  checkSession()
})
</script>

<style>
/* Aquí puedes importar tus estilos globales si es necesario */
/* @import '@/assets/main.css'; */ 
</style>