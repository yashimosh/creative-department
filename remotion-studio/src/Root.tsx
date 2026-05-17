/**
 * Root — Remotion entry point.
 * Registers all compositions (templates + productions) with their default props.
 *
 * Default props shown here are generic demo content for the Remotion Studio
 * preview. Replace them with your brand's real content when you render.
 *
 * To add a new composition:
 * 1. Create the component in src/templates/ or src/productions/
 * 2. Register it here with a Composition element
 * 3. Set default props for the Remotion Studio preview
 */

import React from "react";
import { Composition } from "remotion";
import { brand } from "./brand/tokens";

// Templates (Phase 1 — social video)
import { TextPost, TextPostProps } from "./templates/TextPost";
import { CaptionReel, CaptionReelProps } from "./templates/CaptionReel";
import { Listicle, ListicleProps } from "./templates/Listicle";
import { BeforeAfter, BeforeAfterProps } from "./templates/BeforeAfter";
import { Announcement, AnnouncementProps } from "./templates/Announcement";

// Productions (Phase 2 — complex video)
import { Explainer, ExplainerProps } from "./productions/Explainer";
import { DataViz, DataVizProps } from "./productions/DataViz";
import { BrandFilm, BrandFilmProps } from "./productions/BrandFilm";
import { DemoVideo, DemoVideoProps } from "./productions/DemoVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* ========== TEMPLATES ========== */}

      {/* TextPost — all platform variants */}
      <Composition
        id="TextPost-Reel"
        component={TextPost}
        {...brand.formats.reel}
        durationInFrames={150}
        defaultProps={{
          headline: "The headline does the weight.",
          body: "Supporting copy carries the argument one layer down.",
          variant: "dark" as const,
        }}
      />
      <Composition
        id="TextPost-Square"
        component={TextPost}
        {...brand.formats.feedSquare}
        durationInFrames={150}
        defaultProps={{
          headline: "The headline does the weight.",
          body: "Supporting copy carries the argument one layer down.",
          variant: "dark" as const,
        }}
      />
      <Composition
        id="TextPost-YouTube"
        component={TextPost}
        {...brand.formats.youtube}
        durationInFrames={150}
        defaultProps={{
          headline: "The headline does the weight.",
          body: "Supporting copy carries the argument one layer down.",
          variant: "dark" as const,
        }}
      />

      {/* CaptionReel */}
      <Composition
        id="CaptionReel"
        component={CaptionReel as React.FC<CaptionReelProps>}
        {...brand.formats.reel}
        durationInFrames={300}
        defaultProps={{
          hook: "Most tools in this space are loud.",
          points: [
            "This one isn't.",
            "The gates are hard.",
            "The output is quiet.",
          ],
          hardStop: "It works.",
          variant: "dark" as const,
        }}
      />

      {/* Listicle */}
      <Composition
        id="Listicle-Reel"
        component={Listicle as React.FC<ListicleProps>}
        {...brand.formats.reel}
        durationInFrames={360}
        defaultProps={{
          title: "Four working rules",
          items: [
            "Clarity over cleverness.",
            "Show the system, not the ad.",
            "Absence is a signal too.",
            "Specificity is the measure.",
          ],
          variant: "dark" as const,
        }}
      />

      {/* BeforeAfter */}
      <Composition
        id="BeforeAfter-Reel"
        component={BeforeAfter as React.FC<BeforeAfterProps>}
        {...brand.formats.reel}
        durationInFrames={240}
        defaultProps={{
          beforeLabel: "Before",
          afterLabel: "After",
          beforeText: "A vague statement that anyone could write.",
          afterText: "A specific detail that only the person who built it would know.",
          variant: "dark" as const,
        }}
      />
      <Composition
        id="BeforeAfter-YouTube"
        component={BeforeAfter as React.FC<BeforeAfterProps>}
        {...brand.formats.youtube}
        durationInFrames={240}
        defaultProps={{
          beforeLabel: "Before",
          afterLabel: "After",
          beforeText: "Vague summary that anyone could write.",
          afterText: "Specific detail that only the person who built it would know.",
          variant: "dark" as const,
        }}
      />

      {/* Announcement */}
      <Composition
        id="Announcement-Reel"
        component={Announcement as React.FC<AnnouncementProps>}
        {...brand.formats.reel}
        durationInFrames={180}
        defaultProps={{
          title: "Your Brand",
          description: "A one-line description of what this thing is, or what it does, or who it's for.",
          tagline: "The tagline goes here.",
          variant: "dark" as const,
        }}
      />

      {/* ========== PRODUCTIONS ========== */}

      {/* Explainer */}
      <Composition
        id="Explainer-YouTube"
        component={Explainer as React.FC<ExplainerProps>}
        {...brand.formats.youtube}
        durationInFrames={600}
        defaultProps={{
          title: "The Pattern You're Arguing With",
          scenes: [
            {
              title: "The Observation",
              emphasis: "Name the pattern in one sentence.",
              body: "Short historical context or a precedent. Two lines maximum.",
            },
            {
              title: "The Application",
              body: "Where this pattern shows up in the specific thing you're writing about.",
            },
            {
              title: "The Consequence",
              emphasis: "What the pattern forces you to face.",
              body: "One uncomfortable truth, stated plainly.",
            },
          ],
          outro: "Hard stop.",
          variant: "dark" as const,
        }}
      />
      <Composition
        id="Explainer-Reel"
        component={Explainer as React.FC<ExplainerProps>}
        {...brand.formats.reel}
        durationInFrames={450}
        defaultProps={{
          title: "The Pattern You're Arguing With",
          scenes: [
            {
              emphasis: "Name the pattern in one sentence.",
              body: "Short historical context or a precedent.",
            },
            {
              body: "Where this pattern shows up in the specific thing you're writing about.",
            },
          ],
          outro: "Hard stop.",
          variant: "dark" as const,
        }}
      />

      {/* DataViz */}
      <Composition
        id="DataViz-YouTube"
        component={DataViz as React.FC<DataVizProps>}
        {...brand.formats.youtube}
        durationInFrames={450}
        defaultProps={{
          title: "The System — By the Numbers",
          dataPoints: [
            { label: "Skills in the package", value: 3, context: "remotion-studio, whisper, audio-enhance" },
            { label: "Clients shown as example", value: 1, context: "example-brand — fork as your starting point" },
            { label: "Pipeline stages", value: 5, suffix: "", context: "DRAFT → REVIEW → REGISTER → SCHEDULE → LOG" },
          ],
          variant: "dark" as const,
        }}
      />

      {/* BrandFilm */}
      <Composition
        id="BrandFilm"
        component={BrandFilm as React.FC<BrandFilmProps>}
        {...brand.formats.youtube}
        durationInFrames={600}
        defaultProps={{
          statements: [
            "A brand is a claim.",
            "Structure shapes behavior.",
            "Authority comes from specificity.",
            "The tool is the shape of the thinking.",
          ],
          closingLine: "Your Brand",
          variant: "dark" as const,
        }}
      />

      {/* DemoVideo */}
      <Composition
        id="DemoVideo-YouTube"
        component={DemoVideo as React.FC<DemoVideoProps>}
        {...brand.formats.youtube}
        durationInFrames={600}
        defaultProps={{
          projectName: "Your Project",
          tagline: "One line that says what this is and who it's for.",
          steps: [
            { title: "Step 1", description: "A request enters the system. Classification and routing decide where it goes." },
            { title: "Step 2", description: "Skills communicate through structured dispatches. No manual handoff." },
            { title: "Step 3", description: "Copy first, design second, motion third. Each skill updates the registry." },
            { title: "Step 4", description: "Review gates run. Real disagreements get harvested, style noise gets dropped." },
            { title: "Step 5", description: "Published. Registered. Logged. Complete audit trail." },
          ],
          variant: "dark" as const,
        }}
      />
    </>
  );
};
