import { NextResponse } from 'next/server';
import OpenAI from 'openai';
import { SpeechFeatureDto, SpeechFeatureSchema } from '../dtos/speech-feature';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function POST(req: Request) {
  const json = await req.json();
  const parsed = SpeechFeatureSchema.safeParse(json);

  if (!parsed.success) {
    return NextResponse.json(
      { message: 'Invalid input parameters.', errors: parsed.error.flatten() },
      { status: 400 },
    );
  }

  const { difficulty, numberOfWords }: SpeechFeatureDto = parsed.data;

  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: `Generate a tongue twister sentence containing exactly ${numberOfWords} words, suitable for ${difficulty} difficulty.`,
        },
      ],
      temperature:
        difficulty === 'easy' ? 0.3 : difficulty === 'medium' ? 0.6 : 0.9,
    });

    const sentence = completion.choices[0].message.content?.trim();

    return NextResponse.json({ sentence });
  } catch (error) {
    console.error('Error generating tongue twisters:', error);
    return NextResponse.json(
      { message: 'Failed to generate tongue twisters' },
      { status: 500 },
    );
  }
}
