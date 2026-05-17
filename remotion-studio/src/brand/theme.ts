/**
 * Theme — derived styles from brand tokens.
 * Components use these instead of raw token values.
 */

import { brand } from "./tokens";

export const theme = {
  // Background presets
  bg: {
    dark: {
      backgroundColor: brand.colors.background.dark,
      color: brand.colors.text.primary,
    },
    light: {
      backgroundColor: brand.colors.background.light,
      color: brand.colors.text.onLight,
    },
  },

  // Typography presets
  text: {
    display: {
      fontFamily: `${brand.typography.display.family}, ${brand.typography.display.fallback}`,
      fontWeight: brand.typography.display.weight,
    },
    heading: {
      fontFamily: `${brand.typography.heading.family}, ${brand.typography.heading.fallback}`,
      fontWeight: brand.typography.heading.weight,
    },
    body: {
      fontFamily: `${brand.typography.body.family}, ${brand.typography.body.fallback}`,
      fontWeight: brand.typography.body.weight,
    },
    mono: {
      fontFamily: `${brand.typography.mono.family}, ${brand.typography.mono.fallback}`,
      fontWeight: brand.typography.mono.weight,
    },
  },

  // Safe zones for platform overlays
  safeZone: {
    reel: {
      top: 150, // username area
      bottom: 270, // CTA/description area
      right: 100, // engagement buttons
    },
    youtubeShort: {
      top: 100,
      bottom: 200,
      right: 80,
    },
    tiktok: {
      top: 150,
      bottom: 270,
      right: 100,
    },
  },
} as const;
