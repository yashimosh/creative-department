/**
 * DividerLine — animated horizontal rule.
 * Extends from left to right. Clean, minimal.
 */

import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { brand } from "../brand/tokens";

interface DividerLineProps {
  startFrame?: number;
  color?: string;
  thickness?: number;
  width?: string;
}

export const DividerLine: React.FC<DividerLineProps> = ({
  startFrame = 0,
  color = brand.colors.accent,
  thickness = 1,
  width = "100%",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: brand.motion.easing.default,
  });

  const scaleX = interpolate(progress, [0, 1], [0, 1]);

  return (
    <div
      style={{
        width,
        height: thickness,
        backgroundColor: color,
        transformOrigin: "left center",
        transform: `scaleX(${scaleX})`,
      }}
    />
  );
};
