/** @type {import("tailwindcss").Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ["var(--font-serif)", "serif"],
        sans: ["var(--font-sans)", "sans-serif"],
      },
      colors: {
        "background-1": "#f6f5e9",
        "background-2": "#f7f6ef",
        "background-3": "#f8f6f3",
        "background-4": "#faf8fa",
        "green-sidc": "#4c9a89",
      }
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
  ],
}
