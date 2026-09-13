import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { MonthlyOutcomePoint } from "../../types/churn";

export function OutcomeStack({ data }: { data: MonthlyOutcomePoint[] }) {
  const recent = data.slice(-14);

  return (
    <div className="chart-frame tall">
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={recent}>
          <CartesianGrid stroke="#e5e7eb" vertical={false} />
          <XAxis dataKey="month" tickLine={false} axisLine={false} />
          <YAxis tickLine={false} axisLine={false} />
          <Tooltip />
          <Legend />
          <Bar dataKey="Churn" stackId="a" fill="#b3261e" />
          <Bar dataKey="Auto Renewal" stackId="a" fill="#385f8f" />
          <Bar dataKey="Positive Renewal" stackId="a" fill="#006b5f" />
          <Bar dataKey="TOS" stackId="a" fill="#d19b29" />
          <Bar dataKey="Leakage" stackId="a" fill="#8f4f35" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

