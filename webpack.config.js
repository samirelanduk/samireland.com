const path = require("path");

module.exports = {
    entry: "./core/static/js/main.js",
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "core/static/js/")
    },
    mode: "development"
}