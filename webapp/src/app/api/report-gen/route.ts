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
      "overview": "<Provide a concise summary of how the user generally interacts with their alarms. Include details such as the types of alarms frequently set (**Speech**, **Math**, **Shake It**, **Image Recognition**, **Nothing**) and overall effectiveness.>",
      
      "frequentPatterns": "<Highlight clear patterns, such as which alarm types (**Speech**, **Math**, **Shake It**, **Image Recognition**, **Nothing**) and difficulty levels are most commonly used. Identify if the user favors certain tasks consistently.>",
      
      "wakeUpRegularity": "<Evaluate and comment clearly if the user tends to wake up at consistent times or if their waking times vary significantly. Include specific references to the data provided.>",
      
      "retriggerAnalysis": "<Carefully analyze if multiple alarms are triggered closely together (within short intervals, e.g., under 15 minutes). Explicitly indicate if this shows repeated snoozing or the re-triggering of alarms (**Speech**, **Math**, **Shake It**, **Image Recognition**, **Nothing**).>",
      
      "suggestions": [
        "<Provide specific, actionable advice based on your analysis. Clearly suggest improvements such as setting harder challenges (**Speech** or **Math**), using louder alarms, repositioning devices to avoid retriggers, adjusting bedtime, or if necessary, recommend seeking professional sleep guidance.>"
      ]
    }

    IMPORTANT FORMATTING RULES:
    - Whenever mentioning alarm types: "**Speech**", "**Math**", "**Shake It**", "**Image Recognition**", or "**Nothing**", strictly use Markdown bold formatting as demonstrated.
    - Keep language professional, concise, and suitable for direct storage in a database or user-facing display.

    User's Alarm History Data:
    ${JSON.stringify(history, null, 2)}
  `.trim();

  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4-1106-preview',
      messages: [{ role: 'system', content: systemPrompt }],
      temperature: 0.7,
      response_format: { type: 'json_object' },
    });

    const content = completion.choices[0].message.content;
    const reportParsed = AlarmReportSchema.safeParse(JSON.parse(content || ''));

    if (!reportParsed.success) {
      console.error('Parsing error:', reportParsed.error.flatten());
      return NextResponse.json(
        { message: 'Parsing error', errors: reportParsed.error.flatten() },
        { status: 500 },
      );
    }

    console.log('Report generated successfully:', reportParsed.data);
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
