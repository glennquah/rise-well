'use client';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { cn } from '@/lib/utils';
import { ChevronDown } from 'lucide-react';
import React, { useState } from 'react';
import { FullAlarmHistoryDto } from '../api/dtos/alarm-history';

const formatTimeDifference = (start: Date, end: Date) => {
  const diff = end.getTime() - start.getTime();
  const seconds = Math.floor(diff / 1000) % 60;
  const minutes = Math.floor(diff / 60000) % 60;
  const hours = Math.floor(diff / 3600000);
  if (hours > 0) return `${hours}h ${minutes}m ${seconds}s`;
  if (minutes > 0) return `${minutes}m ${seconds}s`;
  return `${seconds}s`;
};

const renderAlarmDetailsContent = (alarm: FullAlarmHistoryDto) => {
  switch (alarm.alarmType) {
    case 'Math':
      return (
        <div className="space-y-1">
          <p>
            <strong>Difficulty:</strong> {alarm.difficulty}
          </p>
          <p>
            <strong>Math Operation:</strong> {alarm.mathOperations}
          </p>
          <p>
            <strong>Number of Questions:</strong> {alarm.numberOfQuestions}
          </p>
        </div>
      );
    case 'Speech':
      return (
        <div className="space-y-1">
          <p>
            <strong>Difficulty:</strong> {alarm.difficulty}
          </p>
          <p>
            <strong>Number of Words:</strong> {alarm.numberOfWords}
          </p>
          <p>
            <strong>Given Words:</strong> {alarm.givenWords}
          </p>
        </div>
      );
    case 'Shake It':
      return (
        <div className="space-y-1">
          <p>
            <strong>Difficulty:</strong> {alarm.difficulty}
          </p>
          <p>
            <strong>Shake Count:</strong> {alarm.shakeCount}
          </p>
        </div>
      );

    case 'Image Recognition':
      return (
        <div className="space-y-2">
          <p>
            <strong>Mode:</strong> {alarm.mode}
          </p>

          {alarm.mode === 'category' && (
            <p>
              <strong>Target Object:</strong> {alarm.target_object ?? 'N/A'}
            </p>
          )}

          {alarm.mode === 'reference' && alarm.refImageUrl && (
            <div>
              <p className="mb-1">
                <strong>Reference Image:</strong>
              </p>
              <img
                src={alarm.refImageUrl}
                alt="Reference"
                className="max-w-xs max-h-60 object-contain border rounded shadow"
              />
            </div>
          )}

          {alarm.imageUrl && (
            <div>
              <p className="mb-1">
                <strong>Captured Image:</strong>
              </p>
              <img
                src={alarm.imageUrl}
                alt="Captured"
                className="max-w-xs max-h-60 object-contain border rounded shadow"
              />
            </div>
          )}
        </div>
      );
  }
};

interface AlarmTableProps {
  data: FullAlarmHistoryDto[];
}

const AlarmTable = ({ data }: AlarmTableProps) => {
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const toggleRow = (id: string) => {
    const newExpandedRows = new Set(expandedRows);
    if (newExpandedRows.has(id)) {
      newExpandedRows.delete(id);
    } else {
      newExpandedRows.add(id);
    }
    setExpandedRows(newExpandedRows);
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Math':
        return 'bg-blue-100 text-blue-800';
      case 'Speech':
        return 'bg-purple-100 text-purple-800';
      case 'Shake It':
        return 'bg-green-100 text-green-800';
      case 'Image Recognition':
        return 'bg-amber-100 text-amber-800';
      case 'Nothing':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="glass-panel rounded-2xl soft-shadow w-full">
      <div className="p-6 flex flex-col md:flex-row items-start md:items-center gap-4 border-b border-border/30">
        <div>
          <h2 className="text-xl font-semibold text-foreground">
            Alarm History
          </h2>
          <p className="text-sm text-foreground/60 mt-1">
            Review your alarm activity and generate insights. This data is being
            shown through your IOT alarm clock, where you can set alarms and
            track your sleep patterns and insights through the app. Press on the
            details icon to see more information about the alarm.
          </p>
        </div>
      </div>
      <div className="overflow-x-auto w-full">
        <div className="min-w-[700px]">
          <Table className="table-auto whitespace-nowrap w-full">
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead className="w-[120px]">Date</TableHead>
                <TableHead>Triggered Time</TableHead>
                <TableHead>Deactivated</TableHead>
                <TableHead>Time to Resolve</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Details</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.map((alarm) => {
                const triggered = new Date(alarm.alarmTime);
                const deactivated = new Date(alarm.resolvedTime);
                return (
                  <React.Fragment key={alarm._id}>
                    <TableRow className="hover:bg-blue-50/50 transition-colors">
                      <TableCell className="font-medium">
                        {new Date(triggered).toLocaleDateString('en-SG', {
                          timeZone: 'Asia/Singapore',
                        })}
                      </TableCell>
                      <TableCell>
                        {new Date(triggered).toLocaleTimeString('en-SG', {
                          timeZone: 'Asia/Singapore',
                        })}
                      </TableCell>
                      <TableCell>
                        {new Date(deactivated).toLocaleTimeString('en-SG', {
                          timeZone: 'Asia/Singapore',
                        })}
                      </TableCell>
                      <TableCell>
                        {formatTimeDifference(triggered, deactivated)}
                      </TableCell>
                      <TableCell>
                        <span
                          className={cn(
                            'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                            getTypeColor(alarm.alarmType),
                          )}
                        >
                          {alarm.alarmType}
                        </span>
                      </TableCell>
                      <TableCell className="text-center">
                        <button
                          onClick={() => toggleRow(alarm._id)}
                          className="p-2 focus:outline-none"
                        >
                          <ChevronDown
                            className={`h-4 w-4 transition-transform ${
                              expandedRows.has(alarm._id) ? 'rotate-180' : ''
                            }`}
                          />
                        </button>
                      </TableCell>
                    </TableRow>
                    {expandedRows.has(alarm._id) && (
                      <TableRow className="bg-gray-50">
                        <TableCell colSpan={6} className="p-4">
                          {renderAlarmDetailsContent(alarm)}
                        </TableCell>
                      </TableRow>
                    )}
                  </React.Fragment>
                );
              })}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
};

export default AlarmTable;
