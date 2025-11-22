<template>
  <section class="bg-linear-to-br from-blue-600 to-blue-800 py-16 px-4 text-center text-white">
    <h1 class="text-3xl md:text-4xl font-bold mb-4">Descubrí los Sitios Históricos</h1>
    <p class="text-white/80 mb-8">Buscá, explorá y conocé los lugares más importantes.</p>

    <div class="max-w-md mx-auto flex">
      <input
        v-model="search"
        @keyup.enter="emitSearch"
        type="text"
        placeholder="Buscar un sitio..."
        class="flex-1 px-4 py-3 rounded-l-full text-black focus:outline-none"
      />

      <button
        @click="emitSearch"
        class="bg-blue-900 px-6 py-3 rounded-r-full hover:bg-blue-950 transition"
      >
        🔍
      </button>
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'SearchHero',
  setup(_, { emit }) {
    const search = ref('')
    const emitSearch = () => emit('search', search.value)
    return { search, emitSearch }
  },
}
</script>
