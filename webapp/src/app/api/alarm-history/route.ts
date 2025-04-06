import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';
import { getCollection } from '../../lib/mongodb';
import { AlarmHistorySchema } from '../dtos/alarm-history';

const COLLECTION_NAME = 'alarm-history';

export async function POST(req: Request) {
  try {
    const json = await req.json();
    const parsed = AlarmHistorySchema.safeParse(json);

    if (!parsed.success) {
      return NextResponse.json(
        {
          message: 'Invalid alarm history data',
          errors: parsed.error.flatten(),
        },
        { status: 400 },
      );
    }

    const { ...alarmData } = parsed.data;
    const collection = await getCollection(COLLECTION_NAME);
    const result = await collection.insertOne(alarmData);

    return NextResponse.json(
      { message: 'Alarm history created', id: result.insertedId },
      { status: 201 },
    );
  } catch (error) {
    console.error('Error creating alarm history:', error);
    return NextResponse.json(
      { message: 'Internal Server Error' },
      { status: 500 },
    );
  }
}

export async function GET() {
  // IMPT!! Make sure u add this to protect the route
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  try {
    const collection = await getCollection(COLLECTION_NAME);
    const alarms = await collection.find({ userId }).toArray();
    return NextResponse.json({ alarms });
  } catch (error) {
    console.error('Error fetching alarm history:', error);
    return NextResponse.json(
      { message: 'Internal Server Error' },
      { status: 500 },
    );
  }
}
