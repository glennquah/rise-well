import { AlarmClockHistory } from '../components/AlarmClockHistory';
import AlarmReport from '../components/AlarmReport';
import ResponsiveContainer from '../components/ResponsiveContainer';
import { ReusableTabs } from '../components/ReusableTabs';

export default async function AlarmClockAnalytics() {
  const tabs = [
    {
      value: 'history',
      label: 'History',
      content: <AlarmClockHistory />,
    },
    {
      value: 'report',
      label: 'Report',
      content: <AlarmReport />,
    },
  ];

  return (
    <ResponsiveContainer>
      <div className="flex flex-col min-h-screen py-8 gap-4">
        <h1 className="text-4xl font-bold text-start">Alarm Clock Analytics</h1>
        <ReusableTabs defaultValue="history" tabs={tabs} />
      </div>
    </ResponsiveContainer>
  );
}
