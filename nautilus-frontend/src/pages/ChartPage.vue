<template>
  <div>
    <SearchPanel />
    <StockChartVue />
  </div>
</template>

<script>
import SearchPanel from "@/components/SearchPanel.vue";
import StockChartVue from "../components/StockChart.vue";
import { ref, provide } from "vue";

export default {
  name: "ChartPage",
  components: {
    SearchPanel,
    StockChartVue,
  },
  setup() {
    const stockData = ref([]);
    provide("stockDataKey", stockData);

    const comparisonData = ref([]);
    provide("comparisonDataKey", comparisonData);
  },
};
</script>

<style scoped></style>
