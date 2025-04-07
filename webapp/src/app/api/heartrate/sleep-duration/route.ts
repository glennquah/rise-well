import { auth } from '@clerk/nextjs/server';
import { differenceInMinutes, format } from 'date-fns';
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

    // Find the most recent alarm for the user (i.e., latest day)
    const latestDateDoc = await collection
      .find({ userId })
      .sort({ alarmTime: -1 }) // <-- change from 1 to -1 for descending
      .limit(1)
      .toArray();

    if (!latestDateDoc.length) {
      return NextResponse.json({ message: 'No alarms found' }, { status: 404 });
    }


    // const sameDayAlarms = await collection
    //   .find({
    //     userId,
    //     alarmTime: {
    //       $gte: new Date(`${dateKey}T00:00:00.000Z`),
    //       $lte: new Date(`${dateKey}T23:59:59.999Z`),
    //     },
    //   })
    //   .toArray();

    const sameDayAlarms = await collection
      .find({
        userId,
        heartrate: { $exists: true },
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


    // const mins = differenceInMinutes(
    //   new Date(last.resolvedTime),
    //   new Date(first.alarmTime),
    // );

    const hours = Math.floor(mins / 60);
    const minutes = mins % 60;

    const sleepDuration = `${hours.toString().padStart(2, '0')}:${minutes
      .toString()
      .padStart(2, '0')}`;

    return NextResponse.json({
      sleepDuration,
    });
  } catch (error) {
    console.error('Error getting sleep duration:', error);
    return NextResponse.json(
      { message: 'Internal Server Error' },
      { status: 500 },
    );
  }
}
