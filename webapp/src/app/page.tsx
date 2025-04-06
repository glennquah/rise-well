import { currentUser } from '@clerk/nextjs/server';
import HeroSection from './components/Header';
import QuickAccessSection from './components/QuickAccessSection';
import ResponsiveContainer from './components/ResponsiveContainer';
import SummarySection from './components/SummarySection';

export default async function Home() {
  const user = await currentUser();
  const name = user?.firstName || user?.fullName || 'Guest';

  return (
    <ResponsiveContainer>
      <HeroSection name={name} />
      <SummarySection />
      <QuickAccessSection />
    </ResponsiveContainer>
  );
}
