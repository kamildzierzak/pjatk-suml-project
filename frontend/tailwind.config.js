/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  safelist: [
    {
      pattern: /grid-cols-.+/,
      variants: ["xl"],
    },
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};