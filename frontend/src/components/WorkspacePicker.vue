<template>
    <select
      v-model="model"
      class="workspace-picker form-select"
      aria-label="Workspace Selection"
      @change="filterChangeEvent"
    >
      <option v-if="workspaces.length === 0" disabled value="">No Workspaces exist in this Project Group</option>
      <option v-for="ws in workspaces" :key="ws.id" :value="ws.id" >
        {{ ws.title }}
      </option>
    </select>
</template>

<script setup lang="ts">
  import { defineEmits, ref, toRefs, watch } from 'vue';
  import { workspacesClient } from '@/services/index';
  
  const model = defineModel({ required: true });
  const props = defineProps({
    projectGroupId: {
        type: String,
        required: true
    }
  });

  const { projectGroupId } = toRefs(props);
  const workspaces = ref([]);
 
  watch(projectGroupId, (val) => refreshWorkspaces(val));

  async function refreshWorkspaces(projectGroupId: string) {
    const myWorkspaces = (await workspacesClient.getMyWorkspaces());
    workspaces.value = myWorkspaces.filter(item => item.tdeiProjectGroupId === projectGroupId).sort((a, b) => a.title.localeCompare(b.title));
    if (workspaces.value.length === 0) {
        model.value = null;
    }
  }

  const emit = defineEmits(['filter-change-event']);

  const filterChangeEvent = () => {
    emit('filter-change-event');
  };
</script>
  