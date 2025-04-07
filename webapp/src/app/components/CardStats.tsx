import { cn } from '@/lib/utils';
import React from 'react';

interface CardStatProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  description?: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  className?: string;
}

const CardStats = ({
  title,
  value,
  icon,
  description,
  trend,
  className,
}: CardStatProps) => {
  return (
    <div
      className={cn(
        'glass-panel bg-white rounded-2xl p-6 soft-shadow card-hover',
        className,
      )}
    >
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-foreground/60">{title}</p>
          <h3 className="mt-2 text-2xl font-semibold text-foreground">
            {value}
          </h3>

          {trend && (
            <div className="flex items-center mt-2">
              <span
                className={cn(
                  'text-xs font-medium mr-1',
                  trend.isPositive ? 'text-emerald-500' : 'text-rose-500',
                )}
              >
                {trend.isPositive ? '+' : '-'}
                {Math.abs(trend.value)}%
              </span>
              <span className="text-xs text-foreground/60">vs last week</span>
            </div>
          )}

          {description && (
            <p className="mt-2 text-sm text-foreground/60">{description}</p>
          )}
        </div>

        {icon && (
          <div className="p-2 rounded-full bg-primary/10 text-primary">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
};

export default CardStats;
