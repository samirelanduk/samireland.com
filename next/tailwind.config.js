/** @type {import("tailwindcss").Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            "code::before": {
              content: '""'
            },
            "code::after": {
              content: '""'
            },
            "code": {
              "font-weight": "inherit",
              "color": "inherit",
            },
          }
        }
      },
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
        "green-sidc-faint": "#a5c8be"
      },
      height: {
        "54": "13.5rem",
      },
      maxWidth: {
        "8xl": "88rem",
        "9xl": "96rem",
        "10xl": "104rem",
      },
      screens: {
        "xs": "400px",
        "3xl": "1720px",
      },
      fontSize: {
        "2xs": ".625rem",
      },
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
  ],
}
