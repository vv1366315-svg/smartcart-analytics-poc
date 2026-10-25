# GTM and GA4 setup checklist (beginner-friendly)

## A. Create GA4
1. Open https://analytics.google.com/ and sign in.
2. Create an Analytics account if needed, then create a GA4 property.
3. Create a Web data stream. For local testing, use your local development URL (for example `http://localhost:8000`) if accepted by the setup flow. You can change configuration later.
4. Note the Measurement ID, formatted like `G-XXXXXXXXXX`. Do not paste secrets into GitHub; a Measurement ID is not a password, but keep project configuration documented clearly.

## B. Create GTM
1. Open https://tagmanager.google.com/.
2. Create an account and a Web container.
3. Copy the container ID, formatted like `GTM-XXXXXXX`.
4. In `website/index.html`, replace **both** occurrences of `GTM-XXXXXXX` with your container ID.
5. Save the file and reload the local website.

## C. Run the website
From the project root:
```powershell
cd website
py -m http.server 8000
```
Open http://localhost:8000. Keep the terminal open while testing.

## D. Configure the Google tag
In GTM:
1. Open **Tags → New**.
2. Choose the **Google tag** tag type.
3. Enter your GA4 Measurement ID (`G-XXXXXXXXXX`).
4. Set the trigger to **Initialization - All Pages** or the recommended all-pages trigger for the tag type.
5. Save as `Google tag - GA4`.

## E. Configure a custom event tag
Repeat for each event (`view_item`, `add_to_cart`, `view_cart`, `begin_checkout`, `purchase`):
1. **Triggers → New → Custom Event**.
2. Set the event name to the exact name, e.g. `add_to_cart`.
3. Set the trigger to all custom events matching that exact event name.
4. **Tags → New → Google Analytics: GA4 Event** (or the current GA4 Event tag option shown in your GTM workspace).
5. Select the Google tag / enter the Measurement ID as required by the interface.
6. Set Event Name to the same event name, e.g. `add_to_cart`.
7. Configure event parameters. For ecommerce events, ensure `currency`, `value` and the ecommerce `items` array are passed correctly. The GTM UI may offer an ecommerce data option such as sending ecommerce data from the data layer; use the current available option and verify the payload in Preview.
8. Select the matching Custom Event trigger and save.

**Important:** GTM interface labels can change. Verify in Preview that each tag fires once and the event parameters have the expected values. If ecommerce `items` are not mapped correctly, document the mapping and fix it before relying on the report.

## F. Test before publishing
1. In GTM, click **Preview** and enter `http://localhost:8000`.
2. In the connected debug window, click Add to cart, open the cart, and complete the simulated checkout.
3. Confirm the matching data layer event appears and the correct GA4 Event tag fires.
4. Open GA4 → Admin / DebugView (the exact navigation may vary) and confirm incoming events.
5. Only publish the GTM container if you are comfortable with the configuration. Save a version with a clear name such as `SmartCart demo tracking`.

## G. Evidence for your submission
Capture your own screenshots of:
- GTM container overview.
- GTM Preview showing `add_to_cart` and `purchase` events.
- GA4 DebugView showing received events.
- Python analysis output and chart.
- Dashboard and SQL query results.

Do not fabricate screenshots or claim that GA4 received events until you have verified it.

## Troubleshooting
- **No GTM activity:** check that both container ID placeholders in `index.html` were replaced correctly and reload.
- **Tag does not fire:** ensure the Custom Event trigger name matches the `dataLayer` event exactly.
- **Event visible in GTM but not GA4:** check the Google tag Measurement ID and event-tag parameters; then check DebugView.
- **No immediate report data:** standard GA4 reports can take time to process. DebugView is more suitable for testing.
- **Localhost rejected or awkward to test:** use a free static host such as GitHub Pages after you have a repository, or another development URL you control. Do not publish personal information.
