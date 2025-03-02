import { NextResponse } from "next/server";
import { getCollection } from "../../lib/mongodb";

// EXAMPLE OF HOW NEXTJS API ROUTES WORKS, ofc we should rename data, just putting here as reference
const COLLECTION_NAME = "data";

export async function GET() {
  try {
    const collection = await getCollection(COLLECTION_NAME);
    const data = await collection.find({}).toArray();
    return NextResponse.json({ data });
  } catch (error) {
    console.error("Error fetching data:", error);
    return NextResponse.json({ message: "Internal Server Error" }, { status: 500 });
  }
}

export async function POST(req: Request) {
  try {
    const { name, email } = await req.json();

    const collection = await getCollection(COLLECTION_NAME);
    const result = await collection.insertOne({ name, email });

    return NextResponse.json({ message: "Data inserted", id: result.insertedId });
  } catch (error) {
    console.error("Error inserting data:", error);
    return NextResponse.json({ message: "Internal Server Error" }, { status: 500 });
  }
}