import { z } from 'zod';

const DateString = z.preprocess((arg) => {
  if (typeof arg === 'string' || arg instanceof Date) {
    return new Date(arg);
  }
}, z.date());

const BaseAlarmHistorySchema = z.object({
  userId: z.string(),
  alarmType: z.enum(['speech', 'math', 'shake', 'image']),
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

const ImageHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('image'),
  taskType: z.enum(['preset', 'prompt']),
  imageUrl: z.string().optional(),
  prompt: z.string().optional(),
});

export const AlarmHistorySchema = z.discriminatedUnion('alarmType', [
  SpeechHistorySchema,
  MathHistorySchema,
  ShakeHistorySchema,
  ImageHistorySchema,
]);

export type AlarmHistoryDto = z.infer<typeof AlarmHistorySchema>;
