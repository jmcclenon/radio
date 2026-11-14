# Lion's Den — Agensi marketplace plan

Status: **proposal / not listed on Agensi**. This repository hosts a prototype radio-discovery skill; no paid product has been published.

## Positioning

There are two different audiences:

1. **Listener:** Lion's Den Radio Finder (free). A usable discovery skill that sends people to the free, public web player. Market it as finding stations from simple questions, **not** as remote-controlled playback.
2. **Builder:** Lion's Den Radio Builder (proposed **$29 one-time**). A *separate, original skill not yet built* for developers who want to implement an internet-radio website, with accessibility, legal-compliance guidance, templates, tests, and deployment workflows. Do not simply repackage the publicly available `index.html`.

Suggested listener listing title: **Lion's Den Radio Finder — Discover Reggae, Jazz & More**

Suggested summary: **Find live internet radio stations by genre and country, then listen through Lion's Den's free browser player. No account required.**

Suggested example prompts:
- "Find roots reggae from Jamaica."
- "Suggest relaxing jazz radio stations."
- "Where can I hear classical music tonight?"
- "Find ambient radio I can listen to before bed."

## Marketplace workflow

- Verify the `SKILL.md` performs its claims using a compatible agent.
- Bundle its text files as the one-skill ZIP required by Agensi.
- Choose **Free** for the listener skill.
- Set up Creator Mode and a verified payout method for any paid listing.
- Add a short demo showing a query, actual candidate stations, and a *user-initiated* browser listen.
- Submit for security review before declaring it live.
- Agensi supports text-based SKILL.md skill packages, not hosted app/MCP servers.

## Distribution

Use the existing GitHub Pages site for discovery and listening. Distribute the optional skill via Agensi and link the skill listing from the public site **after approval**, with no claim that agents can automatically control browser playback. Promote concrete use cases rather than AI jargon on social platforms and through short videos. Avoid unsubstantiated user or uptime claims.

## Validation metrics

Record discovery-to-listen clicks, skill views and uses, returning listeners, actual playback error rate, and (for a future paid builder) listing conversion, refunds, and support load. Respect privacy; prefer aggregate counts and avoid collecting listening history without consent.

## License and stream restrictions

The application contains station directory information and third-party URLs; it does not own the underlying musical works, recordings, station marks, or public-safety audio. Check the relevant streaming providers' policies before promoting commercial distribution. Broadcastify live-audio APIs may require an agreement and are out of scope. Respect Radio Browser's public-service policies. Paid builder templates must consist of original or properly licensed material.
