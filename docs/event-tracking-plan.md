# Event tracking plan

## Scope
The site is a non-production demonstration store. Checkout and purchase are simulated. The site does not collect real payment details or personal customer information.

| Website action | `dataLayer` event | Important parameters | GA4 event |
|---|---|---|---|
| Product cards displayed on initial page load | `view_item` | `currency`, `value`, `ecommerce.items` | `view_item` |
| Click Add to cart | `add_to_cart` | `currency`, `value`, `ecommerce.items` | `add_to_cart` |
| Open cart | `view_cart` | `currency`, `value`, `ecommerce.items` | `view_cart` |
| Click Proceed to checkout | `begin_checkout` | `currency`, `value`, `ecommerce.items` | `begin_checkout` |
| Complete simulated order | `purchase` | `transaction_id`, `currency`, `value`, `ecommerce.items` | `purchase` |
| Click Explore products | `select_promotion` | `promotion_name`, `creative_name` | `select_promotion` |

## Implementation notes
- `website/app.js` pushes these events to `window.dataLayer`.
- GTM needs a Custom Event trigger and a GA4 Event tag for each event that should be sent to GA4.
- In each GA4 Event tag, pass the ecommerce parameters and items according to the GTM/GA4 configuration. For ecommerce events, verify the `items` array is mapped correctly.
- Product cards are counted as viewed on initial page load for this simplified demo. A production site should consider viewport visibility and actual product-detail page views.
- The `purchase` event is triggered in the demo when the user clicks the simulated checkout button. No actual payment is processed.
- Test with GTM Preview / Tag Assistant and GA4 DebugView before claiming the events are received by GA4.
