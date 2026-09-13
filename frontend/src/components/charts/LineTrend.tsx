import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type TrendPoint = {
  month: string;
  [key: string]: string | number;
};

export function LineTrend({ data, dataKey, stroke = "#006b5f" }: { data: TrendPoint[]; dataKey: string; stroke?: string }) {
  return (
    <div className="chart-frame">
      <ResponsiveContainer width="100%" height={260}>
        <AreaChart data={data}>
          <CartesianGrid stroke="#e5e7eb" vertical={false} />
          <XAxis dataKey="month" tickLine={false} axisLine={false} />
          <YAxis tickLine={false} axisLine={false} />
          <Tooltip />
          <Area type="monotone" dataKey={dataKey} stroke={stroke} fill={stroke} fillOpacity={0.16} strokeWidth={3} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
