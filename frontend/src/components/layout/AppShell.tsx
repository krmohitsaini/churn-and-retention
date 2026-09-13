import { Activity, BarChart3, Gauge, LayoutDashboard, Settings } from "lucide-react";
import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/portfolio", label: "Portfolio", icon: LayoutDashboard },
  { to: "/churn", label: "Churn", icon: Activity },
  { to: "/propensity", label: "Propensity", icon: Gauge },
  { to: "/admin/kpis", label: "KPI Logic", icon: BarChart3 },
  { to: "/admin/apis", label: "API Debug", icon: Settings }
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">N</div>
          <div>
            <div className="brand-name">NRG Retention</div>
            <div className="brand-subtitle">Canada portfolio</div>
          </div>
        </div>
        <nav className="nav-list">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.to} to={item.to} className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}>
                <Icon size={18} />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>
      <main className="main-content">{children}</main>
    </div>
  );
}
