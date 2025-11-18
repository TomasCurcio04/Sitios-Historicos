<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SiteCard from '../components/SiteCard.vue'
import { fetchSites } from '../api.js' // asegúrate de usar la nueva api.js

export default {
  name: 'ListPage',
  components: { SiteCard },

  setup() {
    const route = useRoute()
    const router = useRouter()

    const search = ref(route.query.q || '')
    const order = ref(route.query.order || '')

    const sites = ref([])
    const loading = ref(false)

    const page = ref(Number(route.query.page) || 1)
    const pageSize = 9
    const totalPages = ref(1)

    async function fetchData() {
      loading.value = true

      router.replace({
        query: {
          q: search.value || undefined,
          order: order.value || undefined,
          page: page.value !== 1 ? page.value : undefined,
        },
      })

      try {
        const result = await fetchSites({
          q: search.value,
          order: order.value,
          page: page.value,
          limit: pageSize,
        })

        if (result.success) {
          sites.value = result.data.items || []
          totalPages.value = Math.ceil((result.data.total || 0) / pageSize)
        } else {
          console.error('Error fetchSites:', result.error)
          sites.value = []
          totalPages.value = 1
        }
      } catch (e) {
        console.error('Error cargando listado:', e)
        sites.value = []
        totalPages.value = 1
      }

      loading.value = false
    }

    function nextPage() {
      if (page.value < totalPages.value) {
        page.value++
        fetchData()
      }
    }

    function prevPage() {
      if (page.value > 1) {
        page.value--
        fetchData()
      }
    }

    onMounted(fetchData)
    watch(() => route.query, fetchData)

    return {
      sites,
      search,
      order,
      loading,
      page,
      totalPages,
      nextPage,
      prevPage,
      fetchData,
    }
  },
}
</script>
