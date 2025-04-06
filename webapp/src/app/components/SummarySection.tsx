'use client';
import { motion } from 'framer-motion';
import { BarChart2, Clock, Moon } from 'lucide-react';
import CardStats from './CardStats';

export default function SummarySection() {
  return (
    <section className="py-8">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <h2 className="section-title">Todays Summary</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 py-2">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.3 }}
          >
            <CardStats
              title="Wake-up Time"
              value={'14:44'}
              icon={<Clock className="h-5 w-5" />}
            />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <CardStats
              title="Time Taken to Wakeup"
              value={'8h 30m'}
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
              value={'8h 30m'}
              icon={<Moon className="h-5 w-5" />}
            />
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
}
