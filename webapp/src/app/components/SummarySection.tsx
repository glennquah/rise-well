'use client';
import { motion } from 'framer-motion';
import { BarChart2, Clock, Moon } from 'lucide-react';
import { useEffect, useState } from 'react';
import CardStats from './CardStats';

export default function SummarySection() {
  const [wakeUpTime, setWakeUpTime] = useState<string | null>(null);
  const [timeToWakeup, setTimeToWakeup] = useState<string | null>(null);
  const [sleepDuration, setSleepDuration] = useState<string | null>(null);

  useEffect(() => {
    const fetchWakeUpData = async () => {
      try {
        const wakeRes = await fetch('/api/alarm-history/wake-up-time', {
          credentials: 'include',
        });
        const wakeData = await wakeRes.json();
        setWakeUpTime(wakeData.wakeUpTime);

        const wakeupTimeRes = await fetch('/api/alarm-history/time-to-wakeup', {
          credentials: 'include',
        });
        const wakeupTimeData = await wakeupTimeRes.json();
        setTimeToWakeup(wakeupTimeData.timeToWake);

        //sleep duration
        const sleepDurationRes = await fetch(
          '/api/heartrate/sleep-duration',
          {
            credentials: 'include',
          },
        );
        const sleepDurationData = await sleepDurationRes.json();
        setSleepDuration(sleepDurationData.sleepDuration);

      } catch (error) {
        console.error('Error fetching summary data:', error);
      }
    };

    fetchWakeUpData();
  }, []);

  const formatTimeToWake = (time: string | null) => {
    if (!time) return 'N/A';
    const [hrs, mins] = time.split(':').map(Number);
    const parts = [];
    if (hrs > 0) parts.push(`${hrs}h`);
    if (mins > 0) parts.push(`${mins}m`);
    return parts.join(' ') || '0m';
  };

  return (
    <section className="py-8">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <h2 className="section-title">Today's Summary</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 py-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.3 }}
          >
            <CardStats
              title="Wake-up Time"
              value={wakeUpTime ?? 'Loading...'}
              icon={<Clock className="h-5 w-5" />}
            />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <CardStats
              title="Time Taken to Wakeup"
              value={formatTimeToWake(timeToWakeup)}
              icon={<BarChart2 className="h-5 w-5" />}
            />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.4 }}
          >
            <CardStats
              title="Sleep Duration"
              //value={'8h 30m'} // TODO: Replace with actual API call
              ///value={sleepDuration ?? 'Loading...'}
              value={formatTimeToWake(sleepDuration)}
              icon={<Moon className="h-5 w-5" />}
            />
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
}
