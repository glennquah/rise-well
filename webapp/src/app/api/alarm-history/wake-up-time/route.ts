import { auth } from '@clerk/nextjs/server';
import { format } from 'date-fns';
import { NextResponse } from 'next/server';
import { getCollection } from '../../../lib/mongodb';

const COLLECTION_NAME = 'alarm-history';

export async function WAKE_UP_TIME() {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  try {
    const collection = await getCollection(COLLECTION_NAME);
    const alarms = await collection
      .find({ userId })
      .sort({ alarmTime: 1 })
      .limit(1)
      .toArray();

    if (!alarms.length) {
      return NextResponse.json({ message: 'No alarms found' }, { status: 404 });
    }

    const resolved = alarms[0].resolvedTime;
    const resolvedFormatted = format(new Date(resolved), 'HH:mm');

    return NextResponse.json({ wakeUpTime: resolvedFormatted });
  } catch (error) {
    console.error('Error getting earliest resolved time:', error);
    return NextResponse.json(
      { message: 'Internal Server Error' },
      { status: 500 },
    );
  }
}
