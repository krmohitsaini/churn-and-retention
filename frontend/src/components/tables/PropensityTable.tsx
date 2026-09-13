import { Link } from "react-router-dom";
import type { PropensityCustomer } from "../../types/propensity";

export function PropensityTable({ customers }: { customers: PropensityCustomer[] }) {
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Customer</th>
            <th>Province</th>
            <th>Segment</th>
            <th>Product</th>
            <th>Value</th>
            <th>Risk</th>
            <th>Propensity</th>
            <th>Top driver</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {customers.map((customer) => (
            <tr key={customer.customer_id}>
              <td>
                <Link to={`/customers/${customer.customer_id}`}>{customer.customer_id}</Link>
                <span>{customer.customer_name}</span>
              </td>
              <td>{customer.province}</td>
              <td>{customer.segment}</td>
              <td>{customer.product_type}</td>
              <td>${customer.estimated_annual_value?.toLocaleString()}</td>
              <td>
                <span className={`risk-pill ${customer.risk_band.toLowerCase()}`}>{customer.risk_band}</span>
              </td>
              <td>{Math.round(customer.churn_probability * 100)}%</td>
              <td>{customer.top_driver}</td>
              <td>{customer.recommended_action}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

