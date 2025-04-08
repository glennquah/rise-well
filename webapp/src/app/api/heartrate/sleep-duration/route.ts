import { auth } from '@clerk/nextjs/server';
import { differenceInMinutes } from 'date-fns';
import { getCollection } from '../../../lib/mongodb';

const COLLECTION_NAME = 'heartrate';

export async function GET() {
  const { userId } = await auth();
  if (!userId) {
    return new Response('Unauthorized', { status: 401 });
  }

  try {
    const collection = await getCollection(COLLECTION_NAME);

    const [latestEntry] = await collection
      .find({ userId, heartrate: { $exists: true } })
      .sort({ alarmTime: -1 })
      .limit(1)
      .toArray();

    if (!latestEntry) {
      return new Response('No alarms found', { status: 404 });
    }

    const alarmDate = new Date(latestEntry.alarmTime);
    const startOfDay = new Date(alarmDate);
    startOfDay.setUTCHours(0, 0, 0, 0);
    const endOfDay = new Date(alarmDate);
    endOfDay.setUTCHours(23, 59, 59, 999);

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
      return new Response('No alarms on that date', { status: 404 });
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

    return new Response(sleepDuration, {
      status: 200,
      headers: { 'Content-Type': 'text/plain' },
    });
  } catch (error) {
    console.error('Error getting sleep duration:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
}
