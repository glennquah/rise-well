import { z } from 'zod';

export const SpeechFeatureSchema = z.object({
  difficulty: z.enum(['easy', 'medium', 'hard']),
  words: z.number(),
});

export type SpeechFeatureDto = z.infer<typeof SpeechFeatureSchema>;
