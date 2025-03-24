import { getCollection } from '@/app/lib/mongodb';
import { auth } from '@clerk/nextjs/server';
import { NextResponse } from 'next/server';
import { AlarmReportSchema } from '../dtos/alarm-report';

const COLLECTION_NAME = 'alarm-report';

export async function POST(req: Request) {
  const { userId } = await auth();

  if (!userId) {
    return NextResponse.json({ message: 'Unauthorized' }, { status: 401 });
  }

  const json = await req.json();
  const parsed = AlarmReportSchema.safeParse(json);

  if (!parsed.success) {
    return NextResponse.json(
      { message: 'Invalid report format', errors: parsed.error.flatten() },
      { status: 400 },
    );
  }

  const report = parsed.data;

  try {
    const collection = await getCollection(COLLECTION_NAME);

    await collection.insertOne({
      userId,
      ...report,
      createdAt: new Date(),
    });

    return NextResponse.json(
      { message: 'Report saved successfully' },
      { status: 201 },
    );
  } catch (error) {
    console.error('Error saving report:', error);
    return NextResponse.json(
      { message: 'Failed to save report' },
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

    const report = await collection
      .find({ userId })
      .sort({ createdAt: -1 })
      .limit(1)
      .project({ _id: 0, userId: 0 })
      .toArray();

    if (report.length === 0) {
      return NextResponse.json(
        { message: 'No report found for this user' },
        { status: 404 },
      );
    }

    return NextResponse.json(report[0], { status: 200 });
  } catch (error) {
    console.error('Error retrieving report:', error);
    return NextResponse.json(
      { message: 'Failed to retrieve report' },
      { status: 500 },
    );
  }
}
