---
name: mortups
description: Catálogos web, menús QR y marketing para comercios que venden por WhatsApp. A light, category-standard agency site where the product demonstrates itself.
colors:
  brand-violet: "#8B2CFF"
  brand-violet-hover: "#7716F0"
  brand-violet-ink: "#6A16D9"
  brand-violet-tint: "#F4EDFF"
  selection-violet: "#E3D1FF"
  paper: "#FFFFFF"
  paper-mist: "#F7F6FA"
  paper-lilac: "#EFEDF4"
  ink: "#17141F"
  ink-soft: "#4A4558"
  ink-muted: "#6B6579"
  hairline: "rgba(23,20,31,.10)"
  hairline-strong: "rgba(23,20,31,.16)"
  wa-bubble: "#E3F7D6"
  wa-bubble-ink: "#14321F"
  wa-chat: "#F3F1EC"
  ok-green: "#1E7A4C"
typography:
  display:
    fontFamily: "Hanken Grotesk, system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "clamp(38px, 4.6vw, 60px)"
    fontWeight: 600
    lineHeight: 1.04
    letterSpacing: "-0.035em"
  headline:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "clamp(30px, 3.6vw, 44px)"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  title:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "19px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  price:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "40px"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.03em"
    fontFeature: "tnum"
  lead:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "clamp(18px, 1.6vw, 20px)"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "15px"
    fontWeight: 500
    lineHeight: 1.4
  fine:
    fontFamily: "Hanken Grotesk, system-ui, sans-serif"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  sm: "8px"
  control: "10px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  device: "28px"
  pill: "999px"
spacing:
  gutter: "clamp(16px, 4vw, 40px)"
  container: "1200px"
  section: "clamp(72px, 9vw, 128px)"
  section-inner: "clamp(56px, 7vw, 96px)"
  stack-sm: "12px"
  stack-md: "24px"
  stack-lg: "32px"
  head-gap: "48px"
components:
  button-primary:
    backgroundColor: "{colors.brand-violet}"
    textColor: "{colors.paper}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "0 24px"
    height: "52px"
  button-primary-hover:
    backgroundColor: "{colors.brand-violet-hover}"
  button-secondary:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0 24px"
    height: "52px"
  button-secondary-hover:
    backgroundColor: "{colors.paper-mist}"
  button-small:
    rounded: "{rounded.control}"
    padding: "0 16px"
    height: "40px"
  text-link:
    textColor: "{colors.brand-violet-ink}"
    typography: "{typography.label}"
  tab-selected:
    backgroundColor: "{colors.brand-violet-tint}"
    textColor: "{colors.brand-violet-ink}"
    rounded: "{rounded.control}"
    padding: "10px 14px"
  card:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.lg}"
    padding: "28px"
  plan-card:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.lg}"
    padding: "32px"
  chip:
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.pill}"
    padding: "0 12px"
    height: "30px"
  badge:
    backgroundColor: "{colors.brand-violet}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    padding: "0 10px"
    height: "26px"
  wa-bubble:
    backgroundColor: "{colors.wa-bubble}"
    textColor: "{colors.wa-bubble-ink}"
    padding: "12px 14px"
  closing-band:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
---

# Design System: mortups

## Overview

**Creative North Star: "The Working Storefront"**

mortups looks like the category standard for a light agency/SaaS site, built with Stripe-grade finish and the plain-spoken closeness of Argentine merchant tools. The product demonstrates itself: a real client catalog in a browser window, a WhatsApp order bubble with the total already summed, an interactive demo where adding products writes the message live. Ornament is replaced by evidence. Every page ends in a WhatsApp button.

The canvas is white and a barely violet-tinted mist grey, with near-black ink and 1px hairlines doing the structural work. Brand violet is a scarce signal, not an atmosphere: it marks the primary action, the wordmark, selection, and the active or linked state. Depth exists only where something is shown as an object (screenshots, the order card, the phone mockup, the demo window); everything else lies flat on the page. Density is comfortable and merchant-legible: 17px body, 52px buttons, tabular figures on every price.

This world replaced an earlier dark look with glows, emoji icons and bright violet gradients; that look is the confirmed anti-reference.

**Key Characteristics:**
- Light paper surfaces, hairline structure, tonal alternation between white and mist sections.
- One violet, used sparingly; WhatsApp green appears only inside the order bubble.
- Hanken Grotesk at 400/500/600 with tight negative tracking on headings and tabular numerals on prices.
- Hand-drawn single-stroke line icons (1.6 stroke, round caps), never glyphs or emoji.
- Shadows reserved for shown objects: screenshots, mockups, the demo, the floating order card.
- One soft hero entrance; all other motion is short color and transform transitions.

## Colors

A white-and-ink system with a single saturated violet and a quarantined WhatsApp green.

### Primary
- **Brand Violet** (brand-violet): fill of the primary button, the "ups" of the wordmark, the badge on the featured plan, the 2px border of the featured plan, the focus ring, and the small list bullets in content cards. White text on it passes AA.
- **Pressed Violet** (brand-violet-hover): hover state of the primary button only.
- **Violet Ink** (brand-violet-ink): the text-weight violet. Inline links (`Ver cómo funciona →`), solution-row icons, check icons in plan lists, step timings, selected tab and variant text, legal-page links. Use this, not Brand Violet, whenever violet is text or a thin stroke.
- **Violet Wash** (brand-violet-tint): background of the selected demo tab, selected variant, promo note, numbered step discs and highlighted notes.
- **Selection Lilac** (selection-violet): text selection background.

### Secondary
- **WhatsApp Bubble** (wa-bubble) with **Bubble Ink** (wa-bubble-ink): the outgoing-message bubble that carries an assembled order, on a **Chat Paper** (wa-chat) backdrop. These three only ever appear together, inside an order card or the demo drawer.
- **Confirm Green** (ok-green): check icons in the hero facts list and the "en línea" status in the demo chat header.

### Neutral
- **Paper** (paper): page background, cards, buttons-secondary, mockup windows.
- **Mist** (paper-mist): alternating sections, inner-page hero band, legal top bar, footer, window title bars, hover fill for rows/nav/tabs.
- **Lilac Grey** (paper-lilac): soft badge and status chip fill.
- **Ink** (ink): headings, body emphasis, the closing CTA band background, avatar discs, the pressed table-selector state.
- **Soft Ink** (ink-soft): body copy in descriptions, nav links, lead paragraphs.
- **Muted Ink** (ink-muted): metadata, fine print, breadcrumbs, table headers, placeholders.
- **Hairline** (hairline) and **Strong Hairline** (hairline-strong): every divider, card border and table rule; the strong one for control outlines (secondary button, chips, quantity steppers, search field, step discs).

### Named Rules
**The Scarce Violet Rule.** Brand Violet fills at most one primary action per viewport plus the wordmark. Everything else violet is Violet Ink text/strokes or Violet Wash fills marking a selected or linked state. No violet gradients, glows or violet section backgrounds.

**The Quarantined Green Rule.** WhatsApp green (the bubble, its ink, the chat paper) lives only inside a depicted WhatsApp conversation. WhatsApp CTAs are violet buttons with the line chat icon, not green buttons.

## Typography

**Display Font:** Hanken Grotesk (self-hosted variable woff2, 100–900, falling back to system-ui, -apple-system, Segoe UI, Roboto)
**Body Font:** Hanken Grotesk
**Label/Mono Font:** none distinct; numerals switch to tabular figures.

**Character:** One neutral grotesque carrying everything at three weights. Headings get tight negative tracking and balanced wrapping; body is set slightly large (17px) for merchants on phones.

### Hierarchy
- **Display** (600, clamp 38–60px, 1.04, -0.035em): home h1 only. Inner-page h1 uses the same treatment capped at 56px; legal h1 at 44px.
- **Headline** (600, clamp 30–44px, 1.1, -0.03em): section h2, max ~24ch on inner pages, 20ch in the closing band.
- **Title** (600, 19px, 1.3): card and row h3; scales to 21–26px for solution rows, plan names and case studies.
- **Price** (600, 40px, 1.1, -0.03em, tabular): plan prices, followed by a 15px Muted Ink period suffix.
- **Lead** (400, clamp 18–20px, 1.55, Soft Ink, max 60ch): hero and page-hero standfirst. Section subheads run 18px, max 62ch.
- **Body** (400, 17px, 1.6): running text, max 68ch in inner pages.
- **Label** (500, 14–15px): nav, buttons-small, tabs, links, chips, step timings.
- **Fine** (400, 13px, 1.6, Muted Ink): footnotes, legal top bar, metadata.

### Named Rules
**The Three Weights Rule.** Only 400, 500 and 600. No bold 700+, no light weights, no second family.

**The Counted Figures Rule.** Every price, quantity, total, step number and table cell uses tabular numerals.

**The Sentence Case Rule.** No uppercase letter-spaced labels anywhere; section heads open directly on the h2.

## Layout

A 1200px centered container with a fluid gutter (16px on phones, up to 40px). Sections breathe on a fluid vertical rhythm (72–128px on the home, 56–96px on inner pages) and alternate Paper and Mist backgrounds; on inner pages consecutive white sections are separated by a hairline instead. Section heads sit left-aligned at max 720px with a 48px gap before content; centered heads are the exception.

The home hero is an asymmetric two-column grid (≈1.12fr text, 1fr stage) where the screenshot window intentionally bleeds 18% past its column and the order card overlaps its lower-left edge; below 960px it stacks text, buttons, then the window with the order card pulled up over its bottom edge. Lists of offerings are hairline tables rather than card grids: solution rows (icon, title, description, link), a 5-up bordered directory of rubros (3-up under 1040px, 2-up under 640px), and a two-column ruled grid for digital products. Card grids (3-up, or 2×2 when exactly four) are used for plans and inner-page content boxes. The process is a numbered 4-step track joined by a horizontal hairline that turns vertical on mobile. FAQ is a two-column layout with a sticky h2.

Breakpoints observed: 960px (nav collapses to menu, hero and plans stack, floating WhatsApp button appears), 900px, 860px, 800px, 760px, 640px, 560px (full-width action buttons, single-column facts).

## Elevation & Depth

Flat by default, with two neutral ink-tinted shadows reserved for objects being shown. Sections, rows, cards and plans are separated by hairlines and tonal backgrounds, not shadows. The large shadow sits under screenshot windows, the hero order card, the demo window, the phone mockup and the open mobile menu panel. The small shadow marks the featured plan and the WhatsApp bubble in inner-page mockups.

### Shadow Vocabulary
- **Object Lift** (`box-shadow: 0 2px 4px rgba(23,20,31,.05), 0 24px 56px -16px rgba(23,20,31,.22)`): screenshots, mockups, demo, order card, menu panel.
- **Quiet Lift** (`box-shadow: 0 1px 2px rgba(23,20,31,.06), 0 8px 24px -8px rgba(23,20,31,.14)`): featured plan, inner-page bubble.
- **Floating Action** (`box-shadow: 0 8px 24px -6px rgba(23,20,31,.35)`): mobile floating WhatsApp button only.

### Named Rules
**The Shown-Object Rule.** A shadow means "this is a thing you are looking at" (a window, a phone, a message). Content cards and sections never take one. No colored shadows, no glows, no hard offset shadows.

## Shapes

Gently rounded and consistent: 8px for small chrome (nav items, legal bar items), 10px for controls (small buttons, tabs, search, steppers, promo), 12px for primary buttons and notes, 16px for cards, plans, windows and the order card, 24px for the demo and mockup stage, 28px for the phone body, and full pills for chips, badges and status. Borders are 1px hairlines everywhere; the only 2px border is the featured plan. Screenshots are framed in a browser window: a Mist title bar with three soft grey dots and a URL pill. Message bubbles have a tucked corner (12px 12px 4px 12px). Numbered steps use 36px hairline circles.

## Components

### Buttons
Solid and calm; they read as the one thing to press.
- **Shape:** gently rounded (12px), 52px tall, 24px side padding, 17px weight 500, 10px gap for a leading line icon.
- **Primary:** Brand Violet fill, white text. Hover darkens to Pressed Violet; active nudges down 1px. All WhatsApp CTAs are primary and carry the chat-bubble line icon.
- **Secondary:** Paper fill, Ink text, Strong Hairline border; hover to Mist. Inside the dark closing band it inverts to a white fill.
- **Small:** 40px tall, 16px padding, 10px radius, 15px text (header CTA).
- **Focus:** 2px Brand Violet outline, 3px offset.
- **Floating (mobile):** a pill-shaped primary button fixed bottom-right under 960px, with the Floating Action shadow.

### Text links
Violet Ink, weight 500, followed by a 16px arrow icon that shifts 2px right on hover; underline appears on hover. Neutral links (footer, legal bar, breadcrumbs) are Soft Ink and darken to Ink with underline.

### Chips / Badges
- **Tags:** 30px pills, Strong Hairline border, Soft Ink 14px text (case-study capabilities).
- **Badge:** 26px pill, Brand Violet with white text for "Más elegido"; a soft variant uses Lilac Grey with Soft Ink.
- **Pill counters:** 32px Mist pills in the demo (cart count).

### Cards / Containers
- **Corner Style:** 16px.
- **Background:** Paper, on Mist or Paper sections.
- **Shadow Strategy:** none (see The Shown-Object Rule); the featured plan alone gets Quiet Lift plus a 2px violet border.
- **Border:** 1px Hairline.
- **Internal Padding:** 28px (content boxes), 32px (plans), 28px 32px (entry offer strip).
- Plans list features below a hairline with Violet Ink check icons and end in a full-width button pushed to the bottom.

### Inputs / Fields
- **Style:** 40px search field, Strong Hairline border, 10px radius, leading Muted Ink icon.
- **Focus:** border turns Brand Violet with a 3px violet ring at 15% opacity.
- **Steppers:** joined minus/count/plus group in a 10px hairline box; variant buttons are 28px hairline chips that turn Violet Wash with Violet Ink border when selected.

### Navigation
Sticky 68px header on 92% white with backdrop blur and a hairline bottom. Wordmark "mortups" at 24px weight 600, -0.04em, with "ups" in Brand Violet. Nav items are 15px Soft Ink in 8px-radius hit areas that fill Mist on hover or current page. Above it, a 36px Mist legal bar with right-aligned 13px links (arrepentimiento, baja). Under 960px the nav collapses into a 44px hairline square button opening a 16px-radius panel with Object Lift.

### Signature: Browser window frame
Every product screenshot sits in a Paper window with 16px radius, a 40px Mist title bar, three 10px grey dots and a hairline URL pill naming the client site. Pure-CSS variant for case pages draws the dots with gradients.

### Signature: WhatsApp order card
A card with an ink avatar disc and "Pedido nuevo" header over Chat Paper, holding a WhatsApp Bubble with line items and a tabular total separated by a hairline, plus a time stamp and blue double-check. It is the system's proof device and appears in the hero, the demo drawer (where it fills live) and inner-page phone mockups.

### Signature: Interactive demo
A 24px-radius window with a scrollable row of rubro tabs (selected tab in Violet Wash), a product list with steppers on the left and a 340px WhatsApp drawer on the right that writes the order as products are added; the empty state is a dashed hairline outline. Stacks under 900px.

## Do's and Don'ts

### Do:
- **Do** keep the canvas Paper and Mist with Ink text; separate with 1px hairlines (rgba(23,20,31,.10)).
- **Do** use Brand Violet (#8B2CFF) for the primary button, wordmark and focus ring, and Violet Ink (#6A16D9) whenever violet is text or a thin stroke.
- **Do** show the product: frame screenshots in the browser window and prove claims with the WhatsApp order card.
- **Do** draw icons as single-stroke 24px line SVGs (stroke 1.6, round caps and joins) colored by currentColor.
- **Do** set prices and quantities in tabular figures, with the period suffix in Muted Ink.
- **Do** end every page in the Ink closing band with a primary WhatsApp button.
- **Do** keep motion to one soft hero entrance (16px rise, 0.8s, ease cubic-bezier(.16,1,.3,1)) and 0.2s color/transform transitions; honor reduced motion.

### Don't:
- **Don't** use violet gradients, glows, neon accents or dark-mode-by-default surfaces; that is the replaced look.
- **Don't** use emoji or text glyphs as icons.
- **Don't** add uppercase letter-spaced labels or eyebrow text above headings.
- **Don't** put shadows on content cards or sections; shadows belong to shown objects.
- **Don't** use WhatsApp green outside a depicted conversation, or for buttons.
- **Don't** introduce a second typeface, weights outside 400/500/600, or third-party hosted fonts.
