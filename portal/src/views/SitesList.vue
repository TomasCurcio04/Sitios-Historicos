<template>
  <div>
    <SearchHero @search="handleHeroSearch" />
    
    <div class="container">
      <h1 class="title">Listado de sitios</h1>

    <div class="main-layout">
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
              <option
                v-for="tag in tags"
                :key="tag.id"
                :value="tag.name"
              >
                {{ tag.name }}
              </option>
            </select>
          </div>

          <!-- Provincias -->
          <div class="filter-group">
            <label class="filter-label">Provincias:</label>
            <select v-model="selectedProvince" class="filter-input">
              <option value="">--Cualquiera--</option>
              <option
                v-for="state in states"
                :key="state.id"
                :value="state.name"
              >
                {{ state.name }}
              </option>
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

          <!-- Radio mapa -->
          <div class="filter-group">
            <label class="filter-label">Radio (Km):</label>
            <input type="number" v-model.number="radius" @input="actualizarRadio" class="filter-input">
          </div>

          <!-- MAPA -->
          <div id="map" style="height: 300px; margin: 1rem 0; border-radius: 8px;"></div>

          <div class="buttons-group">
            <button type="button" @click="buscarSitios(1)" class="btn btn-primary">Buscar</button>
            <button type="button" @click="borrarFiltros" class="btn btn-secondary">Borrar</button>
          </div>

        </div>
      </div>

      <!-- CONTENIDO PRINCIPAL -->
      <div class="content-area">
        <!-- GRID DE TARJETAS -->
        <div class="sites-grid">
          <router-link
            v-for="site in sites"
            :key="site.id"
            :to="`/sites/${site.id}`"
            class="site-card"
          >
            <div class="card-image">
              <img
                v-if="site.cover_image"
                :src="getMinioUrl(site.cover_image)"
                :alt="'Cover de ' + site.name"
                class="cover-image"
              />
              <div v-else class="no-image-placeholder">Sin Portada</div>
            </div>

            <div class="card-content">
              <h2 class="card-title">{{ site.name }}</h2>
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
                  <span class="label">Estado:</span>
                  <span class="value conservation-badge">{{ site.state_of_conservation }}</span>
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <div v-if="hasSearched && sites.length === 0" class="no-results">
      No se encontraron sitios con los filtros seleccionados.
    </div>

    <div v-if="meta.total > 0" class="pagination">
      <button
        class="btn"
        :disabled="meta.page === 1"
        @click="cambiarPagina(meta.page - 1)"
      >
        ◀ Anterior
      </button>

      <span class="page-info">
        Página {{ meta.page }} de {{ meta.pages }}
      </span>

      <button
        class="btn"
        :disabled="meta.page === meta.pages"
        @click="cambiarPagina(meta.page + 1)"
      >
        Siguiente ▶
      </button>
    </div>
    </div>
  </div>
</template>

<script>
import api from '../Services/api.js';
import SearchHero from '../components/SearchHero.vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
L.Popup.prototype.options.zoomAnimation = false;

export default {
  components: {
    SearchHero
  },
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
      minioBucket: "grupo10",

      selectedLat: null,
      selectedLong: null,

      map: null,
      marker: null,
      markersLayer: null,
      circle: null,
      radius: 100
    };
  },

  created() {
    api.getTags().then(res => this.tags = res.data);
    api.getStates().then(res => this.states = res.data);

    const urlParams = new URLSearchParams(window.location.search);
    const pageFromUrl = parseInt(urlParams.get("page")) || 1;

    if (urlParams.get("q")) this.searchNameDesc = urlParams.get("q");
    if (urlParams.get("favorites") === "true") this.favorites = true;

    // Inicializar selects según order_by del query
    const orderParam = urlParams.get("order_by");
    if (orderParam) {
      switch(orderParam) {
        case "most-visited": this.sortBy = "visitas"; this.sortOrder = "asc"; break;
        case "name-asc": this.sortBy = "nombre"; this.sortOrder = "asc"; break;
        case "name-desc": this.sortBy = "nombre"; this.sortOrder = "desc"; break;
        case "rating-1-5": this.sortBy = "rank"; this.sortOrder = "asc"; break;
        case "rating-5-1": this.sortBy = "rank"; this.sortOrder = "desc"; break;
        case "latest": this.sortBy = "fecha"; this.sortOrder = "desc"; break;
        case "oldest": this.sortBy = "fecha"; this.sortOrder = "asc"; break;
        default: break;
      }
    }

    this.buscarSitios(pageFromUrl);
  },

  mounted() {
    this.map = L.map('map').setView([-34.6037, -58.3816], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }).addTo(this.map);

    this.markersLayer = L.layerGroup().addTo(this.map);

    this.map.on('click', (e) => {
      const lat = e.latlng.lat;
      const long = e.latlng.lng;

      this.selectedLat = lat;
      this.selectedLong = long;

      if (this.marker) this.marker.setLatLng([lat, long]);
      else this.marker = L.marker([lat, long]).addTo(this.map);

      if (this.circle) this.circle.setLatLng([lat, long]);
      else this.circle = L.circle([lat, long], {
        radius: this.radius*1000,
        color: 'blue',
        fillColor: 'blue',
        fillOpacity: 0.2
      }).addTo(this.map);
    });
  },

  methods: {
    handleHeroSearch(query) {
      this.searchNameDesc = query;
      this.buscarSitios(1);
    },

    getMinioUrl(imagePath) {
      return `${this.minioBaseUrl}/${this.minioBucket}/${imagePath}`;
    },

    actualizarRadio() {
      if (this.circle) this.circle.setRadius(this.radius*1000);
    },

    actualizarMarcadores() {
      if (!this.map) return;
      this.map.closePopup();
      this.markersLayer.clearLayers();
      this.sites.forEach(site => {
        const lat = Number(site.lat);
        const long = Number(site.long);
        if (!isNaN(lat) && !isNaN(long)) {
          const marker = L.marker([lat, long]).addTo(this.markersLayer);
          marker.bindPopup(`<b>${site.name}</b><br>${site.city}, ${site.province}`);
        }
      });
    },

    buscarSitios(page = 1) {
      this.hasSearched = true;
      const params = { page, per_page: 20 };

      if (this.searchCity) params.city = this.searchCity;
      if (this.selectedProvince) params.province = this.selectedProvince;
      if (this.selectedTags.length) params.tags = this.selectedTags.join(',');
      if (this.favorites) params.favorites = true;
      if (this.searchNameDesc) params.search = this.searchNameDesc;

      if (this.selectedLat && this.selectedLong) {
        params.lat = this.selectedLat;
        params.long = this.selectedLong;
      }
      if (this.radius) params.radius = this.radius;

      // Generar order_by según selects
      const map = {
        nombre: { asc: "name-asc", desc: "name-desc" },
        rank: { asc: "rating-1-5", desc: "rating-5-1" },
        fecha: { asc: "oldest", desc: "latest" },
        visitas: { asc: "most-visited", desc: "most-visited" }
      };
      params.order_by = map[this.sortBy][this.sortOrder];

      this.$router.push({ query: params });
      console.log("Parámetros de búsqueda:", params);

      api.getSites(params)
        .then(res => {
          this.sites = res.data.data;
          this.meta = res.data.meta;
          this.actualizarMarcadores();

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
