import { z } from 'zod';

export const AlarmReportSchema = z.object({
  overview: z.string(),
  frequentPatterns: z.string(),
  wakeUpRegularity: z.string(),
  retriggerAnalysis: z.string(),
  suggestions: z.array(z.string()),
});

export type AlarmReportDto = z.infer<typeof AlarmReportSchema>;
