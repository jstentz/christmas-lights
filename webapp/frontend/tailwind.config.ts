import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      aspectRatio: {
        '4/3': '4 / 3',
      },
      keyframes: {
        click: {
          '0%': {transform: 'scale(1.0)'},
          '50%': {transform: 'scale(0.9)'},
          '100%': {transform: 'scale(1.0)'},
        }
      },
      animation: {
        click: 'click 0.2s',
      },
    },
  },
  plugins: [require('tailwind-scrollbar')],
};
export default config;
