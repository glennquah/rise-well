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
    <Tabs defaultValue={defaultValue} className="w-fit rounded-full p-1">
      <TabsList className="flex gap-1 bg-transparent p-0 shadow-none bg-gray-200">
        {tabs.map((tab) => (
          <TabsTrigger
            key={tab.value}
            value={tab.value}
            className="rounded-full px-4 py-1.5 text-sm font-medium text-muted-foreground data-[state=active]:bg-white data-[state=active]:text-foreground data-[state=active]:shadow-sm transition-all"
          >
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>

      {tabs.map((tab) => (
        <TabsContent key={tab.value} value={tab.value} className="pt-2">
          {tab.content}
        </TabsContent>
      ))}
    </Tabs>
  );
};
