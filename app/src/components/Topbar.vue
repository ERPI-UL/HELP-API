<template>
  <div
    class="sticky top-0 w-screen flex justify-between bg-white p-4 z-30 shadow-lg"
  >
    <div>
      <slot name="left"></slot>
    </div>
    <div>
      <slot></slot>
    </div>
    <div>
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "Topbar",
  props: {
    left: String,
  },
};
</script>

<style>
</style>