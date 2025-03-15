import { auth, currentUser } from '@clerk/nextjs/server';
import ResponsiveContainer from './components/ResponsiveContainer';

export default async function Home() {
  const authData = await auth();
  console.log(authData);
  const user = await currentUser();
  console.log(user);
  return <ResponsiveContainer>HOME PAGE</ResponsiveContainer>;
}
