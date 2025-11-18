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

const loggedIn = ref(false)
const user = ref(null)

onMounted(async () => {
  const res = await fetch('http://localhost:5000/google/status', {
    credentials: 'include'
  })
  const data = await res.json()

  loggedIn.value = data.logged_in
  user.value = data.user || null
})

const loginWithGoogle = () => {
  window.location.href = 'http://localhost:5000/google/login'
}

const logout = () => {
  const current = window.location.href;
  window.location.href = `http://localhost:5000/google/logout?next=${encodeURIComponent(current)}`;
};

</script>

<style scoped>
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
