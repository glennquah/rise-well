import { z } from 'zod';

export const AlarmSchema = z.object({
  userId: z.string(),
  alarmType: z.enum(['speech', 'math', 'shake']),
  time: z.string(),
});

export type AlarmDto = z.infer<typeof AlarmSchema>;
