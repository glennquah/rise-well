import { ObjectId } from 'mongodb';
import { NextRequest, NextResponse } from 'next/server';
import { getCollection } from '../../../lib/mongodb';

const COLLECTION_NAME = 'alarm-history';

const getRandom = <T>(arr: T[]): T =>
  arr[Math.floor(Math.random() * arr.length)];

const generateAlarm = (
  date: Date,
  hour: number,
  userId: string,
  alarmType: string,
) => {
  const rerings = Math.floor(Math.random() * 4) + 1;
  const baseTime = new Date(date);
  baseTime.setHours(hour, 0, 0, 0);

  const alarms = [];

  for (let i = 0; i < rerings; i++) {
    const alarmTime = new Date(baseTime.getTime() + i * 60_000);
    const resolvedTime = new Date(
      alarmTime.getTime() + Math.random() * 4 * 60_000 + 60_000,
    );

    const common = {
      _id: new ObjectId(),
      userId,
      alarmTime,
      resolvedTime,
      alarmType,
    };

    switch (alarmType) {
      case 'Speech':
        alarms.push({
          ...common,
          difficulty: getRandom(['Easy', 'Medium', 'Hard']),
          numberOfWords: Math.floor(Math.random() * 3) + 3,
          givenWords: 'apple banana orange',
          attempts: Math.floor(Math.random() * 2) + 1,
        });
        break;
      case 'Math':
        alarms.push({
          ...common,
          difficulty: getRandom(['Easy', 'Medium', 'Hard']),
          mathOperations: getRandom([
            'Addition',
            'Subtraction',
            'Multiplication',
            'Division',
          ]),
          numberOfQuestions: Math.floor(Math.random() * 3) + 3,
          attempts: Math.floor(Math.random() * 2) + 1,
        });
        break;
      case 'Shake It':
        alarms.push({
          ...common,
          difficulty: getRandom(['Easy', 'Medium', 'Hard']),
          shakeCount: Math.floor(Math.random() * 30) + 10,
        });
        break;
      case 'Image Recognition':
        alarms.push({
          ...common,
          mode: getRandom(['reference', 'category']),
          imageUrl: 'https://example.com/image.jpg',
          refImageUrl: 'https://example.com/ref.jpg',
          target_object: 'cat',
          category: 'animal',
        });
        break;
      case 'Nothing':
        alarms.push({ ...common });
        break;
    }
  }

  return alarms;
};

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const userId = body.userId;

    if (!userId || typeof userId !== 'string') {
      return NextResponse.json(
        { message: 'Missing or invalid userId' },
        { status: 400 },
      );
    }

    const collection = await getCollection(COLLECTION_NAME);
    const now = new Date();
    const allAlarms = [];

    for (let i = 0; i < 10; i++) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);

      // To simulate a late wake-up time, (2pm)
      const isLateWake = i === Math.floor(Math.random() * 10);
      const hour = isLateWake ? 14 : getRandom([8, 9, 10]);
      const alarmType = getRandom([
        'Speech',
        'Math',
        'Shake It',
        'Image Recognition',
        'Nothing',
      ]);

      allAlarms.push(...generateAlarm(date, hour, userId, alarmType));
    }

    await collection.insertMany(allAlarms);

    return NextResponse.json({
      message: 'Seeded alarm history',
      count: allAlarms.length,
      userId,
    });
  } catch (err) {
    console.error('Seeding error:', err);
    return NextResponse.json({ message: 'Seeding failed' }, { status: 500 });
  }
}
