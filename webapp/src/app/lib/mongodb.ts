// FIXME: Fix this, anot eslint friendly
/* eslint-disable @typescript-eslint/no-explicit-any */
import { Collection, Db, MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI as string;
if (!uri) throw new Error("Missing MONGODB_URI environment variable");

const options = {};

let client: MongoClient;
let clientPromise: Promise<MongoClient>;

if (!("mongoClientPromise" in globalThis)) {
  client = new MongoClient(uri, options);
  (globalThis as any)._mongoClientPromise = client.connect();
}

// eslint-disable-next-line prefer-const
clientPromise = (globalThis as any)._mongoClientPromise;

export async function getDatabase(): Promise<Db> {
  const client = await clientPromise;
  return client.db("rise-well");
}

export async function getCollection(collectionName: string): Promise<Collection> {
  const db = await getDatabase();
  return db.collection(collectionName);
}

export default clientPromise;