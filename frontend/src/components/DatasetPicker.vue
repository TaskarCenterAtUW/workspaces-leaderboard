<template>
    <select
      v-model="model"
      class="dataset-picker form-select"
      aria-label="Dataset Selection"
    >
      <option v-if="datasets.length === 0" disabled value="">No Workspaces exist in this Project Group</option>
      <option v-for="ds in datasets" :key="ds.id" :value="ds.id" >
        {{ ds.name }} (version {{ ds.version }})
      </option>
    </select>
</template>

<script setup lang="ts">
  import { ref, toRefs, watch } from 'vue';
  import { tdeiClient } from '@/services/index'
  
  const model = defineModel({ required: true });
  const props = defineProps({
    projectGroupId: {
        type: String,
        required: true
    }
  });

  const { projectGroupId } = toRefs(props);
  const datasets = ref([]);
 
  watch(projectGroupId, (val) => refreshDatasets(val));

  async function refreshDatasets(projectGroupId: string) {
    datasets.value = (await tdeiClient.getDatasetsByProjectGroup(projectGroupId))
        .sort((a, b) => a.name.localeCompare(b.name));

    if (datasets.value.length === 0) {
        model.value = null;
    }
  }
</script>
  