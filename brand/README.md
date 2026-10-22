# Vector Translation brand kit

The mark is Leonardo's octahedron from Luca Pacioli's *De divina proportione* (1509), the source of the Vector Humanities rhombicuboctahedron, drawn twice as a wireframe. The source copy is pale ink. The translated copy, displaced by a vector, is electric blue, with visible edges (those bordering a face turned to the eye) bold and hidden edges thin and pale. A vermilion arrow joins the top vertex of the source copy to the top vertex of the translated copy. The view is turned 15° and seen 22° from above; the Vector Humanities mark's 23° makes the octahedron read as a kite.

On the site the two solids turn slowly about the vertical axis. The top vertex lies on that axis, so the arrow holds still.

| File | Use |
|:--|:--|
| `mark-full-*.svg` | 80 px and up: every edge of both copies, hidden edges thin and pale |
| `mark-front-*.svg` | 28 to 80 px: visible edges only |
| `mark-icon-*.svg` | 16 to 28 px: outlines only, heavier strokes |
| `favicon.svg` (also `../assets/favicon.svg`) | icon level, follows the browser's light or dark scheme |
| `avatar.svg`, `avatar-1024.png` | repository or organisation avatar |
| `social-card.svg`, `social-card-1200x630.png` | link previews (`og:image`) |

Grounds: `paper` (#f6f2e9, beams #1a1aff, source ink #141518 at low strength), `night` (#0c0e1c, beams #8a90ff), `electric` (#1a1aff, beams white). Vermilion #ff4a24 (#ff6a45 on dark grounds). Type: Cormorant Garamond 600 caps, tracked, for the wordmark VECTOR TRANSLATION; IBM Plex Mono for the line "a Vector Humanities method"; Source Serif 4 for text.

`src/mark.py` writes the SVGs, the favicon, the avatar and card SVGs, the header mark used inline in `index.html` (`src/header-mark.txt`, coloured by the `.mk` classes in `assets/style.css`) and a contact sheet (`src/sheet.html`):

```bash
python3 brand/src/mark.py brand assets
```

The PNGs are screenshots of the avatar and card SVGs taken in headless Chrome at their native sizes.
