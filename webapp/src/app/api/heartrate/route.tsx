import { getCollection } from "../../lib/mongodb";

export async function GET() {
  const heartrateCollection = await getCollection("heartrate");
  const heartRates = await heartrateCollection.find({}).toArray();
  const plainHeartRates = heartRates.map((item) => ({
    _id: item._id.toString(),
    timestamp: item.timestamp,
    heartrate: item.heartrate,
  }));
  
  return new Response(JSON.stringify(plainHeartRates), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}
