/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        space: {
          950: "#0a0a1a",   // page background
          900: "#0f0f24",   // sidebar / hero panel
          800: "#15152e",   // card background
          700: "#1e1e3c",   // card border / hover
          600: "#2a2a52",   // subtle border
        },
        nebula: {
          500: "#7c3aed",   // violet
          400: "#a855f7",   // purple
          pink: "#ec4899",
          blue: "#3b82f6",
          cyan: "#06b6d4",
        },
      },
      fontFamily: {
        display: ["Sora", "ui-sans-serif", "system-ui"],
        body: ["Inter", "ui-sans-serif", "system-ui"],
      },
      backgroundImage: {
        "nebula-gradient": "linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #ec4899 100%)",
        "nebula-radial": "radial-gradient(circle at 20% 20%, rgba(124,58,237,0.25), transparent 40%), radial-gradient(circle at 80% 70%, rgba(236,72,153,0.15), transparent 40%)",
      },
      boxShadow: {
        glow: "0 0 40px rgba(124, 58, 237, 0.25)",
      },
    },
  },
  plugins: [],
};
