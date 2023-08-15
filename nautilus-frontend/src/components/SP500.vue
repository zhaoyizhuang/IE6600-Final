<template>
  <div class="stock-chart">
    <button class="show-button" @click="showPerformance = !showPerformance">
      {{
        showPerformance
          ? "Show S&P500 Sector"
          : "Show S&P500 Sector Performance"
      }}
    </button>
    <ECharts v-if="!showPerformance" class="chart" :option="pie" />
    <div v-else>
      <button class="show-button" @click="showOneYear = !showOneYear">
        {{ showOneYear ? "Show 5Y Performance" : "Show 1Y Performance" }}
      </button>
      <ECharts v-if="showOneYear" class="chart" :option="bar" />
      <ECharts v-else class="chart" :option="bar5" />
    </div>
  </div>
</template>

<script>
import ECharts from "vue-echarts";
import { use } from "echarts/core";
import { PieChart } from "echarts/charts";
import performance from "../assets/SP500_Perf.csv";

use([PieChart]);

export default {
  name: "SP500Chart",
  components: {
    ECharts,
  },
  data() {
    return {
      showPerformance: false,
      showOneYear: true,
      performance: performance,
      pie: {
        title: {
          text: "S&P 500 Sectors",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        plotarea: {
          left: 0,
          "adjust-layout": true,
        },
        legend: {
          orient: "horizontal",
          bottom: 0,
          "adjust-layout": true,
        },
        series: [
          {
            name: "S&P 500 Sector",
            type: "pie",
            radius: "50%",
            data: [
              { value: 28.1, name: "Information Technology" },
              { value: 13.1, name: "Health Care" },
              { value: 12.6, name: "Financials" },
              { value: 10.6, name: "Consumer Discretionary" },
              { value: 8.7, name: "Communication Services" },
              { value: 8.5, name: "Industrials" },
              { value: 6.6, name: "Consumer Staples" },
              { value: 4.3, name: "Energy" },
              { value: 2.6, name: "Utilities" },
              { value: 2.5, name: "Materials" },
              { value: 2.5, name: "Real Estate" },
            ],
            tooltip: {
              trigger: "item",
              formatter: "{a} <br/>{b} : {c}%",
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      },
      bar: {
        title: {
          text: "S&P 500 Sectors 1Y Performance",
          left: "center",
        },
        xAxis: {
          type: "category",
          axisLabel: {
            show: true,
            interval: 0,
            rotate: 45,
          },
          data: [
            "Information Technology",
            "Health Care",
            "Financials",
            "Consumer Discretionary",
            "Communication Services",
            "Industrials",
            "Consumer Staples",
            "Energy",
            "Utilities",
            "Materials",
            "Real Estate",
          ],
        },
        yAxis: {
          type: "value",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
          formatter: "{b} : {c}%",
        },
        series: [
          {
            data: [
              13.85, 1.82, -1.93, 0.4, 11.63, 9.14, -0.32, 14.53, -16.46, 2.28,
              -18.16,
            ],
            type: "bar",
            areaStyle: {},
          },
        ],
        visualMap: {
          left: "right",
          min: 0,
          max: 1,
          inRange: {
            color: ["red", "green"],
          },
          calculable: true,
        },
        grid: {
          containLabel: true,
        },
      },
      bar5: {
        title: {
          text: "S&P 500 Sectors 5Y Performance",
          left: "center",
        },
        xAxis: {
          type: "category",
          axisLabel: {
            show: true,
            interval: 0,
            rotate: 45,
          },
          data: [
            "Information Technology",
            "Health Care",
            "Financials",
            "Consumer Discretionary",
            "Communication Services",
            "Industrials",
            "Consumer Staples",
            "Energy",
            "Utilities",
            "Materials",
            "Real Estate",
          ],
        },
        yAxis: {
          type: "value",
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow",
          },
          formatter: "{b} : {c}%",
        },
        series: [
          {
            data: [
              134.45, 52.87, 26.07, 50.62, 49.55, 46.65, 43.05, 25.05, 20.88,
              43.23, 14.87,
            ],
            type: "bar",
            areaStyle: {},
          },
        ],
        visualMap: {
          left: "right",
          min: 0,
          max: 1,
          inRange: {
            color: ["red", "green"],
          },
          calculable: true,
        },
        grid: {
          containLabel: true,
        },
      },
    };
  },
};
</script>

<style scoped>
.chart {
  height: 450px;
  width: 800px;
}
.stock-chart {
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
  flex-direction: column;
}

.show-button {
  background-color: antiquewhite;
  height: 24px;
  margin-top: 8px;
}

.show-button:hover {
  cursor: pointer;
}
</style>
