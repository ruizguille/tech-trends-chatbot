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
      'sans': ['Open Sans', 'sans-serif'],
      'urbanist': ['Urbanist', 'sans-serif'],
    },
    extend: {
      colors: {
        'primary-blue': 'rgb(146, 179, 202)',
        'primary-orange': 'rgb(243, 195, 177)',
        'main-text': 'rgb(0, 43, 49)',
        'error-red': 'rgb(208, 69, 82)',
      },
      animation: {
        'spinner': 'spinner 1.5s linear infinite',
        'spinner-delayed': 'spinner 1.5s linear infinite 0.75s',
      },
      keyframes: {
        spinner: {
          '0%': { transform: 'scale(0)', opacity: 1 },
          '100%': { transform: 'scale(1)', opacity: 0 },
        },
      },
    },
  },
  plugins: [],
};
