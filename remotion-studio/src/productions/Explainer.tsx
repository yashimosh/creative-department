/**
 * Explainer — multi-scene concept breakdown video.
 * Use for: explaining frameworks, showing processes, concept videos.
 *
 * Takes an array of scenes, each with its own text and optional visual.
 * Sequences them with brand transitions. Longer form than templates.
 */

import React from "react";
import { Sequence, useVideoConfig } from "remotion";
import { brand } from "../brand/tokens";
import {
  BrandFrame,
  TextReveal,
  DividerLine,
  LowerThird,
  Transition,
} from "../components";

export interface ExplainerScene {
  title?: string;
  body: string;
  emphasis?: string; // A key stat, quote, or takeaway — displayed large
}

export interface ExplainerProps {
  title: string;
  scenes: ExplainerScene[];
  outro?: string;
  variant?: "dark" | "light";
  [key: string]: unknown;
}

export const Explainer: React.FC<ExplainerProps> = ({
  title,
  scenes,
  outro,
  variant = "dark",
}) => {
  const { durationInFrames } = useVideoConfig();

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;
  const mutedColor = brand.colors.text.secondary;

  // Timing: title gets 3s, each scene gets equal share, outro gets 2s
  const titleFrames = 90;
  const outroFrames = outro ? 60 : 0;
  const sceneFrames = Math.floor(
    (durationInFrames - titleFrames - outroFrames) / scenes.length
  );

  return (
    <BrandFrame variant={variant} padding={60}>
      {/* Title card */}
      <Sequence from={0} durationInFrames={titleFrames}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            height: "100%",
            gap: brand.spacing.xl,
          }}
        >
          <TextReveal
            text={title}
            mode="word"
            fontSize={brand.typography.scale["4xl"]}
            color={textColor}
            fontStyle="display"
            startFrame={10}
            style={{ textAlign: "center", justifyContent: "center" }}
          />
          <DividerLine startFrame={30} color={mutedColor} width="30%" />
        </div>
      </Sequence>

      {/* Scenes */}
      {scenes.map((scene, i) => {
        const sceneStart = titleFrames + i * sceneFrames;

        return (
          <Sequence key={i} from={sceneStart} durationInFrames={sceneFrames}>
            <Transition type="fade" startFrame={0}>
              <BrandFrame variant={variant} padding={60}>
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    height: "100%",
                    gap: brand.spacing.lg,
                  }}
                >
                  {/* Scene number */}
                  <div
                    style={{
                      fontFamily: brand.typography.mono.family,
                      fontSize: brand.typography.scale.sm,
                      color: mutedColor,
                      letterSpacing: "0.1em",
                    }}
                  >
                    {String(i + 1).padStart(2, "0")} / {String(scenes.length).padStart(2, "0")}
                  </div>

                  {/* Scene title */}
                  {scene.title && (
                    <TextReveal
                      text={scene.title}
                      mode="word"
                      fontSize={brand.typography.scale["2xl"]}
                      color={textColor}
                      fontStyle="heading"
                      startFrame={5}
                    />
                  )}

                  {/* Emphasis — large, isolated */}
                  {scene.emphasis && (
                    <TextReveal
                      text={scene.emphasis}
                      mode="word"
                      fontSize={brand.typography.scale["3xl"]}
                      color={textColor}
                      fontStyle="display"
                      startFrame={15}
                    />
                  )}

                  {/* Body */}
                  <TextReveal
                    text={scene.body}
                    mode="word"
                    fontSize={brand.typography.scale.lg}
                    color={mutedColor}
                    fontStyle="body"
                    startFrame={scene.emphasis ? 25 : 15}
                  />
                </div>
              </BrandFrame>
            </Transition>
          </Sequence>
        );
      })}

      {/* Outro */}
      {outro && (
        <Sequence from={durationInFrames - outroFrames} durationInFrames={outroFrames}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
            }}
          >
            <TextReveal
              text={outro}
              mode="word"
              fontSize={brand.typography.scale["2xl"]}
              color={textColor}
              fontStyle="heading"
              startFrame={5}
              style={{ textAlign: "center", justifyContent: "center" }}
            />
          </div>
        </Sequence>
      )}

      <Sequence from={10}>
        <LowerThird startFrame={0} context="Explainer" />
      </Sequence>
    </BrandFrame>
  );
};
