<template>
  <section class="my-8 px-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold">{{ title }}</h2>

      <router-link
        class="text-sm text-blue-600 hover:underline"
        :to="{ name: 'sites-list', query: queryParams }"
      >
        Ver todos >
      </router-link>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-gray-500">Cargando...</div>

    <!-- No content -->
    <div
      v-else-if="items.length === 0"
      class="bg-gray-200 text-gray-700 px-4 py-2 rounded-full text-center text-sm"
    >
      No hay contenido
    </div>

    <!-- Grid -->
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <SiteCard v-for="site in items" :key="site.id" :site="site" />
    </div>
  </section>
</template>

<script>
import { ref, onMounted } from 'vue'
import SiteCard from './SiteCard.vue'

export default {
  name: 'SectionCarousel',
  components: { SiteCard },

  props: {
    title: String,
    fetchFn: Function,
    queryParams: Object,
  },

  setup(props) {
    const items = ref([])
    const loading = ref(true)

    onMounted(async () => {
      try {
        items.value = await props.fetchFn(props.queryParams)
      } catch (err) {
        console.error('Error loading section:', err)
      } finally {
        loading.value = false
      }
    })

    return { items, loading }
  },
}
</script>
