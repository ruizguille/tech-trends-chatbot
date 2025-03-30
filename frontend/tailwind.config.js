/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        urbanist: ['Urbanist', 'sans-serif'],
        opensans: ['Open Sans', 'sans-serif'],
      },
      colors: {
        'primary-blue': 'rgb(146, 179, 202)',
        'primary-orange': 'rgb(255, 149, 0)',
        'main-text': '#1A1A1A',
        'error-red': 'rgb(208, 69, 82)',
      },
      animation: {
        chat: 'pulse 0.4s cubic-bezier(0.4, 0, 0.6, 1)',
      },
    },
  },
  plugins: [],
}