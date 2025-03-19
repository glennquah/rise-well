import { currentUser } from '@clerk/nextjs/server';
import ResponsiveContainer from './components/ResponsiveContainer';

export default async function Home() {
  const user = await currentUser();
  const name = user?.firstName || user?.fullName || 'Guest';
  console.log(user);

  return (
    <ResponsiveContainer>
      <div className="flex flex-col min-h-screen py-8 gap-2">
        <h1 className="text-4xl font-bold text-start">Hello, {name}!</h1>
        <p className="text-lg text-start text-gray-700">
          Welcome to RiseWell – your personalized IoT alarm clock designed to
          help you wake up refreshed and ready for the day. Explore your sleep
          insights, monitor your health, and experience a smarter morning
          routine.
        </p>
      </div>
      <div>Add some analytics here</div>
    </ResponsiveContainer>
  );
}
