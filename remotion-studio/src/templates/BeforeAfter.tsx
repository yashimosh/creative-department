/**
 * BeforeAfter — split-screen reveal for comparisons.
 * Use for: transformations, corrections, this-vs-that, improvements.
 *
 * Left side appears first (the "before"), then a divider sweeps,
 * revealing the right side (the "after"). Clean, functional.
 */

import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Sequence,
} from "remotion";
import { brand } from "../brand/tokens";
import { BrandFrame, TextReveal, LowerThird } from "../components";

export interface BeforeAfterProps {
  beforeLabel?: string;
  afterLabel?: string;
  beforeText: string;
  afterText: string;
  variant?: "dark" | "light";
  [key: string]: unknown;
}

export const BeforeAfter: React.FC<BeforeAfterProps> = ({
  beforeLabel = "Before",
  afterLabel = "After",
  beforeText,
  afterText,
  variant = "dark",
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;
  const mutedColor = brand.colors.text.secondary;

  // Divider sweeps at frame 90
  const dividerProgress = spring({
    frame: frame - 90,
    fps,
    config: { mass: 1, damping: 20, stiffness: 100 },
  });

  const dividerX = interpolate(dividerProgress, [0, 1], [0, width / 2]);
  const isVertical = width < 1200;
  const panelPadding = brand.spacing["2xl"];

  return (
    <BrandFrame variant={variant} padding={0}>
      {/* Before side */}
      <Sequence from={10}>
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: isVertical ? "100%" : "50%",
            height: isVertical ? "50%" : "100%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            padding: panelPadding,
          }}
        >
          <div
            style={{
              fontSize: brand.typography.scale.sm,
              color: mutedColor,
              textTransform: "uppercase",
              letterSpacing: "0.1em",
              fontFamily: brand.typography.mono.family,
              marginBottom: brand.spacing.md,
            }}
          >
            {beforeLabel}
          </div>
          <TextReveal
            text={beforeText}
            mode="word"
            fontSize={brand.typography.scale.xl}
            color={textColor}
            fontStyle="body"
          />
        </div>
      </Sequence>

      {/* Divider */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: isVertical ? 0 : dividerX,
          width: isVertical ? "100%" : 2,
          height: isVertical ? 2 : "100%",
          backgroundColor: brand.colors.accent,
          ...(isVertical ? { top: height / 2 } : {}),
        }}
      />

      {/* After side */}
      <Sequence from={100}>
        <div
          style={{
            position: "absolute",
            top: isVertical ? "50%" : 0,
            left: isVertical ? 0 : "50%",
            width: isVertical ? "100%" : "50%",
            height: isVertical ? "50%" : "100%",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            padding: panelPadding,
          }}
        >
          <div
            style={{
              fontSize: brand.typography.scale.sm,
              color: mutedColor,
              textTransform: "uppercase",
              letterSpacing: "0.1em",
              fontFamily: brand.typography.mono.family,
              marginBottom: brand.spacing.md,
            }}
          >
            {afterLabel}
          </div>
          <TextReveal
            text={afterText}
            mode="word"
            fontSize={brand.typography.scale.xl}
            color={textColor}
            fontStyle="body"
          />
        </div>
      </Sequence>

      <Sequence from={15}>
        <LowerThird startFrame={0} />
      </Sequence>
    </BrandFrame>
  );
};
