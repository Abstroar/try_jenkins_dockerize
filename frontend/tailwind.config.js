/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cyan': {
          300: '#67e8f9',
          400: '#22d3ee',
          600: '#0891b2',
          700: '#0e7490',
        },
      },
      animation: {
        'pan': 'pan 10s linear infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        pan: {
          '0%': { backgroundPosition: '0% 0%' },
          '100%': { backgroundPosition: '100% 100%' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
} 