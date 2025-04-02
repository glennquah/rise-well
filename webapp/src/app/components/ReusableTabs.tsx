'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import * as React from 'react';

interface TabItem {
  value: string;
  label: string;
  content: React.ReactNode;
}

interface ReusableTabsProps {
  defaultValue?: string;
  tabs: TabItem[];
}

export const ReusableTabs: React.FC<ReusableTabsProps> = ({
  defaultValue,
  tabs,
}) => {
  return (
    <Tabs defaultValue={defaultValue} className="relative mr-auto w-full">
      <TabsList className="w-full justify-start rounded-none border-b bg-transparent p-0">
        {tabs.map((tab) => (
          <TabsTrigger
            key={tab.value}
            value={tab.value}
            className="relative rounded-b-none border-b-2 border-b-transparent bg-transparent px-6 py-2 font-semibold text-muted-foreground shadow-none transition-none focus-visible:ring-0 data-[state=active]:border-b-primary data-[state=active]:text-foreground data-[state=active]:shadow-none"
          >
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>
      {tabs.map((tab) => (
        <div className="pb-2" key={tab.value}>
          <TabsContent value={tab.value}>{tab.content}</TabsContent>
        </div>
      ))}
    </Tabs>
  );
};
