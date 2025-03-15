import { z } from 'zod';

const DateString = z.preprocess((arg) => {
  if (typeof arg === 'string' || arg instanceof Date) {
    return new Date(arg);
  }
}, z.date());

const BaseAlarmHistorySchema = z.object({
  userId: z.string(),
  alarmType: z.enum(['speech', 'math', 'shake']),
  alarmTime: DateString,
  resolvedTime: DateString,
});

const SpeechHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('speech'),
  difficulty: z.enum(['easy', 'medium', 'hard']),
  numberOfWords: z.number(),
  givenWords: z.string(),
});

const MathHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('math'),
});

const ShakeHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('shake'),
});

export const AlarmHistorySchema = z.discriminatedUnion('alarmType', [
  SpeechHistorySchema,
  MathHistorySchema,
  ShakeHistorySchema,
]);

export type AlarmHistoryDto = z.infer<typeof AlarmHistorySchema>;
