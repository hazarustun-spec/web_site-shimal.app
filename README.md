# Shimal website

Static website for shimal.app, hosted by the existing GitHub Pages repository.

- `index.html`: all currently published apps.
- The home page also lists Shimal, Bring Light, marker., and drappin under “Coming soon”, linked to their existing pages.
- `zoo-merge/`, `challengebu/`, `cekim-yasasi-bolluk/`: individual app pages.
- `support/`: links to every existing app and its legal documents.
- `assets/site.css`: Helvetica, black, white, and #2626F5.
- `assets/gallery.js`: screenshot navigation and accessible enlarged previews.
- `assets/app-store-manifest.json`: verified Apple listing IDs, source URLs, asset hashes, and verification date. The iOS and Mac listings were checked for Turkey and the US; the account currently lists three iPhone apps and no separate Mac apps.

The 3 icons and 22 screenshots in `assets/apps/` are downloaded from their matching App Store listings. Screenshots retain the original store order and aspect ratio. Store screenshots in Turkish remain in Turkish.

## Edit and preview

Editorial text and templates live in `scripts/build_site.py`. Run `python3 scripts/build_site.py` after editing. The generated HTML is committed directly; GitHub Pages needs no build step or server-side runtime.

Run `python3 -m http.server 4173 --bind 127.0.0.1` in this folder for local preview.

Run `python3 scripts/verify_site.py` to check links, anchors, catalogue completeness, and image integrity (Pillow required for image verification).

Existing privacy policies, KVKK documents, terms, redirects, other app pages, CNAME, and app-ads.txt are retained. The build script only writes the main catalogue, the three published app landing pages, and the support directory. It never rewrites legal documents.
