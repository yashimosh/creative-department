/**
 * CaptionReel — kinetic typography for short-form video.
 * Use for: Reels, Shorts, TikToks with text-driven content.
 *
 * Structure mirrors the brand voice pattern:
 * 1. Hook (big, fast)
 * 2. Body points (staggered reveal)
 * 3. Hard stop (final line, isolated)
 *
 * No resolution. No CTA. The last line just... lands.
 */

import React from "react";
import { Sequence, useVideoConfig } from "remotion";
import { brand } from "../brand/tokens";
import { BrandFrame, TextReveal, DividerLine, LowerThird } from "../components";

export interface CaptionReelProps {
  hook: string;
  points: string[];
  hardStop: string;
  variant?: "dark" | "light";
  [key: string]: unknown;
}

export const CaptionReel: React.FC<CaptionReelProps> = ({
  hook,
  points,
  hardStop,
  variant = "dark",
}) => {
  const { durationInFrames } = useVideoConfig();

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;
  const mutedColor = brand.colors.text.secondary;

  // Timing: hook gets 2s, each point gets 2s, hard stop gets last 2s
  const hookDuration = 60;
  const pointDuration = 60;
  const hardStopStart = hookDuration + points.length * pointDuration;

  return (
    <BrandFrame variant={variant} padding={60}>
      {/* Hook — big, centered, immediate */}
      <Sequence from={5} durationInFrames={hookDuration}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%",
          }}
        >
          <TextReveal
            text={hook}
            mode="word"
            fontSize={brand.typography.scale["4xl"]}
            color={textColor}
            fontStyle="display"
            style={{ textAlign: "center", justifyContent: "center" }}
          />
        </div>
      </Sequence>

      {/* Body points — staggered, left-aligned */}
      {points.map((point, i) => (
        <Sequence
          key={i}
          from={hookDuration + i * pointDuration}
          durationInFrames={pointDuration}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              height: "100%",
              paddingLeft: brand.spacing.xl,
              paddingRight: brand.spacing.xl,
            }}
          >
            <DividerLine startFrame={0} color={mutedColor} />
            <div style={{ marginTop: brand.spacing.lg }}>
              <TextReveal
                text={point}
                mode="word"
                fontSize={brand.typography.scale["2xl"]}
                color={textColor}
                fontStyle="heading"
                startFrame={5}
              />
            </div>
          </div>
        </Sequence>
      ))}

      {/* Hard stop — the line that lands */}
      <Sequence from={hardStopStart} durationInFrames={durationInFrames - hardStopStart}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%",
          }}
        >
          <TextReveal
            text={hardStop}
            mode="word"
            fontSize={brand.typography.scale["3xl"]}
            color={textColor}
            fontStyle="display"
            style={{ textAlign: "center", justifyContent: "center" }}
          />
        </div>
      </Sequence>

      {/* Lower third — persists through all scenes */}
      <Sequence from={15}>
        <LowerThird startFrame={0} />
      </Sequence>
    </BrandFrame>
  );
};
