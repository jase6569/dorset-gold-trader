# Photo quote (Cloudflare Worker)

This Worker sits behind the customer quote page at `quote/index.html`. Customers send photos of their gold, and OpenAI says what each piece is. The Worker then does the sums itself using Mastermelt's counter price and Mike's rate, so the AI never sets a price. If the customer asks to be called, the quote, their details and their photos go to Mike's iPhone through ntfy.

## Setup (about 10 minutes)

1. Cloudflare: go to Workers & Pages, create a Worker named `gold-quote`, paste in `worker.js` and deploy.
2. In the Worker, open Settings, then Variables and secrets, and add these **Secrets**:
   * `OPENAI_API_KEY`: the same key the coin scanner uses
   * `NTFY_TOPIC`: Mike's private ntfy topic (the `NTFY_TOPIC_MIKE` secret in gold-sell-timer), so leads land in the app he already has. Use a new topic if he wants leads kept apart from sell alerts.
   * `QUOTE_SECRET`: any long random text
3. Add these **Variables**:
   * `PAY_PCT`: Mike's rate as a % of Mastermelt's counter price (default 80)
   * `COIN_PAY_PCT`: his rate for gold coins, only if it's different
   * `ALLOWED_ORIGINS`: only needed for a site other than dorsetgoldandjewellery.co.uk, which is already allowed
4. Copy the Worker's address (https://gold-quote.<name>.workers.dev) into `QUOTE_URL` near the bottom of `quote/index.html`. `SHOP` already has his number (01202 117896).

Until `QUOTE_URL` is filled in, the page runs in demo mode and shows a made-up quote, which is handy for showing Mike.

## How the price is worked out

* Gold coins: official pure gold weight × Mastermelt's pure gold price × `COIN_PAY_PCT`.
* Jewellery with a readable hallmark: weight × Mastermelt's price for that carat × `PAY_PCT`. The weight is the customer's if they gave one, otherwise the AI's low to high estimate from the photo.
* No readable hallmark: priced between 9ct and 18ct and flagged.
* Plated, silver, platinum or unknown items: no price, with a note to bring them in.
* The overall low figure is taken down another 5%, and everything is rounded to £5.

Quotes are signed, so a customer can't edit the figures before they're sent to Mike. Quotes expire after 3 days. If Mastermelt's price is more than 4 days old, the page asks customers to call instead of quoting.

## Cost and safety

Each quote costs about the same as a coin scan, a fraction of a penny. The Worker only answers pages on jase6569.github.io, dorsetgoldandjewellery.co.uk and any `ALLOWED_ORIGINS`, accepts at most 4 photos, and only ever asks the one fixed question. Set a monthly budget limit on the OpenAI account in case someone hammers the page.
