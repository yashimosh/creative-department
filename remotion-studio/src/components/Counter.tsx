/**
 * Counter — animated number counter for data visualization.
 * Counts from 0 to target value with eased interpolation.
 */

import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { brand } from "../brand/tokens";
import { theme } from "../brand/theme";

interface CounterProps {
  value: number;
  prefix?: string;
  suffix?: string;
  startFrame?: number;
  decimals?: number;
  fontSize?: number;
  color?: string;
}

export const Counter: React.FC<CounterProps> = ({
  value,
  prefix = "",
  suffix = "",
  startFrame = 0,
  decimals = 0,
  fontSize = brand.typography.scale["4xl"],
  color = brand.colors.text.primary,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: { mass: 1, damping: 25, stiffness: 80 },
  });

  const currentValue = interpolate(progress, [0, 1], [0, value]);
  const displayValue = currentValue.toFixed(decimals);

  return (
    <div
      style={{
        ...theme.text.display,
        fontSize,
        color,
        letterSpacing: "-0.03em",
        fontVariantNumeric: "tabular-nums",
      }}
    >
      {prefix}
      {displayValue}
      {suffix}
    </div>
  );
};
