"use client";

import useSWR from "swr";
import { SectionCards } from "@/components/section-cards";
import { ChartLine } from "@/components/chart-line";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

interface PollingDataDisplayProps {
  initialData: any[];
}

export default function PollingDataDisplay({ initialData }: PollingDataDisplayProps) {
  const { data, error } = useSWR("/api/heartrate", fetcher, {
    fallbackData: initialData,
    refreshInterval: 5000,
  });

  if (error) return <div>Error loading data.</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <>
      <SectionCards data={data} />
      <div className="px-4 lg:px-6">
        <ChartLine data={data} />
      </div>
    </>
  );
}
