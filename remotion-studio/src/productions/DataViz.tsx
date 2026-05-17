/**
 * DataViz — animated data visualization video.
 * Use for: metrics, stats, performance reports, dashboards.
 *
 * Takes an array of data points and animates them as counters
 * with contextual labels. Can also display comparison bars.
 */

import React from "react";
import { Sequence, useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";
import { brand } from "../brand/tokens";
import { BrandFrame, TextReveal, Counter, DividerLine, LowerThird } from "../components";

export interface DataPoint {
  label: string;
  value: number;
  prefix?: string;
  suffix?: string;
  context?: string; // e.g., "up 23% from last month"
}

export interface DataVizProps {
  title: string;
  dataPoints: DataPoint[];
  variant?: "dark" | "light";
  [key: string]: unknown;
}

const BarChart: React.FC<{
  value: number;
  maxValue: number;
  startFrame: number;
  color: string;
}> = ({ value, maxValue, startFrame, color }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - startFrame,
    fps,
    config: { mass: 1, damping: 20, stiffness: 100 },
  });

  const barWidth = interpolate(progress, [0, 1], [0, (value / maxValue) * 100]);

  return (
    <div
      style={{
        width: `${barWidth}%`,
        height: 4,
        backgroundColor: color,
        borderRadius: 0,
      }}
    />
  );
};

export const DataViz: React.FC<DataVizProps> = ({
  title,
  dataPoints,
  variant = "dark",
}) => {
  const { durationInFrames } = useVideoConfig();

  const textColor =
    variant === "dark"
      ? brand.colors.text.primary
      : brand.colors.text.onLight;
  const mutedColor = brand.colors.text.secondary;
  const accentColor = brand.colors.accent;

  const titleFrames = 60;
  const pointFrames = Math.floor(
    (durationInFrames - titleFrames) / dataPoints.length
  );
  const maxValue = Math.max(...dataPoints.map((d) => d.value));

  return (
    <BrandFrame variant={variant} padding={60}>
      {/* Title */}
      <Sequence from={5} durationInFrames={titleFrames}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            height: "100%",
            gap: brand.spacing.lg,
          }}
        >
          <TextReveal
            text={title}
            mode="word"
            fontSize={brand.typography.scale["3xl"]}
            color={textColor}
            fontStyle="display"
            startFrame={5}
          />
          <DividerLine startFrame={20} color={mutedColor} width="30%" />
        </div>
      </Sequence>

      {/* Data points */}
      {dataPoints.map((dp, i) => {
        const pointStart = titleFrames + i * pointFrames;

        return (
          <Sequence key={i} from={pointStart} durationInFrames={pointFrames}>
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
                {/* Label */}
                <TextReveal
                  text={dp.label}
                  mode="word"
                  fontSize={brand.typography.scale.lg}
                  color={mutedColor}
                  fontStyle="body"
                  startFrame={0}
                />

                {/* Value — big number */}
                <Counter
                  value={dp.value}
                  prefix={dp.prefix}
                  suffix={dp.suffix}
                  startFrame={5}
                  fontSize={brand.typography.scale["5xl"]}
                  color={textColor}
                />

                {/* Bar chart */}
                <BarChart
                  value={dp.value}
                  maxValue={maxValue}
                  startFrame={10}
                  color={accentColor}
                />

                {/* Context */}
                {dp.context && (
                  <TextReveal
                    text={dp.context}
                    mode="word"
                    fontSize={brand.typography.scale.base}
                    color={mutedColor}
                    fontStyle="mono"
                    startFrame={20}
                  />
                )}
              </div>
            </BrandFrame>
          </Sequence>
        );
      })}

      <Sequence from={10}>
        <LowerThird startFrame={0} context="Data" />
      </Sequence>
    </BrandFrame>
  );
};
