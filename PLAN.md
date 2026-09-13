# Churn and Retention App Plan

## 1. Project Context

This project is a customer retention and churn analytics web app for an energy client, NRG Canada.

The client currently observes roughly 80,000 customers leaving each year. The business may still be growing overall, but churn remains high enough that the app should help business users understand where churn is concentrated, why it is happening, and which customers should be prioritized for retention actions.

The app should start with CSV-backed data during development and later connect to Databricks tables. The final app is expected to be hosted in Databricks Apps.

## 2. Primary Goals

Build a clean, visually appealing, modular web app that helps users:

1. Understand the current customer portfolio.
2. Explore historical and current churn trends.
3. Drill into customer segments with high churn.
4. View customer-level churn propensity scores.
5. Understand why specific customers are at risk.
6. Export targeted customer lists for campaigns.
7. Keep KPI logic, API logic, and UI modules easy to debug and modify.

## 3. Recommended Technical Architecture

Use a split frontend/backend architecture:

- Frontend: React + TypeScript + Vite
- Backend: Python + FastAPI
- Data access now: CSV files
- Data access later: Databricks SQL / Delta tables
- Modeling now: Mock or precomputed churn propensity scores
- Modeling later: Databricks ML / MLflow model pipeline
- Deployment later: Databricks Apps

Databricks Apps supports Python, Node.js, and mixed Python/Node apps, so this architecture should work well for local development and future Databricks deployment.

## 4. Suggested Project Structure

```text
churn-and-retention/
  PLAN.md
  README.md
  app.yaml
  package.json
  requirements.txt

  frontend/
    index.html
    package.json
    vite.config.ts
    tsconfig.json
    src/
      main.tsx
      App.tsx
      routes.tsx
      styles/
        globals.css
        theme.css
      api/
        client.ts
        portfolioApi.ts
        churnApi.ts
        propensityApi.ts
        exportApi.ts
      pages/
        PortfolioPage.tsx
        ChurnPage.tsx
        PropensityPage.tsx
        CustomerDetailPage.tsx
        AdminKpiPage.tsx
        AdminApiPage.tsx
      components/
        layout/
        filters/
        charts/
        tables/
        cards/
        states/
      types/
        portfolio.ts
        churn.ts
        propensity.ts
        customer.ts

  backend/
    app/
      main.py
      api/
        __init__.py
        health.py
        portfolio.py
        churn.py
        propensity.py
        customers.py
        exports.py
        admin.py
      services/
        __init__.py
        portfolio_service.py
        churn_service.py
        propensity_service.py
        customer_service.py
        export_service.py
      kpis/
        __init__.py
        portfolio_kpis.py
        churn_kpis.py
        retention_kpis.py
        revenue_kpis.py
      data/
        __init__.py
        base_repository.py
        csv_repository.py
        databricks_repository.py
      models/
        __init__.py
        churn_model.py
        explainability.py
      schemas/
        __init__.py
        common.py
        portfolio.py
        churn.py
        propensity.py
        customer.py
      config/
        __init__.py
        settings.py

  data/
    sample/
      customers.csv
      churn_events.csv
      propensity_scores.csv
      customer_interactions.csv
      offers.csv
    raw/
    processed/

  notebooks/
    data_profiling/
    model_training/

  tests/
    backend/
    frontend/
```

## 5. Application Pages

### 5.1 Portfolio Overview Page

Purpose: Show the current customer base and allow users to understand the shape of the portfolio.

Primary features:

- Total active customers
- Customer count by province
- Customer count by segment
- Customer count by commodity or product type
- Customer count by plan or contract type
- Customer count by tenure band
- Revenue or margin summary, if available
- Filters for geography, customer type, product, segment, acquisition channel, tenure, and contract status
- Drillable charts and tables

Suggested visuals:

- KPI cards
- Segment distribution bar charts
- Province map or ranked province table
- Tenure distribution
- Product mix chart
- Active customer trend

### 5.2 Churn Analytics Page

Purpose: Help users identify where churn is happening and which segments are most concerning.

Primary features:

- Overall churn rate over time
- Number of churned customers over time
- Churn by segment
- Churn by province
- Churn by product or commodity
- Churn by tenure band
- Churn by acquisition channel
- Churn reason breakdown, if available
- Voluntary vs involuntary churn, if available
- Cohort retention view
- Filters matching the portfolio page

Suggested visuals:

- Churn trend line
- Segment churn heatmap
- Churn by tenure bar chart
- Cohort retention table
- Churn reason Pareto chart
- Revenue-at-risk trend

### 5.3 Churn Propensity Page

Purpose: Show customer-level churn risk and help users create target lists for retention campaigns.

Primary features:

- Customer table with churn propensity score
- Risk band: Low, Medium, High, Critical
- Predicted churn window: next 30, 60, 90, or 180 days
- Key churn drivers for each customer
- Driver weights or contribution values
- Customer attributes such as province, product, tenure, contract, usage, billing behavior, complaints, and service interactions
- Recommended retention offer or action
- Filters for risk band, segment, geography, product, churn window, and customer value
- Export selected or filtered customers as CSV

Suggested table columns:

- Customer ID
- Customer name or masked identifier, depending on privacy rules
- Province
- Segment
- Product
- Tenure
- Estimated annual value
- Churn propensity
- Risk band
- Top churn driver
- Recommended action
- Last interaction date

### 5.4 Customer Detail Page

Purpose: Allow deeper investigation into a specific customer.

Primary features:

- Customer profile summary
- Current product and plan
- Tenure and acquisition channel
- Billing and payment indicators
- Usage history
- Complaint or service interaction history
- Churn propensity score
- Top churn drivers
- Recommended retention action
- Similar customer benchmark, if available later

### 5.5 Admin KPI Page

Purpose: Provide a developer/admin-facing place to understand KPI definitions and calculations.

This page should not be visible to normal end users.

Primary features:

- List of KPI definitions
- Formula descriptions
- Source fields used for each KPI
- Last calculated timestamp
- Example input and output, where useful
- Links or labels pointing to the backend module responsible for each KPI

KPI logic should live in backend files under:

```text
backend/app/kpis/
```

Do not calculate core business KPIs directly inside frontend components.

### 5.6 Admin API Page

Purpose: Provide a developer/admin-facing API reference and debug surface.

This page should not be visible to normal end users.

Primary features:

- List of available API endpoints
- Short description of each endpoint
- Expected filters and query parameters
- Sample response preview
- Basic health check status
- Data source currently in use: CSV or Databricks

API route code should live in:

```text
backend/app/api/
```

Frontend API wrapper code should live in:

```text
frontend/src/api/
```

## 6. Backend API Design

Use FastAPI with versioned routes.

Suggested base path:

```text
/api/v1
```

Suggested endpoints:

```text
GET /api/v1/health
GET /api/v1/portfolio/summary
GET /api/v1/portfolio/segments
GET /api/v1/portfolio/timeseries

GET /api/v1/churn/summary
GET /api/v1/churn/timeseries
GET /api/v1/churn/by-segment
GET /api/v1/churn/cohorts
GET /api/v1/churn/reasons

GET /api/v1/propensity/summary
GET /api/v1/propensity/customers
GET /api/v1/propensity/customers/{customer_id}
GET /api/v1/propensity/drivers

GET /api/v1/customers/{customer_id}

POST /api/v1/exports/propensity

GET /api/v1/admin/kpis
GET /api/v1/admin/apis
GET /api/v1/admin/data-status
```

Each frontend page should call a dedicated frontend API wrapper file. For example:

- `PortfolioPage.tsx` uses `frontend/src/api/portfolioApi.ts`
- `ChurnPage.tsx` uses `frontend/src/api/churnApi.ts`
- `PropensityPage.tsx` uses `frontend/src/api/propensityApi.ts`
- Export actions use `frontend/src/api/exportApi.ts`

Each backend API route should be thin. It should validate request parameters, call a service, and return a response. Business logic should live in services and KPI modules.

## 7. Data Layer Design

Create a repository abstraction so the app can switch from CSV to Databricks later without rewriting business logic.

Use:

```text
backend/app/data/base_repository.py
backend/app/data/csv_repository.py
backend/app/data/databricks_repository.py
```

The backend services should depend on the base repository interface, not directly on CSV or Databricks-specific code.

During local development:

- Read sample data from `data/sample/`
- Use environment variables to choose data source
- Default to CSV mode

Later in Databricks:

- Use Databricks SQL or Spark-backed access
- Read from governed Delta tables
- Keep the same service and API layer

## 8. Initial Sample Data Model

Start with small but realistic CSV files.

### customers.csv

Suggested fields:

- customer_id
- customer_name
- province
- city
- customer_type
- segment
- product_type
- plan_type
- contract_status
- acquisition_channel
- signup_date
- tenure_months
- estimated_annual_value
- current_status

### churn_events.csv

Suggested fields:

- customer_id
- churn_date
- churn_reason
- churn_type
- product_type
- province
- segment
- estimated_lost_value

### propensity_scores.csv

Suggested fields:

- customer_id
- score_date
- churn_probability
- risk_band
- prediction_window_days
- top_driver_1
- top_driver_1_weight
- top_driver_2
- top_driver_2_weight
- top_driver_3
- top_driver_3_weight
- recommended_action
- recommended_offer

### customer_interactions.csv

Suggested fields:

- interaction_id
- customer_id
- interaction_date
- channel
- interaction_type
- sentiment
- issue_category
- resolved_flag

### offers.csv

Suggested fields:

- offer_id
- offer_name
- offer_type
- target_segment
- eligibility_rule
- expected_retention_lift
- estimated_cost

## 9. KPI Module Design

Keep KPI calculations in dedicated backend files so they are easy to find and edit.

Suggested modules:

```text
backend/app/kpis/portfolio_kpis.py
backend/app/kpis/churn_kpis.py
backend/app/kpis/retention_kpis.py
backend/app/kpis/revenue_kpis.py
```

Suggested KPIs:

- Active customers
- New customers
- Churned customers
- Gross churn rate
- Net customer growth
- Retention rate
- Revenue-at-risk
- Lost estimated annual value
- Average tenure
- Segment churn index
- High-risk customer count
- Critical-risk customer count

Each KPI should have:

- A clear function name
- A docstring with the business definition
- Inputs and expected columns documented
- Unit tests for important calculations

## 10. Propensity Model Design

For the first version, the app can use precomputed propensity scores from CSV.

Later, create a proper model pipeline in Databricks:

1. Build feature table from customer, usage, billing, interaction, and churn history.
2. Train classification model to predict churn within a defined window.
3. Evaluate model using AUC, precision, recall, lift, calibration, and segment performance.
4. Use explainability outputs such as SHAP values or feature contributions.
5. Register model in MLflow.
6. Score active customers on a schedule.
7. Write scored customers to a Databricks table.
8. App reads the latest scored table.

The app should show:

- Churn probability
- Risk band
- Prediction window
- Top drivers
- Recommended action
- Model version
- Score date

Do not train the production model directly inside the web app.

## 11. Export Design

The propensity page should allow business users to export customer lists.

Export options:

- Export all filtered customers
- Export only selected customers
- Include or exclude explanatory drivers
- Include recommended offer/action

Initial format:

- CSV download

Later formats:

- Push to campaign tool
- Save export history to Databricks table
- Add approval workflow

Backend route:

```text
POST /api/v1/exports/propensity
```

Export service:

```text
backend/app/services/export_service.py
```

## 12. Debuggability Requirements

The project should be easy to debug.

Follow these rules:

- Keep frontend pages separate.
- Keep frontend API wrappers separate.
- Keep backend API routes separate.
- Keep backend service logic separate.
- Keep KPI calculations separate.
- Keep data access separate from business logic.
- Keep model/scoring logic separate from dashboard logic.
- Use clear file names.
- Add simple tests for KPI calculations.
- Add health check and data status endpoints.
- Add structured logging in the backend.
- Avoid putting business calculations directly in React components.

## 13. Frontend Design Direction

The UI should feel modern, polished, and client-ready.

Design principles:

- Clean executive dashboard style
- Calm professional color palette
- Strong spacing and typography
- Useful charts over decorative visuals
- Clear filters
- Fast drilldowns
- Tables that support sorting, filtering, and export
- Avoid clutter
- Avoid marketing-style landing pages

Recommended layout:

- Left sidebar navigation
- Top bar with page title, data freshness, and global filters
- Main content area with KPI cards, charts, and tables
- Detail panels or drilldown pages for deeper analysis

Suggested navigation:

- Portfolio
- Churn
- Propensity
- Customers
- Admin

Admin should be hidden or protected later.

## 14. Security and Privacy Considerations

Because this app may eventually contain customer-level data:

- Do not expose unnecessary personally identifiable information.
- Mask customer names if needed.
- Add role-based access later.
- Restrict export access to approved users.
- Log exports for auditability.
- Keep secrets and Databricks connection details out of source code.
- Use environment variables or Databricks secrets.

## 15. Future Databricks Integration

When moving from CSV to Databricks:

- Replace CSV repository with Databricks repository.
- Keep API and frontend contracts stable where possible.
- Read customer portfolio from Delta tables.
- Read churn events from Delta tables.
- Read propensity scores from scored model output table.
- Use Databricks Jobs for model scoring.
- Use MLflow for model versioning.
- Use Databricks permissions for access control.
- Deploy app through Databricks Apps from Git.

## 16. Suggested Implementation Phases

### Phase 1: Skeleton

- Create React frontend.
- Create FastAPI backend.
- Add app shell with navigation.
- Add health endpoint.
- Add sample CSV files.
- Add CSV repository.
- Add shared response schemas.

### Phase 2: Portfolio Page

- Add portfolio summary endpoint.
- Add portfolio segmentation endpoint.
- Add portfolio filters.
- Build Portfolio page with KPI cards and charts.

### Phase 3: Churn Page

- Add churn summary endpoint.
- Add churn timeseries endpoint.
- Add churn by segment endpoint.
- Add churn reason endpoint.
- Build Churn page with filters and drilldowns.

### Phase 4: Propensity Page

- Add propensity customer endpoint.
- Add risk band filtering.
- Add customer-level table.
- Add driver display.
- Add export endpoint.
- Add CSV export from filtered or selected rows.

### Phase 5: Customer Detail

- Add customer detail endpoint.
- Build customer detail page.
- Show profile, churn score, top drivers, and interaction history.

### Phase 6: Admin and Debug

- Add Admin KPI page.
- Add Admin API page.
- Add data status endpoint.
- Add basic backend logging.
- Add KPI unit tests.

### Phase 7: Databricks Readiness

- Add Databricks repository placeholder.
- Add environment-based data source selection.
- Add app.yaml for Databricks Apps.
- Document local and Databricks deployment steps.

## 17. Definition of Done for Initial Skeleton

The first working version should include:

- Running React frontend.
- Running FastAPI backend.
- Portfolio page with sample data.
- Churn page with sample data.
- Propensity page with sample data.
- Customer export from propensity page.
- Backend API routes split by domain.
- KPI calculations split into dedicated modules.
- CSV data repository abstraction.
- Clean folder structure.
- README with local run instructions.

## 18. Important Notes for Codex Implementation

When using this file to create the project skeleton:

- Prefer modular files over large all-in-one files.
- Use clear names that match the business domain.
- Keep API contracts simple and typed.
- Add realistic sample data, not placeholder-only data.
- Make the frontend visually polished from the start.
- Do not build a marketing landing page.
- The first screen should be the actual application.
- Keep all business KPI logic out of frontend components.
- Keep Databricks integration pluggable but do not require Databricks for local development.
- Use CSV data first, then add Databricks later.

