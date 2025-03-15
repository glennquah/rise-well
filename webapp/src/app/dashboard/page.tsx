import { auth, currentUser } from "@clerk/nextjs/server";

export const dynamic = "force-dynamic";
export const fetchCache = "force-no-store";

export default async function Home() {
  const authData = await auth();
  console.log(authData);
  const user = await currentUser();
  console.log(user);
  return (
    <div>
      <h1>Dashboard</h1>
    </div>
  );
}
