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

  const temperatureMap: Record<string, number> = {
    Easy: 0.4,
    Medium: 0.7,
    Hard: 1.0,
  };

  const systemPrompt = `
    You are an assistant that generates motivational quotes to encourage someone to get out of bed and start the day.
    The user wants exactly ${numberOfWords} words in the quote. The words should reflect a difficulty of "${difficulty}" in terms of pronunciation:
    - "Easy": straightforward, commonly used words that are simple to pronounce.
    - "Medium": moderately challenging words mixed with more common words.
    - "Hard": more complex, possibly tongue-twister-like words that are tricky to say.
    Make it genuinely uplifting and inspiring, and be sure to keep the exact word count at ${numberOfWords}.
    No extra punctuation that breaks word count, and keep it coherent.
  `.trim();

  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: systemPrompt,
        },
      ],
      temperature: temperatureMap[difficulty] ?? 0.7,
    });

    const sentence = completion.choices[0].message.content?.trim();
    

    return NextResponse.json({ sentence });
  } catch (error) {
    console.error('Error generating motivational quote:', error);
    return NextResponse.json(
      { message: 'Failed to generate motivational quote: ', error },
      { status: 500 },
    );
  }
}
