import { auth, currentUser } from '@clerk/nextjs/server';
import { AlarmClockHistory } from '../components/AlarmClockHistory';
import ResponsiveContainer from '../components/ResponsiveContainer';

export default async function AlarmClockAnalytics() {
  const authData = await auth();
  console.log(authData);
  const user = await currentUser();
  console.log(user);
  return (
    <ResponsiveContainer>
      <div className="flex flex-col min-h-screen py-8 gap-2">
        <h1 className="text-4xl font-bold text-start">Alarm Clock Analytics</h1>
        <AlarmClockHistory />
      </div>
    </ResponsiveContainer>
  );
}
