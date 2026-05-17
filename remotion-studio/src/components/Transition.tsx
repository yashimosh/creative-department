/**
 * Transition — brand-consistent scene transitions.
 * Clean cuts and controlled fades. No wipes, no spins, no zoom-throughs.
 */

import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  AbsoluteFill,
} from "remotion";
import { brand } from "../brand/tokens";

type TransitionType = "cut" | "fade" | "wipeDown" | "slideUp";

interface TransitionProps {
  type?: TransitionType;
  startFrame: number;
  durationFrames?: number;
  children: React.ReactNode;
}

export const Transition: React.FC<TransitionProps> = ({
  type = "fade",
  startFrame,
  durationFrames = brand.motion.duration.normal,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (type === "cut") {
    return (
      <AbsoluteFill style={{ opacity: frame >= startFrame ? 1 : 0 }}>
        {children}
      </AbsoluteFill>
    );
  }

  if (type === "fade") {
    const progress = spring({
      frame: frame - startFrame,
      fps,
      config: brand.motion.easing.enter,
    });

    return (
      <AbsoluteFill style={{ opacity: progress }}>
        {children}
      </AbsoluteFill>
    );
  }

  if (type === "slideUp") {
    const progress = spring({
      frame: frame - startFrame,
      fps,
      config: brand.motion.easing.enter,
    });

    const translateY = interpolate(progress, [0, 1], [40, 0]);

    return (
      <AbsoluteFill
        style={{
          opacity: progress,
          transform: `translateY(${translateY}px)`,
        }}
      >
        {children}
      </AbsoluteFill>
    );
  }

  if (type === "wipeDown") {
    const progress = interpolate(
      frame,
      [startFrame, startFrame + durationFrames],
      [0, 100],
      { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
    );

    return (
      <AbsoluteFill
        style={{
          clipPath: `inset(0 0 ${100 - progress}% 0)`,
        }}
      >
        {children}
      </AbsoluteFill>
    );
  }

  return <AbsoluteFill>{children}</AbsoluteFill>;
};
