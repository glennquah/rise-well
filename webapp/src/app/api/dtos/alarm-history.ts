import { z } from 'zod';

const DateString = z.preprocess((arg) => {
  if (typeof arg === 'string' || arg instanceof Date) {
    return new Date(arg);
  }
}, z.date());

const BaseAlarmHistorySchema = z.object({
  _id: z.string(),
  userId: z.string(),
  alarmType: z.enum([
    'Speech',
    'Math',
    'Shake It',
    'Image Recognition',
    'Nothing',
  ]),
  alarmTime: DateString,
  resolvedTime: DateString,
});

const SpeechHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('Speech'),
  difficulty: z.enum(['Easy', 'Medium', 'Hard']),
  numberOfWords: z.number(),
  givenWords: z.string(),
  attempts: z.number().optional(),
});

const MathHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('Math'),
  difficulty: z.enum(['Easy', 'Medium', 'Hard']),
  mathOperations: z.enum([
    'Addition',
    'Subtraction',
    'Multiplication',
    'Division',
  ]),
  numberOfQuestions: z.number(),
  attempts: z.number().optional(),
});

const ShakeHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('Shake It'),
  difficulty: z.enum(['Easy', 'Medium', 'Hard']),
  shakeCount: z.number(),
});

const ImageHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('Image Recognition'),
  mode: z.enum(['reference', 'category']),
  imageUrl: z.string().optional(),
  refImageUrl: z.string().optional(),
  target_object: z.string().optional(),
  category: z.string().optional(),
});

const NothingHistorySchema = BaseAlarmHistorySchema.extend({
  alarmType: z.literal('Nothing'),
});

export const AlarmHistorySchema = z.discriminatedUnion('alarmType', [
  SpeechHistorySchema,
  MathHistorySchema,
  ShakeHistorySchema,
  ImageHistorySchema,
  NothingHistorySchema,
]);

export type AlarmHistoryDto = z.infer<typeof AlarmHistorySchema>;
