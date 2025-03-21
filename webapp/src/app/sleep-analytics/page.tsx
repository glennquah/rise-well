import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { getCollection } from "../lib/mongodb";
import PollingDataDisplay from "../components/PollingDataDisplay";
import React from "react";

export default async function Page() {
  const heartrateCollection = await getCollection("heartrate");
  const heartRates = await heartrateCollection.find({}).toArray();
  
  const plainHeartRates = heartRates.map((item) => ({
    _id: item._id.toString(),
    timestamp: item.timestamp,
    heartrate: item.heartrate,
  }));

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
              <PollingDataDisplay initialData={plainHeartRates} />
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}


// import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
// import { getCollection } from "../lib/mongodb";
// import React from "react";
// import { SectionCards } from "@/components/section-cards";
// import { ChartLine } from "@/components/chart-line";

// export default async function Page() {
//   const heartrateCollection = await getCollection("heartrate");
//   const heartRates = await heartrateCollection.find({}).toArray();

//   const plainHeartRates = heartRates.map((item) => ({
//     _id: item._id.toString(),
//     timestamp: item.timestamp,
//     heartrate: item.heartrate,
//   }));

//   return (
//     <SidebarProvider
//       style={
//         {
//           "--sidebar-width": "calc(var(--spacing) * 72)",
//           "--header-height": "calc(var(--spacing) * 12)",
//         } as React.CSSProperties
//       }
//     >
//       {/* <AppSidebar variant="inset" /> */}
//       <SidebarInset>
//         {/* <SiteHeader /> */}
//         <div className="flex flex-1 flex-col">
//           <div className="@container/main flex flex-1 flex-col gap-2">
//             <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
//               <SectionCards data={plainHeartRates} />
//               <div className="px-4 lg:px-6">
//                 {/* <ChartAreaInteractive /> */}
//                 <ChartLine data={plainHeartRates}></ChartLine>
//               </div>
//               {/* <DataTable data={data} /> */}
//             </div>
//           </div>
//         </div>
//       </SidebarInset>
//     </SidebarProvider>
//   );
// }





