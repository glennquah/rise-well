import { z } from 'zod';

export const SpeechFeatureSchema = z.object({
  difficulty: z.enum(['Easy', 'Medium', 'Hard']),
  numberOfWords: z.number(),
});

export type SpeechFeatureDto = z.infer<typeof SpeechFeatureSchema>;
