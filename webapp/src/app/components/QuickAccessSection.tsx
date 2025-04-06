'use client';
import { Button } from '@/components/ui/button';
import { motion } from 'framer-motion';
import { Clock, Moon } from 'lucide-react';
import Link from 'next/link';

export default function QuickAccessSection() {
  return (
    <section className="py-12">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="glass-panel rounded-2xl p-8 soft-shadow"
      >
        <h2 className="text-xl font-semibold text-foreground mb-6">
          Quick Access
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="card-hover bg-white/70 rounded-xl p-6 soft-shadow border border-white/40 transition-all">
            <div className="flex items-start space-x-4">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                <Moon className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-foreground">
                  Sleep Analytics
                </h3>
                <p className="mt-1 text-sm text-foreground/70">
                  Track your sleep patterns, quality, and get detailed insights
                  breakdown
                </p>
                <Link href="/sleep-analytics">
                  <Button
                    variant="ghost"
                    className="mt-3 text-primary hover:text-primary/90 hover:bg-blue-50 px-0"
                  >
                    View Analytics →
                  </Button>
                </Link>
              </div>
            </div>
          </div>

          <div className="card-hover bg-white/70 rounded-xl p-6 soft-shadow border border-white/40 transition-all">
            <div className="flex items-start space-x-4">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                <Clock className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-foreground">
                  Alarm Analytics
                </h3>
                <p className="mt-1 text-sm text-foreground/70">
                  Review your alarm activity and get insights on your wake-up
                  patterns
                </p>
                <Link href="/alarm-clock-analytics">
                  <Button
                    variant="ghost"
                    className="mt-3 text-primary hover:text-primary/90 hover:bg-blue-50 px-0"
                  >
                    View Analytics →
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  );
}
