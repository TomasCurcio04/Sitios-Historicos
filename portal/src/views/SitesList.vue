<template>
  <div class="container">
    <h1 class="title">Listado de sitios</h1>

    <!-- FILTROS -->
    <div class="filters-wrapper">
      <button class="filters-toggle" @click="filtersOpen = !filtersOpen">
        <span>{{ filtersOpen ? '✕' : '' }} Filtros</span>
      </button>

      <div class="filters-section" :class="{ active: filtersOpen }">
        <!-- Búsqueda por nombre o descripción -->
        <div class="filter-group">
          <label class="filter-label">Búsqueda por nombre o descripción:</label>
          <input type="text" v-model="searchNameDesc" class="filter-input">
        </div>

        <!-- Tags -->
        <div class="filter-group">
          <label class="filter-label">Tags:</label>
          <select multiple v-model="selectedTags" class="filter-input">
            <option v-for="tag in tags" :key="tag.id" :value="tag.name">{{ tag.name }}</option>
          </select>
        </div>

        <!-- Provincias -->
        <div class="filter-group">
          <label class="filter-label">Provincias:</label>
          <select v-model="selectedProvince" class="filter-input">
            <option value="">--Cualquiera--</option>
            <option v-for="state in states" :key="state.id" :value="state.name">{{ state.name }}</option>
          </select>
        </div>

        <!-- Favoritos -->
        <div class="filter-group">
          <label class="filter-label checkbox-label">
            <input type="checkbox" v-model="favorites" class="checkbox-input"> Favoritos
          </label>
        </div>

        <!-- Ciudad -->
        <div class="filter-group">
          <label class="filter-label">Búsqueda por ciudad:</label>
          <input type="text" v-model="searchCity" class="filter-input">
        </div>

        <!-- Orden -->
        <div class="filter-group">
          <label class="filter-label">Ordenar por:</label>
          <select v-model="sortBy" class="filter-input">
            <option value="fecha">Fecha de registro</option>
            <option value="nombre">Nombre</option>
            <option value="rank">Mejor rankeados</option>
            <option value="visitas">Más visitados</option>
          </select>

          <select v-model="sortOrder" class="filter-input">
            <option value="asc">Ascendente</option>
            <option value="desc">Descendente</option>
          </select>
        </div>

        <div class="buttons-group">
          <button type="button" @click="buscarSitios(1)" class="btn btn-primary">Buscar</button>
          <button type="button" @click="borrarFiltros" class="btn btn-secondary">Borrar</button>
        </div>
      </div>
    </div>

    <!-- GRID DE TARJETAS -->
    <div class="sites-grid">
      <div v-for="site in sites" :key="site.id" class="site-card">
        <img v-if="site.cover_image" :src="getMinioUrl(site.cover_image)" :alt="'Cover de ' + site.name" class="cover-image" />
        <span v-else style="font-size: 0.8rem; color: #888;">Sin imagen</span>

        <div class="card-header">
          <h2 class="card-title">{{ site.name }}</h2>
        </div>
        <div class="card-body">
          <div class="card-info">
            <span class="label">Ciudad:</span>
            <span class="value">{{ site.city }}</span>
          </div>
          <div class="card-info">
            <span class="label">Provincia:</span>
            <span class="value">{{ site.province }}</span>
          </div>
          <div class="card-info">
            <span class="label">Estado de conservación:</span>
            <span class="value conservation-badge">{{ site.state_of_conservation }}</span>
          </div>
          <div>
            <span class="label">Tags:</span>
            <span class="value">{{ site.tags.join(', ') }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="hasSearched && sites.length === 0" class="no-results">
      No se encontraron sitios con los filtros seleccionados.
    </div>

    <div v-if="meta.total > 0" class="pagination">
      <button class="btn" :disabled="meta.page === 1" @click="cambiarPagina(meta.page - 1)">◀ Anterior</button>
      <span class="page-info">Página {{ meta.page }} de {{ meta.pages }}</span>
      <button class="btn" :disabled="meta.page === meta.pages" @click="cambiarPagina(meta.page + 1)">Siguiente ▶</button>
    </div>
  </div>
</template>

<script>
import api from '../Services/api.js';

export default {
  data() {
    return {
      sites: [],
      meta: { page: 1, per_page: 20, total: 0, pages: 1 },
      searchNameDesc: '',
      tags: [],
      states: [],
      selectedTags: [],
      selectedProvince: '',
      searchCity: '',
      favorites: false,
      hasSearched: false,
      filtersOpen: false,
      sortBy: 'fecha',
      sortOrder: 'desc',
      minioBaseUrl: "http://minio.proyecto2025.linti.unlp.edu.ar",
      minioBucket: "grupo10"
    };
  },

  created() {
    api.getTags().then(res => this.tags = res.data);
    api.getStates().then(res => this.states = res.data);

    const urlParams = new URLSearchParams(window.location.search);
    const pageFromUrl = parseInt(urlParams.get("page")) || 1;

    // Asignar filtros desde query params
    if (urlParams.get("q")) this.searchNameDesc = urlParams.get("q");
    if (urlParams.get("favorites") === "true") this.favorites = true;
    if (urlParams.get("order_by")) this.order_by = urlParams.get("order_by");

    this.buscarSitios(pageFromUrl);
  },

  methods: {
    getMinioUrl(imagePath) {
      return `${this.minioBaseUrl}/${this.minioBucket}/${imagePath}`;
    },

    buscarSitios(page = 1) {
      this.hasSearched = true;

      const params = { page, per_page: 20 };

      if (this.searchCity) params.city = this.searchCity;
      if (this.selectedProvince) params.province = this.selectedProvince;
      if (this.selectedTags.length) params.tags = this.selectedTags.join(',');
      if (this.favorites) params.favorites = true;
      if (this.searchNameDesc) params.search = this.searchNameDesc;

      // Usar directamente order_by de query params o de sortBy/sortOrder
      if (this.$route.query.order_by) {
        params.order_by = this.$route.query.order_by;
      } else {
        // Map opcional si se usa el select manual
        const map = {
          nombre: { asc: "name-asc", desc: "name-desc" },
          rank: { asc: "rating-1-5", desc: "rating-5-1" },
          fecha: { asc: "oldest", desc: "latest" },
          visitas: { asc: "most-visited", desc: "most-visited" }
        };
        params.order_by = map[this.sortBy]?.[this.sortOrder] || null;
      }

      this.$router.push({ query: params });

      api.getSites(params)
        .then(res => {
          this.sites = res.data.data;
          this.meta = res.data.meta;
          const total = Number(this.meta.total || 0);
          const perPage = Number(this.meta.per_page || 20);
          this.meta.pages = Math.max(1, Math.ceil(total / perPage));
          if (this.meta.page > this.meta.pages) this.meta.page = this.meta.pages;
        })
        .catch(err => console.error("Error buscando sitios:", err));
    },

    cambiarPagina(nuevaPagina) {
      this.buscarSitios(nuevaPagina);
      const url = new URL(window.location.href);
      url.searchParams.set("page", nuevaPagina);
      window.history.replaceState({}, '', url);
    },

    borrarFiltros() {
      this.searchNameDesc = '';
      this.selectedTags = [];
      this.selectedProvince = '';
      this.searchCity = '';
      this.favorites = false;
      this.sortBy = 'fecha';
      this.sortOrder = 'desc';
      this.$router.push({ query: {} });
      this.buscarSitios(1);
    }
  }
};
</script>
