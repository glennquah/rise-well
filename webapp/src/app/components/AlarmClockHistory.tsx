'use client';
import { Card, CardContent } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { useEffect, useState } from 'react';
import { AlarmHistoryDto } from '../api/dtos/alarm-history';
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

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center">{error}</div>;

  return (
    <div className="py-4">
      <Card>
        <CardContent className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Type</TableHead>
                <TableHead>Alarm Time</TableHead>
                <TableHead>Resolved Time</TableHead>
                <TableHead>Details</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {alarms.map((alarm) => (
                <TableRow key={alarm.alarmTime.toString()}>
                  <TableCell className="w-32">
                    {alarm.alarmType.toUpperCase()}
                  </TableCell>
                  <TableCell className="w-48">
                    {new Date(alarm.alarmTime).toLocaleString('en-US', {
                      dateStyle: 'short',
                      timeStyle: 'short',
                    })}
                  </TableCell>
                  <TableCell className="w-48">
                    {new Date(alarm.resolvedTime).toLocaleString('en-US', {
                      dateStyle: 'short',
                      timeStyle: 'short',
                    })}
                  </TableCell>
                  <TableCell className="w-96">
                    {alarm.alarmType === 'Speech' ? (
                      <details className="group w-full">
                        <summary
                          className="block cursor-pointer text-blue-600 underline w-full m-0"
                          style={{ listStyle: 'none' }}
                        >
                          View Details
                        </summary>
                        <div className="mt-2 space-y-1 transition-all duration-300 ease-in-out opacity-0 group-open:opacity-100">
                          <p>
                            <strong>Difficulty:</strong> {alarm.difficulty}
                          </p>
                          <p>
                            <strong>Number of Words:</strong>{' '}
                            {alarm.numberOfWords}
                          </p>
                          <p className="whitespace-normal">
                            <strong>Given Words:</strong> {alarm.givenWords}
                          </p>
                        </div>
                      </details>
                    ) : alarm.alarmType === 'Math' ? (
                      <details className="group w-full">
                        <summary
                          className="block cursor-pointer text-blue-600 underline w-full m-0"
                          style={{ listStyle: 'none' }}
                        >
                          View Details
                        </summary>
                        <div className="mt-2 space-y-1 transition-all duration-300 ease-in-out opacity-0 group-open:opacity-100">
                          <p>
                            <strong>Difficulty:</strong> {alarm.difficulty}
                          </p>
                          <p>
                            <strong>Math Operation:</strong>{' '}
                            {alarm.mathOperations}
                          </p>
                          <p>
                            <strong>Number of Questions:</strong>{' '}
                            {alarm.numberOfQuestions}
                          </p>
                        </div>
                      </details>
                    ) : (
                      'N/A'
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
};
