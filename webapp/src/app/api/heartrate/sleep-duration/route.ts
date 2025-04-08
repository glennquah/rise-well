import { auth } from '@clerk/nextjs/server';
import { differenceInMinutes } from 'date-fns';
import { NextResponse } from 'next/server';
import { getCollection } from '../../../lib/mongodb';

const COLLECTION_NAME = 'heartrate';

export async function GET() {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  try {
    const collection = await getCollection(COLLECTION_NAME);

    // Get the most recent alarm entry for the user
    const [latestEntry] = await collection
      .find({ userId, heartrate: { $exists: true } })
      .sort({ alarmTime: -1 })
      .limit(1)
      .toArray();

    if (!latestEntry) {
      return NextResponse.json({ message: 'No alarms found' }, { status: 404 });
    }

    const alarmDate = new Date(latestEntry.alarmTime);
    const startOfDay = new Date(alarmDate);
    startOfDay.setUTCHours(0, 0, 0, 0);
    const endOfDay = new Date(alarmDate);
    endOfDay.setUTCHours(23, 59, 59, 999);

    // Fetch all alarms for the same day
    const sameDayAlarms = await collection
      .find({
        userId,
        heartrate: { $exists: true },
        alarmTime: {
          $gte: startOfDay,
          $lte: endOfDay,
        },
      })
      .toArray();

    if (!sameDayAlarms.length) {
      return NextResponse.json(
        { message: 'No alarms on that date' },
        { status: 404 },
      );
    }

    const first = sameDayAlarms.reduce(
      (min, r) => (r.timestamp < min.timestamp ? r : min),
      sameDayAlarms[0],
    );
    const last = sameDayAlarms.reduce(
      (max, r) => (r.timestamp > max.timestamp ? r : max),
      sameDayAlarms[0],
    );

    const firstTime = new Date(first.timestamp * 1000);
    const lastTime = new Date(last.timestamp * 1000);

    const mins = differenceInMinutes(lastTime, firstTime);
    const hours = Math.floor(mins / 60);
    const minutes = mins % 60;

    const sleepDuration = `${hours.toString().padStart(2, '0')}:${minutes
      .toString()
      .padStart(2, '0')}`;

    return NextResponse.json({ sleepDuration });
  } catch (error) {
    console.error('Error getting sleep duration:', error);
    return NextResponse.json(
      { message: 'Internal Server Error' },
      { status: 500 },
    );
  }
}
