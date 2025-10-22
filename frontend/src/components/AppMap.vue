<template>
    <div id="map-container">
      <div v-show="workspaceAreaPolygon" id="map" />
      <div v-show="!workspaceAreaPolygon">
        <div v-if="loadingBbox.active" class="alert alert-info" role="alert">
          <app-spinner size="sm" />
          Rendering map...
        </div>
        <div v-else class="alert alert-info" role="error">
          No workspace area available to render map.
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
  import { ref, reactive, watch, onMounted } from 'vue';
  import { workspacesClient } from '@/services/index';
  import { LoadingContext } from '@/services/loading';
  import * as L from 'leaflet';
  
  const props = defineProps({
    mapMarkers: {
      type: Array,
      default: () => []
    },
    workspace: {
      type: Object,
      default: null
    }
  });
  
  const loadingBbox = reactive(new LoadingContext());
  const map = ref(null);
  const workspaceAreaPolygon = ref(null);
  
  onMounted(() => {
    watch(
      () => props.workspace,
      (val) => {
        if (val) {
          updateMapPreview(val);
        } else {
          map.value = null;
        }
      },
      { immediate: true }
    );
  });
  
  function initMap() {
    map.value = L.map('map');
  
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map.value);

    props.mapMarkers.forEach((marker) => {
      L.marker([marker.latitude, marker.longitude])
        .addTo(map.value)
        .bindPopup(marker.popup || '');
    });
  }
  
  async function updateMapPreview(workspace) {
    if (workspaceAreaPolygon.value) {
      workspaceAreaPolygon.value.remove();
      workspaceAreaPolygon.value = null
    }
  
    if (!props.workspace.id) {
      return;
    }
  
    await setCurrentWorkspacePolygon(workspace);
  
    if (!workspaceAreaPolygon.value) {
      return;
    }
  
    if (!map.value) {
      initMap();
    }
  
    const bounds = workspaceAreaPolygon.value.getBounds();
  
    workspaceAreaPolygon.value.addTo(map.value);
    map.value.fitBounds(bounds);
  }
  
  async function setCurrentWorkspacePolygon(workspace) {
    const metadataArea = workspace.tdeiMetadata?.metadata?.dataset_detail?.dataset_area;
  
    if (metadataArea) {
      const polygon = L.geoJSON(metadataArea);
  
      if (polygon.getBounds().isValid()) {
        workspaceAreaPolygon.value = polygon;
        return;
      }
    }
  
    await loadingBbox.cancelable(workspacesClient, async (client) => {
      const bbox = await client.getWorkspaceBbox(workspace.id);
  
      if (bbox) {
        workspaceAreaPolygon.value = L.rectangle([
          [bbox.min_lat, bbox.min_lon],
          [bbox.max_lat, bbox.max_lon]
        ])
      }
    });
  }
  </script>