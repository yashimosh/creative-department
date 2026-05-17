/**
 * Brand Tokens — generic starting configuration
 *
 * Source of truth for all visual and motion properties.
 * Every composition imports from here. Change the brand, re-render everything.
 *
 * These are neutral, function-first defaults — near-black primary, no
 * decorative color, sans-serif Inter everywhere. Replace with your
 * brand's real typography, palette, and motion values before rendering.
 */

export const brand = {
  name: "Your Brand",
  handle: "@your-handle",

  colors: {
    // Directional — brutalist, function-first
    primary: "#0A0A0A", // near-black — authority, weight
    secondary: "#1A1A1A", // dark gray — structure
    accent: "#E5E5E5", // light gray — subtle emphasis (no decorative color)
    background: {
      dark: "#0A0A0A",
      light: "#FAFAFA",
    },
    text: {
      primary: "#FAFAFA", // on dark bg
      secondary: "#999999", // muted
      onLight: "#0A0A0A", // on light bg
    },
    // No decorative/brand color. That's the point.
  },

  typography: {
    // Directional — pending final brand fonts
    heading: {
      family: "Inter",
      weight: 700,
      fallback: "system-ui, sans-serif",
    },
    body: {
      family: "Inter",
      weight: 400,
      fallback: "system-ui, sans-serif",
    },
    display: {
      family: "Inter",
      weight: 900,
      fallback: "system-ui, sans-serif",
    },
    mono: {
      family: "JetBrains Mono",
      weight: 400,
      fallback: "monospace",
    },
    scale: {
      xs: 14,
      sm: 16,
      base: 18,
      lg: 22,
      xl: 28,
      "2xl": 36,
      "3xl": 48,
      "4xl": 64,
      "5xl": 80,
      "6xl": 96,
    },
  },

  spacing: {
    unit: 8,
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    "2xl": 48,
    "3xl": 64,
    "4xl": 96,
  },

  motion: {
    // Character: confident, precise, no flourish
    personality: "restrained" as const,
    fps: 30,
    premiumFps: 60,

    duration: {
      fast: 8, // frames at 30fps (~267ms)
      normal: 15, // frames (~500ms)
      slow: 25, // frames (~833ms)
      reveal: 20, // frames — text reveal timing
    },

    easing: {
      // No bouncy springs. No playful overshoot. Controlled.
      default: { mass: 1, damping: 20, stiffness: 200 },
      enter: { mass: 1, damping: 25, stiffness: 180 },
      exit: { mass: 1, damping: 30, stiffness: 200 },
      text: { mass: 0.8, damping: 18, stiffness: 160 },
    },

    stagger: {
      fast: 3, // frames between items
      normal: 5,
      slow: 8,
    },
  },

  // Platform output presets
  formats: {
    reel: { width: 1080, height: 1920, fps: 30 },
    feedSquare: { width: 1080, height: 1080, fps: 30 },
    feedPortrait: { width: 1080, height: 1350, fps: 30 },
    youtube: { width: 1920, height: 1080, fps: 30 },
    youtubeShort: { width: 1080, height: 1920, fps: 30 },
    linkedin: { width: 1920, height: 1080, fps: 30 },
    linkedinSquare: { width: 1080, height: 1080, fps: 30 },
  },

  // Anti-patterns (from CLIENT.md)
  avoid: [
    "Stock photos",
    "Rounded corners",
    "Pastel colors",
    "Decorative imagery",
    "Anything that signals 'content creator'",
    "Gradients",
    "Emoji in video content",
    "Bouncy/playful animations",
  ],
} as const;

export type BrandFormat = keyof typeof brand.formats;
export type BrandColor = typeof brand.colors;
