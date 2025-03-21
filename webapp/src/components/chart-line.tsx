"use client"
import { CartesianGrid, Line, LineChart, XAxis, Tooltip } from "recharts"

import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import {
    ChartConfig,
    ChartContainer,
} from "@/components/ui/chart"

const chartConfig = {
    desktop: {
        label: "Desktop",
        color: "hsl(var(--chart-1))",
    },
} satisfies ChartConfig

interface ChartLineProps {
    data: {
        _id: string
        timestamp: number
        heartrate: number
    }[]
}

export function ChartLine({ data }: ChartLineProps) {
    const chartData = data.map(item => ({
        timestamp: new Date(item.timestamp * 1000).toLocaleDateString("en-GB", {
            day: "2-digit",
            month: "short"
        }),
        fullTimestamp: new Date(item.timestamp * 1000).toLocaleString("en-GB", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
        }),
        heartrate: Math.round(item.heartrate),
    }));

    const minDate = new Date(Math.min(...data.map(item => item.timestamp * 1000)))
        .toLocaleDateString("en-GB", { month: "long", year: "numeric" });
    const maxDate = new Date(Math.max(...data.map(item => item.timestamp * 1000)))
        .toLocaleDateString("en-GB", { month: "long", year: "numeric" });

    return (
        <Card>
            <CardHeader>
                <CardTitle>Heart Rate Variability</CardTitle>
                <CardDescription>{`${minDate} - ${maxDate}`}</CardDescription>
            </CardHeader>
            <CardContent>
                <ChartContainer config={chartConfig} className="aspect-auto h-[250px] w-full">
                    <LineChart
                        accessibilityLayer
                        data={chartData}
                        margin={{ left: 12, right: 12 }}
                    >
                        <CartesianGrid vertical={false} />
                        <XAxis
                            dataKey="timestamp"
                            tickLine={false}
                            axisLine={false}
                            tickMargin={8}
                            interval="preserveStartEnd"
                            tickFormatter={(value, index) => (index % 5 === 0 ? value : "")}
                        />
                        <Tooltip
                            content={({ active, payload }) => {
                                if (active && payload && payload.length) {
                                    return (
                                        <div className="bg-white shadow-md rounded-lg px-4 py-3 text-gray-800 border border-gray-200">
                                            <p className="text-sm text-gray-500">
                                                {payload[0].payload.fullTimestamp} {/* Date et heure standard */}
                                            </p>
                                            <p className="text-sm text-gray-500 mt-1">
                                                Heart Rate: <span className=" text-gray-500">{payload[0].value} BPM</span>
                                            </p>
                                        </div>
                                    );
                                }
                                return null;
                            }}
                        />

                        <Line
                            dataKey="heartrate"
                            type="natural"
                            stroke="#2463EB"
                            strokeWidth={2}
                            dot={true} // Affiche les points sur la courbe
                        />
                    </LineChart>
                </ChartContainer>
            </CardContent>
        </Card>
    )
}
