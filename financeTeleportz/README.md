# FinanceTeleportz - Global Trade Financial Hub

This module manages the financial lifecycle of Teleportz's international trade operations, including imports, exports, and internal fiscal compliance.

## 🚀 Key Modules
1. **Liquidity Management**: Real-time tracking of bank and cash reserves across different currencies.
2. **Trade Invoicing**: Specialized Import/Export invoice tracking with client/vendor management.
3. **Budget Sync**: Monthly/Yearly departmental budget forecasting vs actual spend tracking.
4. **Digital Ledger**: Secure audit trail of every transaction (Freight, Customs, Sales, Purchases).
5. **Compliance Shield**: Tracking of financial document compliance status and ISO sync.

## 🔑 Access Credentials (Demo)
- **Finance Commander ID**: `finance_admin`
- **Security Protocol (Password)**: `teleportz_fin_2026`

## 🛠 Tech Stack
- **Backend**: Flask + SQLAlchemy (sharing `site.db`)
- **Frontend**: Hitech Glassmorphism UI with Space Grotesk typography
- **Hosting**: WSGI compatible (Passenger included)

## 📂 Structure
- `/templates`: Custom dashboards and secure login portals.
- `routes.py`: Fiscal logic, transaction processing, and invoice management.
- `app.py`: Standalone launcher (Port 5006).
