/**
 * BrandFilm — manifesto-style brand video.
 * Use for: about/intro videos, brand launches, positioning pieces.
 *
 * Slow, deliberate pacing. Each statement gets its own screen.
 * The emptiness between statements IS the design.
 *
 * Note: this is for the brand, not the content.
 * It does NOT follow the "no manifesto energy" rule —
 * because a brand film IS a manifesto. The social content rule
 * is about not performing belief in daily posts.
 */

import React from "react";
import { Sequence, useVideoConfig } from "remotion";
import { brand } from "../brand/tokens";
import { BrandFrame, TextReveal, DividerLine, LowerThird, Transition } from "../components";

export interface BrandFilmProps {
  statements: string[];
  closingLine: string;
  variant?: "dark" | "light";
  [key: string]: unknown;
}

export const BrandFilm: React.FC<BrandFilmProps> = ({
  statements,
  closingLine,
  variant = "dark",
}) => {
  const { durationInFrames } = useVideoConfig();

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;

  const closingFrames = 90;
  const statementFrames = Math.floor(
    (durationInFrames - closingFrames) / statements.length
  );

  return (
    <BrandFrame variant={variant} padding={0}>
      {/* Statements — one per screen, centered, slow */}
      {statements.map((statement, i) => {
        const start = i * statementFrames;

        return (
          <Sequence key={i} from={start} durationInFrames={statementFrames}>
            <Transition type="fade" startFrame={0} durationFrames={20}>
              <BrandFrame
                variant={variant}
                padding={100}
                style={{
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <TextReveal
                  text={statement}
                  mode="word"
                  fontSize={brand.typography.scale["3xl"]}
                  color={textColor}
                  fontStyle="heading"
                  startFrame={15}
                  style={{
                    textAlign: "center",
                    justifyContent: "center",
                    maxWidth: "80%",
                    lineHeight: "1.4",
                  }}
                />
              </BrandFrame>
            </Transition>
          </Sequence>
        );
      })}

      {/* Closing — the line that defines the brand */}
      <Sequence
        from={durationInFrames - closingFrames}
        durationInFrames={closingFrames}
      >
        <Transition type="fade" startFrame={0}>
          <BrandFrame
            variant={variant}
            padding={100}
            style={{
              justifyContent: "center",
              alignItems: "center",
              gap: brand.spacing.xl,
            }}
          >
            <DividerLine startFrame={10} color={brand.colors.accent} width="20%" />
            <TextReveal
              text={closingLine}
              mode="word"
              fontSize={brand.typography.scale["4xl"]}
              color={textColor}
              fontStyle="display"
              startFrame={20}
              style={{ textAlign: "center", justifyContent: "center" }}
            />
            <LowerThird
              startFrame={40}
              handle={brand.name}
              context={brand.handle}
              position="bottom"
            />
          </BrandFrame>
        </Transition>
      </Sequence>
    </BrandFrame>
  );
};
