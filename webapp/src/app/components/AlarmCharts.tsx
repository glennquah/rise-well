'use client';

import { differenceInMinutes, format } from 'date-fns';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { AlarmHistoryDto } from '../api/dtos/alarm-history';

interface AlarmTableProps {
  data: AlarmHistoryDto[];
}

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#8dd1e1'];

const AlarmCharts = ({ data }: AlarmTableProps) => {
  const alarmTypeCounts = data.reduce((acc: Record<string, number>, item) => {
    acc[item.alarmType] = (acc[item.alarmType] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.entries(alarmTypeCounts).map(([type, count]) => ({
    name: type,
    value: count,
  }));

  const groupedByDate = data.reduce(
    (acc: Record<string, AlarmHistoryDto[]>, item) => {
      const dateKey = format(new Date(item.alarmTime), 'yyyy-MM-dd');
      if (!acc[dateKey]) acc[dateKey] = [];
      acc[dateKey].push(item);
      return acc;
    },
    {},
  );

  const barData = Object.entries(groupedByDate).map(([date, records]) => {
    const firstAlarm = records.reduce(
      (min, r) => (new Date(r.alarmTime) < new Date(min.alarmTime) ? r : min),
      records[0],
    );
    const lastResolved = records.reduce(
      (max, r) =>
        new Date(r.resolvedTime) > new Date(max.resolvedTime) ? r : max,
      records[0],
    );

    const duration = differenceInMinutes(
      new Date(lastResolved.resolvedTime),
      new Date(firstAlarm.alarmTime),
    );

    return {
      date,
      minutesToWake: duration,
    };
  });

  return (
    <div className="py-8 grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
      <div className="glass-panel rounded-2xl soft-shadow overflow-hidden w-full">
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-2">Alarm Type Breakdown</h2>
          <p className="text-sm text-muted-foreground mb-4">
            Shows how often each alarm type was triggered.
          </p>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                outerRadius={100}
                label
              >
                {pieData.map((entry, index) => (
                  <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-panel rounded-2xl soft-shadow overflow-hidden w-full">
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-2">
            Time to Wake Up per Day
          </h2>
          <p className="text-sm text-muted-foreground mb-4">
            Duration from the first alarm triggered to the last resolved alarm
            each day.
          </p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                interval={0}
                angle={-45}
                textAnchor="end"
                height={60}
                tickLine={false}
                style={{ fontSize: '12px' }}
              />
              <YAxis
                label={{
                  value: 'Minutes',
                  angle: -90,
                  position: 'insideLeft',
                }}
              />
              <Tooltip />
              <Legend />
              <Bar dataKey="minutesToWake" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AlarmCharts;
