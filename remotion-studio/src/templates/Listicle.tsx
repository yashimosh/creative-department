/**
 * Listicle — numbered points appearing one by one.
 * Use for: "5 things I learned," frameworks, principles, observations.
 *
 * Each point appears with its number, holds, then the next arrives.
 * Clean stagger. No flashy transitions.
 */

import React from "react";
import { Sequence, useVideoConfig } from "remotion";
import { brand } from "../brand/tokens";
import { BrandFrame, TextReveal, LowerThird } from "../components";

export interface ListicleProps {
  title: string;
  items: string[];
  variant?: "dark" | "light";
  [key: string]: unknown;
}

export const Listicle: React.FC<ListicleProps> = ({
  title,
  items,
  variant = "dark",
}) => {
  const { durationInFrames } = useVideoConfig();

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;
  const mutedColor = brand.colors.text.secondary;
  const accentColor = brand.colors.accent;

  const titleDuration = 60;
  const itemDuration = Math.floor(
    (durationInFrames - titleDuration - 30) / items.length
  );

  return (
    <BrandFrame variant={variant} padding={60}>
      {/* Title */}
      <Sequence from={5} durationInFrames={titleDuration}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "100%",
          }}
        >
          <TextReveal
            text={title}
            mode="word"
            fontSize={brand.typography.scale["3xl"]}
            color={textColor}
            fontStyle="display"
            style={{ textAlign: "center", justifyContent: "center" }}
          />
        </div>
      </Sequence>

      {/* Items */}
      {items.map((item, i) => (
        <Sequence
          key={i}
          from={titleDuration + i * itemDuration}
          durationInFrames={itemDuration}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              height: "100%",
              paddingLeft: brand.spacing["2xl"],
              paddingRight: brand.spacing["2xl"],
            }}
          >
            {/* Number */}
            <TextReveal
              text={`${String(i + 1).padStart(2, "0")}`}
              mode="character"
              fontSize={brand.typography.scale["5xl"]}
              color={accentColor}
              fontStyle="mono"
              startFrame={0}
            />
            {/* Item text */}
            <div style={{ marginTop: brand.spacing.md }}>
              <TextReveal
                text={item}
                mode="word"
                fontSize={brand.typography.scale.xl}
                color={textColor}
                fontStyle="body"
                startFrame={8}
              />
            </div>
          </div>
        </Sequence>
      ))}

      <Sequence from={15}>
        <LowerThird startFrame={0} />
      </Sequence>
    </BrandFrame>
  );
};
