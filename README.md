# PrinTipid — Custom Website Prototype

A responsive school-project website inspired by our PrinTipid design: cream/blue promotional homepage, service cards, how-it-works steps, FAQs, and a dark order-summary panel.

## Files
- `index.html` — page structure and form fields
- `styles.css` — responsive styling
- `main.py` — PyScript event handlers and price calculation

## Run locally
1. Extract this ZIP.
2. Open the folder in VS Code.
3. Install the **Live Server** extension if you do not have it.
4. Right-click `index.html` and choose **Open with Live Server**.
5. Keep an internet connection because PyScript and Google Fonts load from online CDNs.

## Features
- Responsive homepage and service cards
- Student / Teacher / Admin & Staff customer type
- Conditional student or staff information fields
- Local file selection and extension / 10 MB size checks
- Price estimator for B&W (₱2/page), color (₱5/page), photocopy (₱1/page)
- Optional stapling fee (₱3 per job)
- Pages and copies validation
- Live order summary and review status
- Campus pickup or delivery preference
- Clear form button and FAQ section

## Important limitations
This is a browser-only prototype. Selecting a file does **not** upload it to staff. Requests are not saved to a database, and no real printing, payment, or delivery occurs. Do not enter real private information or use confidential files for the public class demo.

## Suggested team contributions
Use each member's own GitHub account to commit meaningful changes. Example: design/CSS, PyScript calculator, form validation, testing/README, and final integration. Replace this section with your team's actual work.

## Price calculation
`total = pages × copies × price per page + optional stapling fee`

Example: 10 B&W pages × 2 copies × ₱2 = ₱40.
