import { getCollection } from "../../lib/mongodb";
import { auth } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

export async function GET() {
  const { userId } = await auth(); // Check authentication

  if (!userId) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const heartrateCollection = await getCollection("alarm-history");
  const heartRates = await heartrateCollection.find({}).toArray();

  const filteredHeartRates = heartRates
  .filter((item) => item.heartrate !== undefined && item.heartrate !== null)
  .map((item) => ({
    _id: item._id.toString(),
    timestamp: item.timestamp,
    heartrate: item.heartrate,
  }));

  // const plainHeartRates = heartRates.map((item) => ({
  //   _id: item._id.toString(),
  //   timestamp: item.timestamp,
  //   heartrate: item.heartrate,
  // }));

  return new Response(JSON.stringify(filteredHeartRates), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}
