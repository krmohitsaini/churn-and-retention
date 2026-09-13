import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import type { ChartPoint } from "../../types/portfolio";

const colors = ["#006b5f", "#385f8f", "#d19b29", "#8f4f35", "#7b6bb0", "#5b7c4a"];

export function DonutChart({ data }: { data: ChartPoint[] }) {
  return (
    <div className="donut-layout">
      <div className="donut-chart">
        <ResponsiveContainer width="100%" height={210}>
          <PieChart>
            <Pie data={data} innerRadius={58} outerRadius={88} dataKey="value" nameKey="name" paddingAngle={2}>
              {data.map((entry, index) => (
                <Cell key={entry.name} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="legend-list">
        {data.map((entry, index) => (
          <div key={entry.name}>
            <span style={{ background: colors[index % colors.length] }} />
            <strong>{entry.name}</strong>
            <em>{entry.value.toLocaleString()}</em>
          </div>
        ))}
      </div>
    </div>
  );
}

