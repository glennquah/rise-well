'use client';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ChartConfig, ChartContainer } from '@/components/ui/chart';
import { CartesianGrid, Line, LineChart, Tooltip, XAxis } from 'recharts';

const chartConfig = {
  desktop: {
    label: 'Desktop',
    color: 'hsl(var(--chart-1))',
  },
} satisfies ChartConfig;

interface ChartLineProps {
  data: {
    _id: string;
    timestamp: number;
    heartrate: number;
  }[];
  selectedDate: string | null;
  onDateChange: (value: string) => void;
}

export function ChartLine({
  data,
  selectedDate,
  onDateChange,
}: ChartLineProps) {
  const chartData = data.map((item) => ({
    timestamp: new Date(item.timestamp * 1000).toLocaleTimeString('en-GB', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }),
    fullTimestamp: new Date(item.timestamp * 1000).toLocaleString('en-GB', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    }),
    heartrate: Math.round(item.heartrate),
  }));

  const minDate = new Date(
    Math.min(...data.map((item) => item.timestamp * 1000)),
  ).toLocaleDateString('en-GB', { month: 'long', year: 'numeric' });
  const maxDate = new Date(
    Math.max(...data.map((item) => item.timestamp * 1000)),
  ).toLocaleDateString('en-GB', { month: 'long', year: 'numeric' });

  return (
    <div className="glass-panel rounded-2xl soft-shadow overflow-hidden w-full">
      <Card className="border-0 shadow-none bg-transparent">
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              {data.length === 0 ? null : (
                <div>
                  <CardTitle>Heart Rate Variability</CardTitle>
                </div>
              )}
            </div>
            <input
              type="date"
              value={selectedDate ?? ''}
              onChange={(e) => onDateChange(e.target.value)}
              className="border px-3 py-2 rounded-md shadow-sm"
            />
          </div>
        </CardHeader>
        <CardContent>
          {data.length === 0 ? (
            <div className="text-center text-gray-500 py-12 mb-12">
              <p className="text-lg font-medium">
                No heart rate data for this date.
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Try selecting a different day.
              </p>
            </div>
          ) : (
            <ChartContainer
              config={chartConfig}
              className="aspect-auto h-[250px] w-full"
            >
              <LineChart
                accessibilityLayer
                data={chartData}
                margin={{ left: 12, right: 12 }}
              >
                <CartesianGrid vertical={false} />
                <XAxis
                  dataKey="timestamp"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  interval="preserveStartEnd"
                  tickFormatter={(value, index) =>
                    index % 4 === 0 ? value : ''
                  }
                />

                <Tooltip
                  content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                      return (
                        <div className="bg-white shadow-md rounded-lg px-4 py-3 text-gray-800 border border-gray-200">
                          <p className="text-sm text-gray-500">
                            {payload[0].payload.fullTimestamp}
                          </p>
                          <p className="text-sm text-gray-500 mt-1">
                            Heart Rate:{' '}
                            <span className=" text-gray-500">
                              {payload[0].value} BPM
                            </span>
                          </p>
                        </div>
                      );
                    }
                    return null;
                  }}
                />
                <Line
                  dataKey="heartrate"
                  type="natural"
                  stroke="#2463EB"
                  strokeWidth={2}
                  dot={true}
                />
              </LineChart>
            </ChartContainer>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
