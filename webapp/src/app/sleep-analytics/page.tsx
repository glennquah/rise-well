import { auth, currentUser } from '@clerk/nextjs/server';
import ResponsiveContainer from '../components/ResponsiveContainer';

export default async function Dashboard() {
  const authData = await auth();
  console.log(authData);
  const user = await currentUser();
  console.log(user);
  return <ResponsiveContainer>SLEEP ANALYTICS PAGE</ResponsiveContainer>;
}
