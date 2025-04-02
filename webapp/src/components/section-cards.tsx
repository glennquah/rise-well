import {
  Card,
  CardAction,
  CardDescription,
  CardHeader,
} from "@/components/ui/card";
import { BarChart, Flame, HeartPulse, Snowflake } from "lucide-react";

interface SectionCardsProps {
  data: {
    _id: string;
    timestamp: number;
    heartrate: number;
  }[];
}

export function SectionCards({ data }: SectionCardsProps) {
  const heartRates = (data || [])
    .map((item) => Number(item.heartrate))
    .filter((hr) => !isNaN(hr));

  const averageBPM = heartRates.length
    ? Math.round(heartRates.reduce((sum, hr) => sum + hr, 0) / heartRates.length)
    : NaN;

  const minBPM = heartRates.length ? Math.round(Math.min(...heartRates)) : NaN;
  const maxBPM = heartRates.length ? Math.round(Math.max(...heartRates)) : NaN;

  const mean = heartRates.length
    ? heartRates.reduce((sum, hr) => sum + hr, 0) / heartRates.length
    : NaN;

  const variance = heartRates.length
    ? heartRates.reduce((sum, hr) => sum + Math.pow(hr - mean, 2), 0) / heartRates.length
    : NaN;

  const stdDeviation = heartRates.length ? Math.round(Math.sqrt(variance)) : NaN;

  return (
    <div className="grid grid-cols-1 gap-4 px-4 lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
      {/* Average BPM */}
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Average BPM</CardDescription>
          <CardAction>
            <HeartPulse className="w-6 h-6 text-gray-500" />
          </CardAction>
        </CardHeader>
        <div className="mb-4 h-full w-full flex justify-center items-center text-4xl font-semibold">
          {isNaN(averageBPM) ? "N/A" : averageBPM}
        </div>
      </Card>

      {/* Maximum BPM */}
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Maximum BPM</CardDescription>
          <CardAction>
            <Flame className="w-6 h-6 text-gray-500" />
          </CardAction>
        </CardHeader>
        <div className="mb-4 h-full w-full flex justify-center items-center text-4xl font-semibold">
          {isNaN(maxBPM) ? "N/A" : maxBPM}
        </div>
      </Card>

      {/* Minimum BPM */}
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Minimum BPM</CardDescription>
          <CardAction>
            <Snowflake className="w-6 h-6 text-gray-500" />
          </CardAction>
        </CardHeader>
        <div className="mb-4 h-full w-full flex justify-center items-center text-4xl font-semibold">
          {isNaN(minBPM) ? "N/A" : minBPM}
        </div>
      </Card>

      {/* Standard Deviation BPM */}
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Standard Deviation</CardDescription>
          <CardAction>
            <BarChart className="w-6 h-6 text-gray-500" />
          </CardAction>
        </CardHeader>
        <div className="mb-4 h-full w-full flex justify-center items-center text-4xl font-semibold">
          {isNaN(stdDeviation) ? "N/A" : stdDeviation}
        </div>
      </Card>
    </div>
  );
}
