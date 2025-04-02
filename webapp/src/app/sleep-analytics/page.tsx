// import { auth, currentUser } from '@clerk/nextjs/server';
// import ResponsiveContainer from '../components/ResponsiveContainer';

// export default async function Dashboard() {
//   const authData = await auth();
//   console.log(authData);
//   const user = await currentUser();
//   console.log(user);
//   return (
//     <ResponsiveContainer>
//       <div className="flex flex-col min-h-screen py-8 gap-2">
//         <h1 className="text-4xl font-bold text-start">Sleep Analytics</h1>
//         <p className="text-lg text-start text-gray-700">
//           Sleep analytics will be displayed here.
//         </p>
//       </div>
//       <p>{authData.userId}</p>
//     </ResponsiveContainer>
//   );
// }

import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import PollingDataDisplay from "../components/PollingDataDisplay";
import React from "react";

export default async function Page() {
  return (
    <SidebarProvider
      style={{
        "--sidebar-width": "calc(var(--spacing) * 72)",
        "--header-height": "calc(var(--spacing) * 12)",
      } as React.CSSProperties}
    >
      <SidebarInset>
        {/* <AppSidebar variant="inset" /> */}
        {/* <SiteHeader /> */}
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
              <PollingDataDisplay  />
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}





