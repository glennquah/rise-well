'use client';
import { useEffect, useState } from 'react';
import { AlarmHistoryDto } from '../api/dtos/alarm-history';
import AlarmCharts from './AlarmCharts';
import AlarmTable from './AlarmTable';
import { LoadingSpinner } from './Loadingspinner';

export const AlarmClockHistory = () => {
  const [alarms, setAlarms] = useState<AlarmHistoryDto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAlarms = async () => {
      try {
        const res = await fetch('/api/alarm-history', {
          credentials: 'include',
        });
        const data = await res.json();
        const alarms = data.alarms as AlarmHistoryDto[];
        if (!res.ok) {
          setError(data.message || 'Error fetching alarms');
        } else {
          setAlarms(alarms);
        }
      } catch (err) {
        console.error('Error fetching alarms:', err);
        setError('Error fetching alarms');
      } finally {
        setLoading(false);
      }
    };

    fetchAlarms();
  }, []);

  if (loading)
    return (
      <div className="flex justify-center items-center h-full">
        <LoadingSpinner />
      </div>
    );
  if (error) return <div className="text-red-500 text-center">{error}</div>;
  return (
    <div className="py-4">
      <AlarmTable data={alarms} />
      <AlarmCharts data={alarms} />
    </div>
  );
};
