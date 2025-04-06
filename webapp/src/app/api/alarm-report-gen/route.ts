import { getCollection } from '@/app/lib/mongodb';
import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';
import OpenAI from 'openai';
import { AlarmHistoryDto } from '../dtos/alarm-history';
import { AlarmReportSchema } from '../dtos/alarm-report';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export async function POST() {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  const history: AlarmHistoryDto[] = await fetchUserAlarms(userId);

  const systemPrompt = `
You are an assistant tasked with generating a comprehensive and structured report based on a user's alarm clock history. 

The alarm history provided includes various types of alarms, each serving different purposes:

- **Speech**: User repeats motivational phrases or challenging words.
- **Math**: User solves arithmetic problems of varying difficulty.
- **Shake It**: User physically shakes their phone to dismiss the alarm.
- **Image Recognition**: User takes a picture of a predetermined object or responds to visual prompts.
- **Nothing**: Simple alarm with no additional tasks.

Analyze the provided alarm history data carefully and strictly generate your report as a JSON object following this exact schema:

{
  "overview": "<Provide a concise summary of how the user interacts with their alarms. Clearly include which alarm types (**Speech**, **Math**, **Shake It**, **Image Recognition**, **Nothing**) they commonly use and their effectiveness at waking the user.>",

  "frequentPatterns": "<Identify clear and notable patterns in the user's alarm behavior. Specify which alarm types (**Speech**, **Math**, **Shake It**, **Image Recognition**, **Nothing**) and difficulty levels appear most frequently.>",

  "wakeUpRegularity": "<Clearly indicate if the user generally wakes up at consistent times or if wake-up times vary significantly. Reference specific time intervals or patterns from the provided data.>",

  "retriggerAnalysis": "<Analyze carefully if multiple alarms were triggered close together (e.g., within 15-minute intervals), clearly identifying if this indicates repeated snoozing or retriggering of alarms (**Speech**, **Math**, **Shake It**, **Image Recognition**, **Nothing**).>",

  "suggestions": [
    "<Provide at least four separate, concise, actionable suggestions to improve the user's wake-up routine. Suggestions should include methods such as setting more challenging tasks (**Speech** or **Math**), using louder or different alarm types (**Shake It**, **Image Recognition**), improving sleep hygiene, positioning devices differently, adjusting bedtime, or seeking professional sleep advice. Each suggestion should be short, actionable, and accompanied by a relevant and helpful link (URL) to a credible external resource.>"
  ]
}

IMPORTANT FORMATTING RULES:
- ALWAYS provide at least FOUR distinct suggestions, each SHORT, ACTIONABLE, and CLEARLY NUMBERED (1, 2, 3, 4, ...).
- Each suggestion must INCLUDE one relevant hyperlink to a credible external source for more information (e.g., sleep foundation, medical advice, or app recommendations).
- Whenever mentioning alarm types: "**Speech**", "**Math**", "**Shake It**", "**Image Recognition**", or "**Nothing**", strictly use Markdown bold formatting.
- Keep language professional, concise, and suitable for direct database storage or user-facing display.
DO NOT wrap the response in triple backticks or any markdown formatting.
Only return a raw JSON object without any additional text or explanation.

User's Alarm History Data:
${JSON.stringify(history, null, 2)}
  `.trim();

  try {
    const stream = await openai.chat.completions.create({
      model: 'gpt-4-1106-preview',
      messages: [{ role: 'system', content: systemPrompt }],
      stream: true,
      temperature: 1,
    });

    let jsonText = '';

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    for await (const chunk of stream as any) {
      const delta = chunk.choices?.[0]?.delta?.content;
      if (delta) {
        jsonText += delta;
      }
    }

    const parsed = JSON.parse(jsonText);
    const reportParsed = AlarmReportSchema.safeParse(parsed);

    if (!reportParsed.success) {
      console.error('Parsing error:', reportParsed.error.flatten());
      return NextResponse.json(
        {
          message: 'Parsing error',
          errors: reportParsed.error.flatten(),
        },
        { status: 500 },
      );
    }

    return NextResponse.json(reportParsed.data);
  } catch (error) {
    console.error('Generation error:', error);
    return NextResponse.json(
      { message: 'Failed to generate report' },
      { status: 500 },
    );
  }
}

async function fetchUserAlarms(userId: string): Promise<AlarmHistoryDto[]> {
  const collection = await getCollection('alarm-history');
  const alarms = await collection
    .find({ userId })
    .project({ _id: 0 })
    .toArray();

  return alarms as AlarmHistoryDto[];
}
