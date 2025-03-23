import { z } from 'zod';

const DateString = z.preprocess((arg) => {
  if (typeof arg === 'string' || arg instanceof Date) {
    return new Date(arg);
  }
}, z.date());

const BaseAlarmHistorySchema = z.object({
  userId: z.string(),
  alarmType: z.enum(['speech', 'math', 'shake', 'image', 'nothing']),
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
  difficulty: z.enum(['easy', 'medium', 'hard']),
  mathOperations: z.enum([
    'Addition',
    'Subtraction',
    'Multiplication',
    'Division',
  ]),
  numberOfQuestions: z.number(),
});

const ShakeHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('shake'),
});

const ImageHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('image'),
  taskType: z.enum(['preset', 'prompt']),
  imageUrl: z.string().optional(),
  promptType: z.string().optional(),
  prompt: z.string().optional(),
});

const NothingHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('nothing'),
});

export const AlarmHistorySchema = z.discriminatedUnion('alarmType', [
  SpeechHistorySchema,
  MathHistorySchema,
  ShakeHistorySchema,
  ImageHistorySchema,
  NothingHistorySchema,
]);

export type AlarmHistoryDto = z.infer<typeof AlarmHistorySchema>;
