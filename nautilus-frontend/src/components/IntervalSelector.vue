<template>
  <button class="selector" @click="$emit('clicked', interval)">
    <span :class="selected ? 'selected' : 'text'">
      {{ interval }}
    </span>
  </button>
</template>

<script>
export default {
  name: "IntervalSelector",
  props: {
    interval: {
      type: String,
      required: true,
    },
    selected: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.selector {
  background-color: white;
  border: white;
}
.text {
  color: black;
}
.text:hover {
  color: rgb(0, 183, 255);
  cursor: pointer;
}
.selected {
  font-weight: 900;
  color: rgb(0, 183, 255);
}
</style>
