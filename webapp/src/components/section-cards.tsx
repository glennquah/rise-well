import { BarChart, Flame, HeartPulse, Snowflake } from 'lucide-react';

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
    ? Math.round(
        heartRates.reduce((sum, hr) => sum + hr, 0) / heartRates.length,
      )
    : NaN;

  const minBPM = heartRates.length ? Math.round(Math.min(...heartRates)) : NaN;
  const maxBPM = heartRates.length ? Math.round(Math.max(...heartRates)) : NaN;

  const mean = heartRates.length
    ? heartRates.reduce((sum, hr) => sum + hr, 0) / heartRates.length
    : NaN;

  const variance = heartRates.length
    ? heartRates.reduce((sum, hr) => sum + Math.pow(hr - mean, 2), 0) /
      heartRates.length
    : NaN;

  const stdDeviation = heartRates.length
    ? Math.round(Math.sqrt(variance))
    : NaN;

  const stats = [
    {
      label: 'Average BPM',
      value: averageBPM,
      icon: <HeartPulse className="w-6 h-6 text-gray-500" />,
    },
    {
      label: 'Maximum BPM',
      value: maxBPM,
      icon: <Flame className="w-6 h-6 text-gray-500" />,
    },
    {
      label: 'Minimum BPM',
      value: minBPM,
      icon: <Snowflake className="w-6 h-6 text-gray-500" />,
    },
    {
      label: 'Standard Deviation',
      value: stdDeviation,
      icon: <BarChart className="w-6 h-6 text-gray-500" />,
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-4 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="glass-panel rounded-2xl soft-shadow overflow-hidden w-full"
        >
          <div className="p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-muted-foreground text-sm">
                {stat.label}
              </span>
              {stat.icon}
            </div>
            <div className="py-4 h-full w-full flex justify-center items-center text-4xl font-semibold">
              {isNaN(stat.value) ? 'N/A' : stat.value}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
