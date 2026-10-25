# Case study: SmartCart Analytics

## 1. Business problem
An online store needs to understand how visitors move from product discovery to purchase and where the shopping journey may be losing potential customers.

## 2. Objective
Demonstrate a practical workflow that uses GTM and GA4 to collect website interaction events, then Python and SQL to process and analyze event data.

## 3. Solution
- Built a static demonstration storefront with simulated cart and checkout.
- Added `dataLayer` events for ecommerce interactions.
- Documented the GTM and GA4 configuration and validation process.
- Used Python/Pandas to inspect data, calculate descriptive metrics, create a chart and load records into SQLite.
- Wrote SQL queries for event counts, popular products, traffic-source comparison and cart/purchase analysis.
- Created an optional Streamlit dashboard.

## 4. Results
Insert the metrics and screenshots from your own successful run here. Clearly identify results from synthetic sample data versus any events actually verified in your GA4 property.

## 5. Recommendations
Use the observed funnel and product/source patterns to choose areas for further investigation. Example hypotheses include unclear product information, checkout friction, unexpected costs, or differences in traffic intent. Do not claim a cause without evidence.

## 6. Limitations
- Sample data is synthetic.
- The static site simulates checkout and has no real payment system.
- The simplified event ratios count sessions containing an event and do not guarantee ordered funnel progression.
- Production analysis would require clear session rules, event IDs, attribution definitions, consent handling, privacy review and quality checks.
