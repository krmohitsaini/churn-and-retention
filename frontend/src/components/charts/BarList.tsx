import type { ChartPoint } from "../../types/portfolio";

export function BarList({ data }: { data: ChartPoint[] }) {
  const maxValue = Math.max(...data.map((point) => point.value), 1);

  return (
    <div className="bar-list">
      {data.map((point) => (
        <div className="bar-row" key={point.name}>
          <div className="bar-label">
            <span>{point.name}</span>
            <strong>{point.value}</strong>
          </div>
          <div className="bar-track">
            <div className="bar-fill" style={{ width: `${(point.value / maxValue) * 100}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

