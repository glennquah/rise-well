import { Collection, Db, MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI as string;
if (!uri) throw new Error("Missing MONGODB_URI environment variable");

const options = {};

let client: MongoClient;
let clientPromise: Promise<MongoClient>;

declare global {
  var _mongoClientPromise: Promise<MongoClient>;
}

if (!global._mongoClientPromise) {
  client = new MongoClient(uri, options);
  global._mongoClientPromise = client.connect();
}

clientPromise = global._mongoClientPromise;

export async function getDatabase(): Promise<Db> {
  const client = await clientPromise;
  return client.db("rise-well");
}

export async function getCollection(collectionName: string): Promise<Collection> {
  const db = await getDatabase();
  return db.collection(collectionName);
}

export default clientPromise;