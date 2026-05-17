/**
 * LowerThird — brand attribution bar.
 * Appears at the bottom of video with handle and optional context.
 */

import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { brand } from "../brand/tokens";
import { theme } from "../brand/theme";

interface LowerThirdProps {
  handle?: string;
  context?: string; // e.g., "Systems Strategy" or "Creative Direction"
  startFrame?: number;
  position?: "bottom" | "top";
}

export const LowerThird: React.FC<LowerThirdProps> = ({
  handle = brand.handle,
  context,
  startFrame = 0,
  position = "bottom",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: brand.motion.easing.enter,
  });

  const translateX = interpolate(progress, [0, 1], [-100, 0]);

  return (
    <div
      style={{
        position: "absolute",
        [position]: brand.spacing["2xl"],
        left: brand.spacing["2xl"],
        display: "flex",
        flexDirection: "column",
        gap: brand.spacing.xs,
        opacity: progress,
        transform: `translateX(${translateX}px)`,
      }}
    >
      <div
        style={{
          ...theme.text.heading,
          fontSize: brand.typography.scale.lg,
          color: brand.colors.text.primary,
          letterSpacing: "-0.02em",
        }}
      >
        {handle}
      </div>
      {context && (
        <div
          style={{
            ...theme.text.body,
            fontSize: brand.typography.scale.sm,
            color: brand.colors.text.secondary,
            textTransform: "uppercase",
            letterSpacing: "0.1em",
          }}
        >
          {context}
        </div>
      )}
    </div>
  );
};
