const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
  // lintOnSave: false,
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.csv$/,
          use: [
            {
              loader: "csv-loader",
              options: {
                dynamicTyping: true,
                header: true,
                skipEmptyLines: true,
              },
            },
          ],
        },
      ],
    },
  },
});
