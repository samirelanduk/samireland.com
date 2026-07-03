module.exports = {
  extends: "next/core-web-vitals",
  rules: {
    "@next/next/no-img-element": "off",
  },
  parserOptions: {
    babelOptions: {
      presets: [require.resolve("next/babel")],
    },
  },
};
