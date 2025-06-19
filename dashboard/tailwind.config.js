/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#ec1c24', // State Farm red
        secondary: '#ffffff',
        accent: '#f5f5f5',
        dark: '#222222',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        xl: '1rem',
        '3xl': '2rem',
      },
      boxShadow: {
        card: '0 4px 24px 0 rgba(236,28,36,0.08)',
        '2xl': '0 8px 32px 0 rgba(236,28,36,0.12)',
        '3xl': '0 16px 48px 0 rgba(236,28,36,0.16)',
      },
      keyframes: {
        'fade-in': {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        'fade-in-slow': {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        'grow-bar': {
          '0%': { width: '0' },
          '100%': { width: '5rem' },
        },
        'gradient-x': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.8s ease-out',
        'fade-in-slow': 'fade-in-slow 1.5s ease-out',
        'grow-bar': 'grow-bar 1s cubic-bezier(0.4,0,0.2,1)',
        'gradient-x': 'gradient-x 4s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
