/**
 * BrandFrame — the standard frame wrapper for all compositions.
 * Applies brand background, padding, and safe zones.
 */

import React from "react";
import { AbsoluteFill } from "remotion";
import { brand } from "../brand/tokens";

interface BrandFrameProps {
  variant?: "dark" | "light";
  padding?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}

export const BrandFrame: React.FC<BrandFrameProps> = ({
  variant = "dark",
  padding = brand.spacing["2xl"],
  children,
  style = {},
}) => {
  const bg =
    variant === "dark"
      ? brand.colors.background.dark
      : brand.colors.background.light;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bg,
        padding,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        ...style,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};
