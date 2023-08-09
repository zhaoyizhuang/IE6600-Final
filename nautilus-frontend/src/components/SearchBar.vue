<template>
  <div>
    <input
      class="search-input"
      v-model.trim="searchValue"
      :placeholder="placeholder"
      @keypress.enter="search"
    />
    <button
      class="search-btn"
      @click="retrieveStockData"
      :disabled="searchValue == ''"
    >
      {{ searchButtonText }}
    </button>
    <div v-if="showErrorMsg" class="search-msg">
      {{ errorMsg }}
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  props: {
    placeholder: {
      default: "Search for ticker symbols or companies",
      type: String,
    },
    searchButtonText: {
      default: "Search",
      type: String,
    },
    retrieveFunction: {
      default() {
        return "Default";
      },
      type: Function,
    },
    interval: {
      requried: true,
      type: String,
    },
    showErrorMsg: {
      default: false,
      type: Boolean,
    },
    errorMsg: {
      default: "No data found",
      type: String,
    },
  },
  data() {
    return {
      searchValue: "",
      currentValue: "",
    };
  },
  watch: {
    interval() {
      if (!this.searchValue && this.currentValue) {
        this.retrieveStockData();
      }
    },
  },
  methods: {
    search() {
      if (this.searchValue !== "") {
        this.retrieveStockData();
      }
    },
    retrieveStockData() {
      const id = this.searchValue ? this.searchValue : this.currentValue;
      this.retrieveFunction(id, this.interval).then((data) => {
        if (data.data?.length) {
          this.currentValue = id;
        }
        this.searchValue = "";
        this.$emit("retrieved", data);
      });
    },
  },
};
</script>

<style scoped>
.search-input {
  /* margin-left: 10%; */
  width: 70%;
  height: 30px;
  outline: 0;
  border-width: 0 0 2px;
  border-color: rgb(185, 221, 236);
  font-family: "Times New Roman", Times, serif;
  font-size: 16px;
}
.search-input:focus {
  border-color: rgb(0, 183, 255);
}

.search-btn {
  display: inline-block;
}
.search-btn {
  background-color: rgb(0, 183, 255);
  border: rgb(0, 183, 255);
  color: white;
  display: inline-block;
  vertical-align: top;
  height: 28px;
  border-radius: 10%;
  margin-top: 5px;
  margin-left: 3px;
}
.search-btn:disabled {
  background-color: rgb(185, 221, 236);
}
.search-btn:hover {
  cursor: pointer;
}

.search-msg {
  padding-top: 3px;
  padding-left: 30%;
  padding-bottom: 5px;
  color: rgb(247, 96, 96);
}
</style>
