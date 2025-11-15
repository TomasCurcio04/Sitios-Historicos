<!-- src/components/GoogleLoginButton.vue -->
<template>
  <button @click="loginWithGoogle">
    Registrarse / Iniciar sesión con Google
  </button>
</template>

<script setup>
const loginWithGoogle = () => {
  window.location.href = 'http://localhost:5000/google/login'
}
</script>

<style scoped>
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
