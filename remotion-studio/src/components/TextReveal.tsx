/**
 * TextReveal — animates text appearing character-by-character or word-by-word.
 * The core text animation for this package. No bouncing. No flourish.
 * Text appears with controlled opacity and slight upward movement.
 */

import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";
import { brand } from "../brand/tokens";
import { theme } from "../brand/theme";

type RevealMode = "word" | "character" | "line";

interface TextRevealProps {
  text: string;
  mode?: RevealMode;
  startFrame?: number;
  style?: React.CSSProperties;
  fontSize?: number;
  color?: string;
  fontStyle?: "display" | "heading" | "body" | "mono";
}

export const TextReveal: React.FC<TextRevealProps> = ({
  text,
  mode = "word",
  startFrame = 0,
  style = {},
  fontSize = brand.typography.scale.xl,
  color = brand.colors.text.primary,
  fontStyle = "heading",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const units =
    mode === "word"
      ? text.split(" ")
      : mode === "character"
        ? text.split("")
        : text.split("\n");

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: mode === "character" ? 0 : fontSize * 0.3,
        ...theme.text[fontStyle],
        fontSize,
        color,
        lineHeight: 1.2,
        ...style,
      }}
    >
      {units.map((unit, i) => {
        const delay = startFrame + i * brand.motion.stagger.normal;
        const progress = spring({
          frame: frame - delay,
          fps,
          config: brand.motion.easing.text,
        });

        const opacity = interpolate(progress, [0, 1], [0, 1]);
        const translateY = interpolate(progress, [0, 1], [12, 0]);

        return (
          <span
            key={i}
            style={{
              opacity,
              transform: `translateY(${translateY}px)`,
              display: "inline-block",
              whiteSpace: mode === "line" ? "pre-wrap" : "pre",
            }}
          >
            {unit}
            {mode === "word" ? " " : ""}
          </span>
        );
      })}
    </div>
  );
};
