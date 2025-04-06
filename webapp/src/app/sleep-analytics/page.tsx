import PollingDataDisplay from '../components/PollingDataDisplay';
import ResponsiveContainer from '../components/ResponsiveContainer';

export default async function Page() {
  return (
    <ResponsiveContainer>
      <div className="flex flex-col min-h-screen py-8">
        <div className="pt-4">
          <h1 className="text-4xl font-bold text-start">Sleep Analytics</h1>
          <p className="text-foreground/70 mt-2">
            Track your sleep patterns, quality, and get detailed insights
            breakdown
          </p>
        </div>
        <div className="flex flex-col gap-4 md:gap-6">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <PollingDataDisplay />
            </div>
          </div>
        </div>
      </div>
    </ResponsiveContainer>
  );
}
