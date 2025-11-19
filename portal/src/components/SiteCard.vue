<template>
  <div class="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden">
    <img
      :src="site.image || 'https://via.placeholder.com/300x200'"
      class="h-32 w-full object-cover"
    />

    <div class="p-3">
      <h3 class="font-semibold text-gray-800 truncate">{{ site.name }}</h3>

      <p class="text-sm text-gray-500 mt-1">⭐ {{ site.rating || 'Sin puntuación' }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SiteCard',
  props: {
    site: { type: Object, required: true },
  },
}
</script>
