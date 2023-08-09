<template>
  <div class="panel">
    <div class="search-panel">
      <div class="search-bar">
        <SearchBar
          ref="search"
          :interval="intervals[selectedIdx]"
          :retrieveFunction="getStock"
          :showErrorMsg="emptyData"
          @retrieved="retrieved"
        />
      </div>
    </div>
    <div class="tool-bar">
      <button class="tools comparison-tool" @click="showComparisonModal = true">
        Comparison
      </button>
      <div class="tools" v-for="(interval, idx) in intervals" :key="interval">
        <IntervalSelector
          :interval="interval"
          :selected="selectedIdx === idx"
          @clicked="clicked(idx)"
        />
      </div>
    </div>
    <ComparisonModal :show="showComparisonModal" @close="closeModal">
      <template v-slot:body>
        <SearchBar
          placeholder="Add a comparison stock"
          searchButtonText="Add"
          :interval="intervals[selectedIdx]"
          :retrieveFunction="getCloseDataStock"
          :showErrorMsg="badComparisonData"
          :errorMsg="comparisonErrorMsg"
          @retrieved="added"
        />
      </template>
    </ComparisonModal>
  </div>
</template>

<script>
import stockService from "../services/stockService";
import IntervalSelector from "./IntervalSelector.vue";
import ComparisonModal from "./ComparisonModal.vue";
import SearchBar from "./SearchBar.vue";
import { inject } from "vue";

export default {
  name: "SearchPanel",
  components: {
    IntervalSelector,
    ComparisonModal,
    SearchBar,
  },
  setup() {
    const stockData = inject("stockDataKey");
    const comparisonData = inject("comparisonDataKey");
    return {
      stockData,
      comparisonData,
    };
  },
  data() {
    return {
      emptyData: false,
      badComparisonData: false,
      comparisonErrorMsg: "",
      getStock: stockService.getStock,
      getCloseDataStock: stockService.getCloseDataStock,
      selectedIdx: 4,
      intervals: ["5D", "60D", "YTD", "1Y", "2Y"],
      showComparisonModal: false,
    };
  },
  watch: {
    selectedIdx() {
      if (this.comparisonData.name) {
        this.getCloseDataStock(
          this.comparisonData.ticker,
          this.intervals[this.selectedIdx]
        ).then((data) => {
          this.added(data);
        });
      }
    },
  },
  methods: {
    retrieved(data) {
      if (data.data?.length === 0) {
        this.emptyData = true;
      } else {
        this.emptyData = false;
        this.stockData = data;
        if (data.name === this.comparisonData.name) {
          this.comparisonData = [];
        }
      }
    },
    added(data) {
      if (data.data?.length === 0) {
        this.badComparisonData = true;
        this.comparisonErrorMsg = "No data found";
      } else {
        if (data.name === this.stockData.name) {
          this.badComparisonData = true;
          this.comparisonErrorMsg = "Duplicate Stock";
        } else {
          this.badComparisonData = false;
          this.comparisonData = data;
          this.closeModal();
        }
      }
    },
    clicked(idx) {
      this.selectedIdx = idx;
    },
    closeModal() {
      this.showComparisonModal = false;
      this.badComparisonData = false;
    },
  },
  mounted() {
    this.getStock("S&P 500", "2Y").then((data) => {
      this.stockData = data;
    });
    this.$refs.search.currentValue = "S&P 500";
  },
};
</script>

<style scoped>
.search-panel {
  margin: auto;
  width: 80%;
  padding: 15px;
}
.search-msg {
  padding-top: 3px;
  padding-left: 30%;
  padding-bottom: 5px;
  color: rgb(247, 96, 96);
}
.text-area {
  margin-left: 7%;
  width: 50%;
  height: 20px;
  font-family: "Times New Roman", Times, serif;
  font-size: 16px;
  background-color: rgba(255, 255, 255, 0.719);
}
.search-btn {
  background-color: rgb(0, 183, 255);
  border: rgb(0, 183, 255);
  color: white;
  display: inline-block;
  vertical-align: top;
  height: 26px;
  border-radius: 5%;
}
.search-btn:disabled {
  background-color: rgb(185, 221, 236);
}
.search-btn:hover {
  cursor: pointer;
}
.search-bar {
  padding-left: 25%;
}

.tools {
  display: inline-block;
  position: relative;
  left: 37%;
  margin: 5px;
}

.comparison-input {
  width: 100%;
  height: 20px;
  outline: 0;
  border-width: 0 0 2px;
  border-color: rgb(185, 221, 236);
}
.comparison-input:focus {
  border-color: rgb(0, 183, 255);
}

.comparison-btn {
  float: right;
}

.comparison-tool {
  border-width: 0;
  background-color: white;
}
.comparison-tool:hover {
  color: rgb(0, 183, 255);
  cursor: pointer;
}
</style>
