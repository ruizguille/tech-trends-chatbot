/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    fontFamily: {
      'sans': ['Open Sans, sans-serif'],
    },
    extend: {
      colors: {
        'primary-blue': 'rgb(178, 217, 231)',
        'primary-orange': 'rgb(243, 195, 177)',
        'main-text': 'rgb(107, 107, 107)',
        'light-gray': 'rgb(244, 244, 244)',
      },
    },
  },
  plugins: [],
};
