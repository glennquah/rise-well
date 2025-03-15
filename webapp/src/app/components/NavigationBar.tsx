import { UserButton } from '@clerk/nextjs';

const NavigationBar = () => {
  return (
    <header className="flex justify-between">
      <h1>RiseWell</h1>
      <UserButton showName={true} />
    </header>
  );
};

export default NavigationBar;
