import { SignedIn, UserButton } from '@clerk/nextjs';

const NavigationBar = () => {
  return (
    <header className="flex justify-between items-center p-4 gap-4 h-16">
      <h1>RiseWell</h1>
      <SignedIn>
        <UserButton showName={true} />
      </SignedIn>
    </header>
  );
};

export default NavigationBar;
