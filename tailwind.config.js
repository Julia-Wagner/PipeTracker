/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,py}"],
  theme: {
    extend: {
      colors: {
        lightblue: "#00B2CA",
        darkblue: "#274060",
        customwhite: "#F9F9F9",
        customblack: "#041020",
        danger: "#bb1515",
        success: "#1da31d",
        warning: "#cfbb1f",
      },
    },
  },
  plugins: [],
}

