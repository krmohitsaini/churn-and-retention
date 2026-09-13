import type { DashboardFilters as DashboardFilterValues, SegmentOptions } from "../../types/portfolio";

const fields = [
  { key: "commodity_type", label: "Commodity" },
  { key: "channel", label: "Channel" },
  { key: "sales_type", label: "Sales type" },
  { key: "AMB_status", label: "AMB" },
  { key: "evergreen_status", label: "Evergreen" },
  { key: "surge_status", label: "Surge" },
  { key: "digital_status", label: "Digital" }
] as const;

type Props = {
  options: SegmentOptions;
  values: DashboardFilterValues;
  onChange: (values: DashboardFilterValues) => void;
};

export function DashboardFilters({ options, values, onChange }: Props) {
  return (
    <section className="filter-bar">
      {fields.map((field) => (
        <label key={field.key}>
          <span>{field.label}</span>
          <select
            value={values[field.key] ?? "All"}
            onChange={(event) => onChange({ ...values, [field.key]: event.target.value })}
          >
            <option>All</option>
            {(options[field.key] ?? []).map((option) => (
              <option key={option} value={option}>
                {option === "true" ? "Yes" : option === "false" ? "No" : option}
              </option>
            ))}
          </select>
        </label>
      ))}
      <button className="secondary-button" onClick={() => onChange({})}>Clear</button>
    </section>
  );
}
