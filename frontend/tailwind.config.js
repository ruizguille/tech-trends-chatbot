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
        'primary-blue': 'rgb(156, 176, 214)',
        'secondary-blue': 'rgb(208, 233, 235)',
        'primary-purple': 'rgb(132, 112, 190)',
        'gray-medium': 'rgb(122, 122, 122)',
        'gray-light': 'rgb(245, 245, 245)',
        'main-text': 'rgb(53, 55, 64)',
        'error-red': 'rgb(208, 69, 82)',
        // 'primary-blue': 'rgb(178, 217, 231)',
        // 'primary-orange': 'rgb(243, 195, 177)',
        // 'main-text': 'rgb(107, 107, 107)',
        // 'light-gray': 'rgb(244, 244, 244)',
      },
      animation: {
        'spinner': 'spinner 2s linear infinite',
        'spinner-delayed': 'spinner 2s linear infinite 1s',
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
