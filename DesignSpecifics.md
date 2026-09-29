# Design Specifics — Novice Teacher Resource Hub

This document is the central hub and storage for shared design decisions. Update it as choices are finalized so we’re all building against the same values. Leave TBD until a decision is locked in.

Last updated: 9/25

---

## Color Palette

- Primary: Beaver Blue #1E407C
- Secondary: Nittany Navy #001E44
- Accent: Keystone #FFD100 (Pugh Blue #96BEE6 on dark backgrounds)
- Background: Cream #FBF7F1
- Surface / Card: #FFFFFF (Leo side panels #F6F3EC)
- Text — Primary: #001E44
- Text — Secondary: #4A5B6E
- Border / Divider: #E4DCCD (cards, dividers)
- Border / Input: #857D6E (form fields, 1.5px)
- Status colors (success / warning / error): success #1C5E3B, warning TBD, error #B11F33

**Notes:** (brand source, accessibility/contrast requirements, etc.)
- Penn State brand colors, entered from memory; verify against the brand guide
- Topic colors: Phonics #BC204B, Vocabulary #1E407C, Fluency #FFD100, Comprehension #491D70, Oral language #1F7A74, Writing #2F8A5B
- Never use yellow text on light backgrounds


---

## Typography

- Font family (headings): Fredoka (marketing pages + wordmark)
- Font family (body): Nunito (all body text, and all Leo screen headings)
- Font source/license: Google Fonts, free (OFL)

Per-role notes (size, weight, line height, etc. — add as needed):
- H1: 56–64px · H2: 44–48px · H3: 23–28px
- Body: 18px · Small: 14px · Buttons: 16–18px, bold

---

## Spacing & Layout

- Base unit: 4px (mostly multiples of 8)
- Scale: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96
- Max content width: 1312px (64px side margins)
- Grid: 12 columns, 24px gutters

---

## Core Components

Shared visual rules for components used across multiple pages. Add sub-points or new components as needed.

### Buttons
- Pill-shaped, Beaver Blue with solid drop shadow on marketing pages; 12px radius, no shadow on Leo screens

### Cards
- White, rounded 24px, with topic color band on library cards

### Navigation Bar
- Navy partnership bar on top, logo left, pill links centered, "Chat with Leo" button right

### Footer
- Navy with color stripe on top, white logo, 4 columns

### Form Fields (inputs, access-code field, chat input)
- Visible labels, 12px radius, #857D6E border, red border + message on error

*(Add more components here as they come up — e.g. modals, tooltips, chat bubbles, tags.)*

---

## Icons & Assets

- Icons: (TBD)
- Logo: line lion + "literacylion." wordmark 
- Favicon: lion icon tile (TBD export)

---

## Accessibility Notes

- WCAG AA; all text colors pass contrast
- Focus states: TBD
- Min 44px tap targets

---

## Change Log

- 9/25 — initial skeleton created
- 9/28 — filled in from v1 design canvas; logo locked