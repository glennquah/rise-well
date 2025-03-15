import { auth, currentUser } from '@clerk/nextjs/server';
import ResponsiveContainer from '../components/ResponsiveContainer';

export default async function Dashboard() {
  const authData = await auth();
  console.log(authData);
  const user = await currentUser();
  console.log(user);
  return (
    <ResponsiveContainer>
      <div className="flex flex-col min-h-screen py-8 gap-2">
        <h1 className="text-4xl font-bold text-start">Sleep Analytics</h1>
        <p className="text-lg text-start text-gray-700">
          Sleep analytics will be displayed here.
        </p>
      </div>
      <p>{authData.userId}</p>
    </ResponsiveContainer>
  );
}
