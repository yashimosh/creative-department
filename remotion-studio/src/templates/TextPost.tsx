/**
 * TextPost — animated text on branded background.
 * Use for: quotes, stats, hot takes, single observations.
 *
 * Props-driven: feed in the text, get a video.
 * The simplest template — one message, animated in, hard stop.
 */

import React from "react";
import { useVideoConfig, Sequence } from "remotion";
import { brand } from "../brand/tokens";
import { BrandFrame, TextReveal, DividerLine, LowerThird } from "../components";

export interface TextPostProps {
  headline: string;
  body?: string;
  attribution?: string;
  variant?: "dark" | "light";
  [key: string]: unknown;
}

export const TextPost: React.FC<TextPostProps> = ({
  headline,
  body,
  attribution,
  variant = "dark",
}) => {
  const { width } = useVideoConfig();
  const isVertical = width < 1200;

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;
  const mutedColor = brand.colors.text.secondary;

  return (
    <BrandFrame variant={variant} padding={isVertical ? 60 : 80}>
      {/* Headline */}
      <Sequence from={10}>
        <div style={{ maxWidth: isVertical ? "100%" : "80%" }}>
          <TextReveal
            text={headline}
            mode="word"
            fontSize={isVertical ? brand.typography.scale["3xl"] : brand.typography.scale["4xl"]}
            color={textColor}
            fontStyle="display"
          />
        </div>
      </Sequence>

      {/* Divider */}
      {body && (
        <Sequence from={30}>
          <div style={{ marginTop: brand.spacing.xl, marginBottom: brand.spacing.xl }}>
            <DividerLine color={mutedColor} />
          </div>
        </Sequence>
      )}

      {/* Body */}
      {body && (
        <Sequence from={40}>
          <div style={{ maxWidth: isVertical ? "100%" : "70%" }}>
            <TextReveal
              text={body}
              mode="word"
              fontSize={isVertical ? brand.typography.scale.lg : brand.typography.scale.xl}
              color={mutedColor}
              fontStyle="body"
            />
          </div>
        </Sequence>
      )}

      {/* Attribution */}
      {attribution && (
        <Sequence from={60}>
          <LowerThird
            handle={attribution}
            startFrame={0}
          />
        </Sequence>
      )}
    </BrandFrame>
  );
};
