import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';
import { getCollection } from '../../lib/mongodb';
import { AlarmSchema } from '../models/alarm';

const COLLECTION_NAME = 'alarm';

export async function POST(req: Request) {
  // IMPT!! Make sure u add this to protect the route
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  try {
    const json = await req.json();
    const parsed = AlarmSchema.safeParse(json);

    if (!parsed.success) {
      return NextResponse.json(
        { message: 'Invalid alarm data', errors: parsed.error.flatten() },
        { status: 400 },
      );
    }

    const { alarmType, time } = parsed.data;
    const collection = await getCollection(COLLECTION_NAME);
    const result = await collection.insertOne({ userId, alarmType, time });

    return NextResponse.json(
      { message: 'Alarm created', id: result.insertedId },
      { status: 201 },
    );
  } catch (error) {
    console.error('Error creating alarm:', error);
    return NextResponse.json(
      { message: 'Internal Server Error' },
      { status: 500 },
    );
  }
}

export async function GET() {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  try {
    const collection = await getCollection(COLLECTION_NAME);
    const alarms = await collection.find({ userId }).toArray();
    return NextResponse.json({ alarms });
  } catch (error) {
    console.error('Error fetching alarms:', error);
    return NextResponse.json(
      { message: 'Internal Server Error' },
      { status: 500 },
    );
  }
}
