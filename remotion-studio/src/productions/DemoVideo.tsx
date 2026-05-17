/**
 * DemoVideo — app walkthrough / product demo.
 * Use for: showcasing built projects, tool demos, feature walkthroughs.
 *
 * Takes a sequence of steps, each with a title and description.
 * Designed to pair with screen recordings or screenshots
 * that get composited in as overlays (added as staticFile assets).
 *
 * This composition provides the text overlay structure —
 * the actual screen content is either a background image/video
 * or rendered by the video-editor skill as a separate layer.
 */

import React from "react";
import { Sequence, useVideoConfig, Img, staticFile } from "remotion";
import { brand } from "../brand/tokens";
import { BrandFrame, TextReveal, DividerLine, LowerThird, Transition } from "../components";

export interface DemoStep {
  title: string;
  description: string;
  screenshotPath?: string; // path relative to public/assets/
}

export interface DemoVideoProps {
  projectName: string;
  tagline: string;
  steps: DemoStep[];
  variant?: "dark" | "light";
  [key: string]: unknown;
}

export const DemoVideo: React.FC<DemoVideoProps> = ({
  projectName,
  tagline,
  steps,
  variant = "dark",
}) => {
  const { durationInFrames, width, height } = useVideoConfig();

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;
  const mutedColor = brand.colors.text.secondary;

  const introFrames = 90;
  const stepFrames = Math.floor(
    (durationInFrames - introFrames - 60) / steps.length
  );

  return (
    <BrandFrame variant={variant} padding={0}>
      {/* Intro */}
      <Sequence from={0} durationInFrames={introFrames}>
        <BrandFrame
          variant={variant}
          padding={80}
          style={{ justifyContent: "center", gap: brand.spacing.lg }}
        >
          <TextReveal
            text={projectName}
            mode="character"
            fontSize={brand.typography.scale["5xl"]}
            color={textColor}
            fontStyle="display"
            startFrame={10}
          />
          <DividerLine startFrame={30} color={mutedColor} width="25%" />
          <TextReveal
            text={tagline}
            mode="word"
            fontSize={brand.typography.scale.xl}
            color={mutedColor}
            fontStyle="body"
            startFrame={40}
          />
        </BrandFrame>
      </Sequence>

      {/* Steps */}
      {steps.map((step, i) => {
        const stepStart = introFrames + i * stepFrames;

        return (
          <Sequence key={i} from={stepStart} durationInFrames={stepFrames}>
            <Transition type="slideUp" startFrame={0}>
              <BrandFrame variant={variant} padding={0}>
                {/* Screenshot background (if provided) */}
                {step.screenshotPath && (
                  <div
                    style={{
                      position: "absolute",
                      top: 0,
                      left: 0,
                      width: "100%",
                      height: "100%",
                      opacity: 0.15,
                    }}
                  >
                    <Img
                      src={staticFile(step.screenshotPath)}
                      style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                      }}
                    />
                  </div>
                )}

                {/* Text overlay */}
                <div
                  style={{
                    position: "absolute",
                    bottom: 0,
                    left: 0,
                    right: 0,
                    padding: brand.spacing["2xl"],
                    background: `linear-gradient(transparent, ${brand.colors.background.dark}ee)`,
                    display: "flex",
                    flexDirection: "column",
                    gap: brand.spacing.sm,
                  }}
                >
                  {/* Step counter */}
                  <div
                    style={{
                      fontFamily: brand.typography.mono.family,
                      fontSize: brand.typography.scale.sm,
                      color: mutedColor,
                      letterSpacing: "0.1em",
                    }}
                  >
                    {String(i + 1).padStart(2, "0")} / {String(steps.length).padStart(2, "0")}
                  </div>

                  <TextReveal
                    text={step.title}
                    mode="word"
                    fontSize={brand.typography.scale["2xl"]}
                    color={textColor}
                    fontStyle="heading"
                    startFrame={5}
                  />
                  <TextReveal
                    text={step.description}
                    mode="word"
                    fontSize={brand.typography.scale.base}
                    color={mutedColor}
                    fontStyle="body"
                    startFrame={15}
                  />
                </div>
              </BrandFrame>
            </Transition>
          </Sequence>
        );
      })}

      {/* Outro */}
      <Sequence from={durationInFrames - 60} durationInFrames={60}>
        <BrandFrame
          variant={variant}
          padding={80}
          style={{ justifyContent: "center", alignItems: "center" }}
        >
          <TextReveal
            text={projectName}
            mode="character"
            fontSize={brand.typography.scale["4xl"]}
            color={textColor}
            fontStyle="display"
            startFrame={5}
            style={{ textAlign: "center", justifyContent: "center" }}
          />
          <LowerThird startFrame={15} position="bottom" />
        </BrandFrame>
      </Sequence>
    </BrandFrame>
  );
};
