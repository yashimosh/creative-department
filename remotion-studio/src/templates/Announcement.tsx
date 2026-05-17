/**
 * Announcement — big reveal with brand framing.
 * Use for: launches, new work, project reveals.
 *
 * Structure: title fades up → brief description → hard stop.
 * No fireworks, no confetti. The restraint IS the announcement.
 */

import React from "react";
import { Sequence, useVideoConfig } from "remotion";
import { brand } from "../brand/tokens";
import { BrandFrame, TextReveal, DividerLine, LowerThird } from "../components";

export interface AnnouncementProps {
  title: string;
  description: string;
  tagline?: string;
  variant?: "dark" | "light";
  [key: string]: unknown;
}

export const Announcement: React.FC<AnnouncementProps> = ({
  title,
  description,
  tagline,
  variant = "dark",
}) => {
  const { durationInFrames } = useVideoConfig();

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;
  const mutedColor = brand.colors.text.secondary;

  return (
    <BrandFrame
      variant={variant}
      padding={80}
      style={{ justifyContent: "center", gap: brand.spacing.xl }}
    >
      {/* Title — the thing being announced */}
      <Sequence from={15}>
        <TextReveal
          text={title}
          mode="word"
          fontSize={brand.typography.scale["5xl"]}
          color={textColor}
          fontStyle="display"
        />
      </Sequence>

      {/* Divider */}
      <Sequence from={40}>
        <DividerLine color={mutedColor} width="40%" />
      </Sequence>

      {/* Description */}
      <Sequence from={50}>
        <div style={{ maxWidth: "80%" }}>
          <TextReveal
            text={description}
            mode="word"
            fontSize={brand.typography.scale.xl}
            color={mutedColor}
            fontStyle="body"
          />
        </div>
      </Sequence>

      {/* Tagline — short, final */}
      {tagline && (
        <Sequence from={90}>
          <TextReveal
            text={tagline}
            mode="word"
            fontSize={brand.typography.scale.lg}
            color={textColor}
            fontStyle="heading"
          />
        </Sequence>
      )}

      <Sequence from={20}>
        <LowerThird
          startFrame={0}
          context="New Work"
        />
      </Sequence>
    </BrandFrame>
  );
};
