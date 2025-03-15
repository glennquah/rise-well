import { auth, currentUser } from '@clerk/nextjs/server';

export default async function Dashboard() {
  const authData = await auth();
  console.log(authData);
  const user = await currentUser();
  console.log(user);
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium quae
      sequi ex consectetur illo impedit libero. Recusandae animi velit possimus.
    </div>
  );
}
