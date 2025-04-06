'use client';

import { ChartLine } from '@/components/chart-line';
import { SectionCards } from '@/components/section-cards';
import { useState } from 'react';
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function PollingDataDisplay() {
  const { data, error } = useSWR('/api/heartrate', fetcher, {
    refreshInterval: 5000,
  });

  const [selectedDate, setSelectedDate] = useState(() => {
    return new Date().toISOString().split('T')[0]; // "YYYY-MM-DD"
  });

  if (error) return <div>Error loading data.</div>;
  if (!data) return <div>Loading...</div>;

  const filteredData = selectedDate
    ? // eslint-disable-next-line @typescript-eslint/no-explicit-any
      data.filter((item: any) => {
        const itemDate = new Date(item.timestamp * 1000)
          .toISOString()
          .split('T')[0];
        return itemDate === selectedDate;
      })
    : data;

  return (
    <div className="flex flex-col gap-6">
      <SectionCards data={filteredData} />
      <div>
        <ChartLine
          data={filteredData}
          selectedDate={selectedDate}
          onDateChange={(value) => setSelectedDate(value)}
        />
      </div>
    </div>
  );
}
