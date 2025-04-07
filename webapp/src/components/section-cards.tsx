import { BarChart, Flame, HeartPulse, Snowflake } from 'lucide-react';

interface SectionCardsProps {
  data: {
    _id: string;
    timestamp: number; // should be in milliseconds
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

  // Calculate deep sleep hours
  const sortedData = [...data]
    .filter((item) => !isNaN(Number(item.heartrate)))
    .sort((a, b) => a.timestamp - b.timestamp);

  const DEEP_SLEEP_THRESHOLD = 60; // heart rate below this means "deep sleep"
  const MIN_DEEP_SLEEP_DURATION = 5 * 60 * 1000; // 5 minutes in ms

  let deepSleepMinutes = 0;
  let inDeepSleep = false;
  let startTimestamp = 0;

  for (let i = 0; i < sortedData.length; i++) {
    const { heartrate, timestamp } = sortedData[i];
    const hr = Number(heartrate);

    if (hr < DEEP_SLEEP_THRESHOLD) {
      if (!inDeepSleep) {
        inDeepSleep = true;
        startTimestamp = timestamp;
      }
    } else if (inDeepSleep) {
      const duration = timestamp - startTimestamp;
      if (duration >= MIN_DEEP_SLEEP_DURATION) {
        deepSleepMinutes += duration / 1000 / 60;
      }
      inDeepSleep = false;
    }
  }

  // Handle case where we ended still in deep sleep
  if (inDeepSleep && sortedData.length > 0) {
    const duration =
      sortedData[sortedData.length - 1].timestamp - startTimestamp;
    if (duration >= MIN_DEEP_SLEEP_DURATION) {
      deepSleepMinutes += duration / 1000 / 60;
    }
  }

  const deepSleepHours = heartRates.length ? deepSleepMinutes / 60 : NaN;

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
      label: 'Hours in Deep Sleep',
      value: !isNaN(deepSleepHours)
        ? Math.round(deepSleepHours * 10) / 10
        : NaN,
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
