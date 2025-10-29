<template>
  <i v-if="tooltip" :class="classes" data-bs-toggle="tooltip" :title="tooltip" />
  <i v-else :class="classes" />
</template>

<script setup lang="ts">
  import { computed } from 'vue';

  const props = defineProps({
    variant: {
      type: String,
      required: true
    },
    size: {
      type: [Number, String],
      default: 18
    },
    noMargin: {
      type: Boolean,
      default: false
    },
    tooltip: {
      type: String,
      default: ''
    }
  })

  const classes = computed(() => ([
    'material-icons',
    `md-${props.size}`,
    `md-${props.variant}`,
    props.noMargin ? undefined : 'me-2'
  ]))
</script>

<style>
  .material-icons {
    vertical-align: middle;
    margin-top: -3px;
  }
  .badge .material-icons {
    font-size: 1em;
    vertical-align: bottom;
    margin-top: 0;

    &.me-2 {
      margin-right: 0.25rem !important;
    }
  }
</style>
