# Universal Tool Design OS  
## Vollständige, basislose Design-System-Vorgabe für lokale Canvas-, Editor-, Builder- und Workflow-Tools

**Version:** 1.0  
**Zweck:** Ein universelles Design-OS, das ohne vorhandene Basisdatei funktioniert und auf unterschiedliche Tooltypen angewendet werden kann.  
**Sprache:** HTML, CSS, JavaScript, optional React/Figma/Penpot-Übertragung  
**Designrichtung:** ruhig, präzise, canvas-first, editorial-minimal, Apple-artig, lokal-produktionsfähig, barrierearm, nicht generisch SaaS.

---

# 0. Grundannahme: Es gibt keine Basis

Dieses Dokument geht davon aus, dass kein bestehendes Designsystem, keine CSS-Datei, keine Komponentenbibliothek und keine UI-Architektur vorhanden ist.

Das bedeutet:

- Alle Tokens werden von Grund auf definiert.
- Alle Komponentenregeln sind vollständig beschrieben.
- Alle Interaktionsregeln sind explizit.
- Alle optionalen Module sind markiert.
- Nicht jedes Tool muss alle Features enthalten.
- Das System ist modular: ein kleines Tool nutzt nur den Kern, ein komplexes Editor-Tool nutzt zusätzliche Module.

Das Ziel ist nicht, jede Anwendung identisch aussehen zu lassen, sondern alle Tools nach derselben **visuellen, typografischen, strukturellen und interaktiven Logik** aufzubauen.

---

# 1. Design-OS-Prinzip

Das Design-OS ist für produktive, lokale oder interne Tools gedacht:

- Canvas-Tools
- Flow-Builder
- Icon-Builder
- Invoice-Tools
- Brief-Builder
- Timeline-Tools
- Product-Design-Engines
- Formulare mit generiertem Output
- visuelle Editoren
- lokale Prototyping-Tools

Es ist **kein** klassisches SaaS-Dashboard-System.

## 1.1 Grundlogik

```txt
Left Sidebar      = creation, settings, actions
Center Canvas     = working area, preview, document, editor
Right Inspector   = optional, only for context or selected object details
Floating Header   = global state, view modes, zoom, export, theme
Popover/Menu      = local contextual actions
Cards/Nodes       = editable work objects
Sockets/Handles   = relation and connection points
```

## 1.2 Designhaltung

Pflicht:

- ruhig
- präzise
- nicht verspielt
- nicht generisch
- keine starken Gradients
- keine großen farbigen SaaS-Flächen
- keine übertriebene Animation
- keine dekorativen Icons ohne Funktion
- Text muss scharf bleiben
- Auswahlzustände müssen sichtbar, aber nicht laut sein
- Tools sollen sich professionell und intern-produktiv anfühlen

---

# 2. Modulares Anwendungsmodell

Nicht alle Tools brauchen alle Module.

## 2.1 Tool-Typen

| Tooltyp | Muss haben | Optional | Nicht nötig |
|---|---|---|---|
| Canvas Editor | Sidebar, Canvas, Zoom, Pan, Selection, Export | Inspector, Shortcuts, Autosave | lange Formularstrecken |
| Flow Builder | Nodes, Connections, Sockets, Drag, Autosave | Multi-Edges, JSON Import, SVG Export | komplexe Tabellen |
| Brief/Form Tool | Fragen, Inputs, Output, Export | Staged Views, Progress | Canvas-Pan/Zoom |
| Invoice Tool | Dokumentpreview, Form Inputs, PDF Export | Currency Toggle, Language Toggle | Node Connections |
| Timeline Tool | Timeline Axis, Cards, States | Filters, Detail Inspector | Freeform Drag |
| Icon Tool | Grid, Shapes, Keylines, Export | Pixel Preview, Quality Check | Long Text Editing |
| Product Engine | Staged Questions, Output Generation | CAD/Test Sections | Free Canvas |

## 2.2 Kernmodule

Jedes Tool nutzt mindestens:

```txt
1. Color Tokens
2. Typography Tokens
3. Spacing Tokens
4. Radius Tokens
5. Interaction States
6. Focus System
7. Light/Dark Theme
8. Export/Save Logic, falls Userdaten entstehen
```

## 2.3 Erweiterungsmodule

Nur wenn relevant:

```txt
Canvas Module
Zoom Module
Node Module
Socket/Connection Module
Inspector Module
Popover Module
Command Palette Module
Library Module
Quality Checker Module
```

---

# 3. Token-Architektur

Ein skalierbares Design-OS trennt drei Ebenen:

```txt
Primitive Tokens  = rohe Werte
Semantic Tokens   = Bedeutung
Component Tokens  = konkrete Anwendung
```

## 3.1 Primitive Tokens

Beispiel:

```css
:root{
  --primitive-white: #FFFFFF;
  --primitive-black: #000000;

  --primitive-gray-50:  #F9F9FA;
  --primitive-gray-100: #F2F2F7;
  --primitive-gray-200: #E5E5EA;
  --primitive-gray-300: #D1D1D6;
  --primitive-gray-400: #C7C7CC;
  --primitive-gray-500: #8E8E93;
  --primitive-gray-600: #636366;
  --primitive-gray-700: #48484A;
  --primitive-gray-800: #2C2C2E;
  --primitive-gray-900: #1C1C1E;
  --primitive-gray-950: #0C0C0E;

  --primitive-blue-500: #0A84FF;
  --primitive-green-500: #32D74B;
  --primitive-yellow-500: #FFD60A;
  --primitive-orange-500: #FF9F0A;
  --primitive-red-500: #FF453A;
  --primitive-purple-500: #BF5AF2;
  --primitive-cyan-500: #64D2FF;
  --primitive-pink-500: #FF2D55;
}
```

## 3.2 Semantic Tokens

Diese Werte werden in Komponenten benutzt, nicht die Primitive direkt.

```css
:root{
  --color-bg-page: var(--primitive-gray-100);
  --color-bg-canvas: var(--primitive-gray-100);
  --color-bg-surface: rgba(255,255,255,.82);
  --color-bg-surface-strong: #FFFFFF;

  --color-glass: rgba(255,255,255,.72);
  --color-glass-border: rgba(0,0,0,.06);

  --color-sidebar-bg: rgba(255,255,255,.30);
  --color-sidebar-border: rgba(0,0,0,.04);

  --color-text-primary: rgba(0,0,0,.96);
  --color-text-secondary: rgba(42,42,45,.76);
  --color-text-muted: rgba(42,42,45,.70);
  --color-text-tertiary: rgba(42,42,45,.62);

  --color-action-active: rgba(0,0,0,.06);
  --color-field-bg: rgba(0,0,0,.048);
  --color-field-bg-hover: rgba(0,0,0,.072);
  --color-field-border: rgba(0,0,0,.10);

  --color-focus: #005FCC;

  --color-success: var(--primitive-green-500);
  --color-warning: var(--primitive-orange-500);
  --color-error: var(--primitive-red-500);
  --color-info: var(--primitive-blue-500);
}
```

## 3.3 Dark Theme Mapping

```css
html[data-theme="dark"]{
  --color-bg-page: var(--primitive-gray-900);
  --color-bg-canvas: var(--primitive-gray-900);
  --color-bg-surface: rgba(36,36,38,.78);
  --color-bg-surface-strong: #2C2C2E;

  --color-glass: rgba(30,30,32,.40);
  --color-glass-border: rgba(255,255,255,.12);

  --color-sidebar-bg: rgba(40,40,40,.40);
  --color-sidebar-border: rgba(255,255,255,.05);

  --color-text-primary: rgba(255,255,255,.96);
  --color-text-secondary: rgba(235,235,245,.76);
  --color-text-muted: rgba(235,235,245,.68);
  --color-text-tertiary: rgba(235,235,245,.60);

  --color-action-active: rgba(255,255,255,.10);
  --color-field-bg: rgba(255,255,255,.065);
  --color-field-bg-hover: rgba(255,255,255,.10);
  --color-field-border: rgba(255,255,255,.15);

  --color-focus: #64D2FF;
}
```

## 3.4 Component Tokens

```css
:root{
  --button-bg: transparent;
  --button-bg-hover: var(--color-action-active);
  --button-text: var(--color-text-secondary);
  --button-text-hover: var(--color-text-primary);
  --button-radius: 8px;
  --button-height: 44px;

  --card-bg: var(--color-bg-surface-strong);
  --card-border: var(--color-glass-border);
  --card-radius: 24px;
  --card-padding: 20px;
  --card-shadow: 0 10px 34px rgba(0,0,0,.07);

  --popover-bg: var(--color-glass);
  --popover-border: var(--color-glass-border);
  --popover-radius: 18px;
  --popover-shadow: 0 18px 52px rgba(0,0,0,.18);

  --focus-ring-width: 2px;
  --focus-ring-offset: 2px;
  --focus-ring-color: var(--color-focus);
}
```

---

# 4. Color System

## 4.1 Farbrollen

| Rolle | Zweck | Regel |
|---|---|---|
| Page Background | App-Grundfläche | neutral, nie gelblich |
| Canvas Background | Arbeitsfläche | ruhig, textschonend |
| Surface | Cards, Panels | leicht kontrastierend |
| Glass | Floating Header, Popovers | transparent + blur |
| Border | Trennung | 0.5px bis 1px, sehr subtil |
| Text Primary | Haupttext | hoher Kontrast |
| Text Secondary | UI-Labels | noch AA-tauglich |
| Text Tertiary | Meta | sparsam, nicht für wichtige Infos |
| Accent | Fokus/Status | nicht überall einsetzen |
| Object Color | Node/Card/Bullet/Connection | objektbezogen |

## 4.2 Farbe darf keine alleinige Information sein

Schlecht:

```txt
grün = fertig
rot = Fehler
```

Besser:

```txt
grün + Check Icon + Text "Done"
rot + Fehlertext + Icon
```

## 4.3 Statusfarben

```css
:root{
  --status-success: #32D74B;
  --status-warning: #FF9F0A;
  --status-error: #FF453A;
  --status-info: #0A84FF;
  --status-neutral: #8E8E93;
}
```

---

# 5. Typography System

## 5.1 Font Stack

```css
:root{
  --font-sans:
    -apple-system,
    BlinkMacSystemFont,
    "SF Pro Display",
    "SF Pro Text",
    "Helvetica Neue",
    Arial,
    sans-serif;

  --font-mono:
    ui-monospace,
    SFMono-Regular,
    Menlo,
    Monaco,
    Consolas,
    monospace;
}
```

## 5.2 Global Font Rendering

```css
*{
  -webkit-font-smoothing: antialiased;
  text-rendering: auto;
  font-kerning: normal;
  font-feature-settings: "kern" 1;
}
```

Nicht verwenden:

```css
text-rendering: geometricPrecision;
```

Das kann in UI-Tools unruhig und spacing-artig wirken.

## 5.3 Typografie-Skala

```css
:root{
  --font-size-xxs: 11px;
  --font-size-xs: 12px;
  --font-size-sm: 13px;
  --font-size-md: 14px;
  --font-size-base: 15px;
  --font-size-lg: 16px;
  --font-size-xl: 17px;
  --font-size-2xl: 20px;
  --font-size-3xl: 28px;
  --font-size-4xl: 34px;

  --line-height-tight: 1.1;
  --line-height-heading: 1.2;
  --line-height-ui: 1.35;
  --line-height-body: 1.46;
  --line-height-long: 1.55;

  --font-weight-regular: 400;
  --font-weight-ui: 430;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
}
```

## 5.4 Typografie-Regeln

- Card-Titel nicht überfetten.
- Fließtext mindestens 14px.
- Wichtiger UI-Text mindestens 13px.
- 11–12px nur für Metadaten, nicht für wichtige Eingaben.
- Letterspacing fast immer `0`.
- Negative Laufweite nur sehr sparsam bei großen Headlines.

## 5.5 Empfohlene Zuordnung

```css
.tool-title{
  font-size:17px;
  line-height:1;
  font-weight:600;
  letter-spacing:-.02em;
}

.panel-title{
  font-size:14px;
  line-height:1.2;
  font-weight:500;
  letter-spacing:-.01em;
}

.glass-chip{
  font-size:13px;
  line-height:1;
  font-weight:500;
  letter-spacing:-.01em;
}

.node-title{
  font-size:16px;
  line-height:1.26;
  font-weight:470;
  letter-spacing:0;
}

.cell-label{
  font-size:13px;
  line-height:1.36;
  font-weight:360;
  letter-spacing:0;
}

.cell-value{
  font-size:14px;
  line-height:1.46;
  font-weight:380;
  letter-spacing:0;
}
```

---

# 6. Spacing System

## 6.1 Base Grid

Das System nutzt ein 4px-Mikroraster und ein 8px-Major-Raster.

```css
:root{
  --space-1: 4px;
  --space-2: 6px;
  --space-3: 8px;
  --space-4: 10px;
  --space-5: 12px;
  --space-6: 14px;
  --space-7: 16px;
  --space-8: 18px;
  --space-9: 20px;
  --space-10: 24px;
  --space-11: 32px;
  --space-12: 40px;
  --space-13: 48px;
}
```

## 6.2 Anwendung

| Token | Anwendung |
|---|---|
| 4px | Button-Gruppen, compact gaps |
| 6px | Sidebar Row Gap |
| 8px | Pill gap, small groups |
| 10px | Icon/Text gap |
| 12px | Sidebar horizontal padding |
| 14px | Card row gap |
| 18px | Floating Header offset |
| 20px | Card padding |
| 24px | Card radius / large section gap |
| 32px | Layout rhythm |
| 44px | minimum interaction target |

---

# 7. Layout System

## 7.1 App Shell

Standard für Canvas-Tools:

```css
.app{
  display:grid;
  grid-template-columns:300px minmax(0,1fr);
  width:100vw;
  height:100dvh;
  min-height:0;
  overflow:hidden;
}
```

Mit Inspector:

```css
.app.with-inspector{
  grid-template-columns:300px minmax(0,1fr) 320px;
}
```

## 7.2 Sidebar

```css
.sidebar{
  min-height:0;
  overflow:auto;
  padding:20px 12px;
  background:var(--color-sidebar-bg);
  backdrop-filter:blur(40px) saturate(180%);
  -webkit-backdrop-filter:blur(40px) saturate(180%);
  border-right:.5px solid var(--color-sidebar-border);
}
```

Regeln:

- Sidebar enthält Creation und Settings.
- Kein übermäßiger Text.
- Keine schweren Cards.
- Panels sind Sektionen, nicht visuelle Container.

## 7.3 Canvas

```css
.canvas{
  position:relative;
  min-width:0;
  min-height:0;
  overflow:hidden;
  background:var(--color-bg-canvas);
}
```

Regeln:

- Canvas ist die Hauptfläche.
- Keine Scrollbars sichtbar, außer Tool braucht Dokumentscroll.
- Pan/Zoom nur bei Canvas-Tools.
- Text muss auch beim Zoom scharf bleiben.

## 7.4 Floating Header

```css
.floating-header{
  position:fixed;
  top:18px;
  left:calc(300px + ((100vw - 300px) / 2));
  transform:translateX(-50%);
  z-index:var(--z-floating-header);
  display:flex;
  align-items:center;
  gap:10px;
  min-height:52px;
  padding:6px;
  border-radius:9999px;
  background:var(--color-glass);
  border:.5px solid var(--color-glass-border);
  backdrop-filter:blur(24px) saturate(150%);
  -webkit-backdrop-filter:blur(24px) saturate(150%);
  box-shadow:var(--shadow-floating);
}
```

Regeln:

- Enthält globalen Zustand.
- Nicht mit Primary Actions überladen.
- Export, Theme, Zoom und View-Switch sind erlaubt.
- Detaileinstellungen gehören in Sidebar/Inspector.

---

# 8. Radius System

```css
:root{
  --radius-xs: 6px;
  --radius-sm: 8px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 18px;
  --radius-2xl: 24px;
  --radius-3xl: 28px;
  --radius-pill: 9999px;
}
```

Anwendung:

| Radius | Anwendung |
|---|---|
| 6px | text focus, tiny controls |
| 8px | buttons, compact rows |
| 10px | fields, custom select |
| 14px | small panels/cards |
| 18px | popovers |
| 24px | Bento cards |
| 28px | canvas stage |
| pill | header, chips, sockets |

---

# 9. Shadows / Elevation

```css
:root{
  --shadow-card: 0 10px 34px rgba(0,0,0,.07);
  --shadow-card-selected: 0 14px 40px rgba(0,0,0,.105);
  --shadow-floating: 0 8px 32px rgba(0,0,0,.20);
  --shadow-popover: 0 18px 52px rgba(0,0,0,.18);
  --shadow-drag: 0 18px 48px rgba(0,0,0,.14);
}
```

Regeln:

- Shadows weich, nicht hart.
- Selection nicht durch starken Glow lösen.
- Popovers dürfen stärker schweben.
- Cards beim Drag nicht skalieren.

---

# 10. Glass / Blur

## 10.1 Glass Surface

```css
.glass{
  background:var(--color-glass);
  border:.5px solid var(--color-glass-border);
  backdrop-filter:blur(24px) saturate(150%);
  -webkit-backdrop-filter:blur(24px) saturate(150%);
}
```

## 10.2 Wann Glass erlaubt ist

Erlaubt:

- Floating Header
- Popovers
- Toasts
- Sidebar
- Context Menus

Nicht verwenden:

- auf jeder Card
- für lange Textflächen
- auf bewegten großen Bereichen, wenn Performance leidet

---

# 11. Z-Index System

Ein fixes Stacking-System verhindert Chaos.

```css
:root{
  --z-base: 0;
  --z-canvas: 1;
  --z-nodes: 10;
  --z-edges: 5;
  --z-guides: 20;
  --z-selected: 30;
  --z-floating-header: 50;
  --z-sidebar: 60;
  --z-popover: 100;
  --z-dropdown: 120;
  --z-toast: 200;
  --z-modal-backdrop: 900;
  --z-modal: 1000;
  --z-system-critical: 9999;
}
```

Regeln:

- Dropdowns immer über Sidebar.
- Popovers über Canvas und Nodes.
- Toast über allem außer Modal.
- Keine zufälligen z-index-Werte wie `999999`, außer System-Critical.

---

# 12. Component System

## 12.1 Buttons

```css
.button,
.chip,
.seg{
  min-height:44px;
  border:0;
  border-radius:8px;
  padding:0 12px;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  background:transparent;
  color:var(--color-text-secondary);
  font-size:14px;
  font-weight:430;
  letter-spacing:0;
  cursor:pointer;
  transition:
    background var(--motion-time) var(--motion-ease),
    color var(--motion-time) var(--motion-ease),
    transform 120ms ease;
}

.button:hover,
.chip:hover,
.seg:hover{
  background:var(--color-action-active);
  color:var(--color-text-primary);
}

.button:active,
.chip:active,
.seg:active{
  transform:scale(.97);
}

.button.active,
.chip.active,
.seg.active{
  background:var(--color-action-active);
  color:var(--color-text-primary);
}
```

Regeln:

- Kein natives Button-Styling.
- Keine starken farbigen Primary Buttons im Tool-Chrome.
- Active State = ruhige Pill-Fläche.

## 12.2 Fields

```css
input,
textarea,
select,
.field{
  min-height:44px;
  border:.5px solid var(--color-field-border);
  border-radius:10px;
  background:var(--color-field-bg);
  color:var(--color-text-primary);
  font-size:14px;
  font-weight:430;
}
```

Regeln:

- Labels immer sichtbar.
- Placeholder nie als einziges Label.
- Fehler direkt am Feld.
- Custom Dropdown statt hässlicher nativer Select-Menüs, wenn visuelles OS wichtig ist.

## 12.3 Cards / Nodes

```css
.node{
  position:absolute;
  width:320px;
  min-height:146px;
  border-radius:24px;
  background:var(--color-bg-surface-strong);
  border:1px solid var(--color-glass-border);
  box-shadow:var(--shadow-card);
  overflow:visible;
  transform:translate3d(var(--x),var(--y),0);
  touch-action:none;
  cursor:default;
}

.node-inner{
  padding:20px;
}

.node.selected{
  border-color:color-mix(in srgb,var(--node-color) 34%,var(--color-glass-border));
  box-shadow:
    var(--shadow-card-selected),
    0 0 0 1px color-mix(in srgb,var(--node-color) 10%,transparent);
}
```

Regeln:

- Keine Bottom Lines.
- Keine Progress-Footer-Linien, außer Tool ist explizit Progress-orientiert.
- Card wächst mit Text.
- Text darf nicht abgeschnitten werden, wenn Bearbeitung erwartet wird.

## 12.4 Rows / Bulletpoints

```css
.row-node{
  display:grid;
  grid-template-columns:minmax(76px,.72fr) minmax(0,1.28fr);
  gap:14px;
  align-items:start;
}

.cell-label{
  font-size:13px;
  line-height:1.36;
  font-weight:360;
  color:var(--color-text-muted);
}

.cell-value{
  font-size:14px;
  line-height:1.46;
  font-weight:380;
  color:var(--color-text-primary);
  white-space:normal;
  overflow:visible;
  word-break:break-word;
}
```

Regeln:

- Bullet values wachsen.
- Keine Ellipsis bei editierbaren Notes.
- Labels und Values können editierbar sein.
- Bullet-Farbe pro Row möglich.

## 12.5 Sockets

```css
.port{
  position:absolute;
  width:44px;
  height:44px;
  border-radius:999px;
  display:grid;
  place-items:center;
  background:transparent;
  border:0;
}

.port::before{
  content:"";
  width:14px;
  height:14px;
  border-radius:50%;
  background:var(--color-bg-canvas);
  border:2px solid var(--node-color);
  box-shadow:
    0 3px 10px rgba(0,0,0,.12),
    0 0 0 4px var(--color-bg-surface-strong);
}

.port.out{
  right:-22px;
  top:50%;
  transform:translateY(-50%);
}

.port.in{
  left:-22px;
  top:50%;
  transform:translateY(-50%);
}
```

Regeln:

- Visuell klein, Hit-Area groß.
- Farbe folgt Node-Farbe.
- Connections gehen aus Sockets, nicht aus Boxmitte.
- Multi-connections sind erlaubt.

## 12.6 Popover

```css
.popover{
  position:fixed;
  z-index:var(--z-popover);
  padding:6px;
  border-radius:18px;
  background:var(--color-glass);
  border:.5px solid var(--color-glass-border);
  box-shadow:var(--shadow-popover);
  backdrop-filter:blur(24px) saturate(150%);
  opacity:0;
  pointer-events:none;
  transform:translateY(6px) scale(.98);
  transition:
    opacity 180ms ease,
    transform var(--motion-time) var(--motion-ease);
}

.popover.open{
  opacity:1;
  pointer-events:auto;
  transform:translateY(0) scale(1);
}
```

Regeln:

- Position immer collision-aware.
- Close bei Escape.
- Close bei Outside Click.
- Trigger bekommt `aria-expanded`.

---

# 13. Iconography

## 13.1 SVG-Regeln

```txt
viewBox: 0 0 24 24
stroke: currentColor
fill: none, außer Solid Icons
stroke-width: 1.6 bis 1.9
stroke-linecap: round
stroke-linejoin: round
```

Beispiel:

```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <path d="M..." />
</svg>
```

## 13.2 Icon-Größen

```css
:root{
  --icon-xs: 12px;
  --icon-sm: 16px;
  --icon-md: 20px;
  --icon-lg: 24px;
}
```

## 13.3 Regeln

- Icons nicht als Dekoration aufblasen.
- Icon-Buttons immer min. 44px Hit-Area.
- Icons in Buttons: 16–20px.
- Drei-Punkte-Menü nie als Text `•••`, sondern SVG.
- Icons über `currentColor` einfärben.

---

# 14. Motion System

```css
:root{
  --motion-ease: cubic-bezier(.22,1,.36,1);
  --motion-time: 320ms;
  --motion-fast: 120ms;
  --motion-medium: 220ms;
  --motion-slow: 520ms;
}
```

Spring-Fallback:

```css
@supports (animation-timing-function:linear(0,1)){
  :root{
    --motion-ease: linear(0,0.06,0.25,0.55,0.81,0.98,1.05,1.07,1.05,1);
    --motion-time: 520ms;
  }
}
```

## 14.1 Regeln

Erlaubt:

- Button press scale `.97`
- Popover opacity + translate
- Card shadow transition
- Edge drawing feedback
- Toast slide up

Nicht verwenden:

- Blur animation auf Text
- Scale animation auf Text-Cards
- heavy parallax
- Layout spring für große Canvas-Bewegungen

---

# 15. Interaction States

## 15.1 Hover

```css
.interactive:hover{
  background:var(--color-action-active);
  color:var(--color-text-primary);
}
```

## 15.2 Active

```css
.interactive:active{
  transform:scale(.97);
}
```

## 15.3 Focus

```css
:where(button,[tabindex],input,textarea,[contenteditable="plaintext-only"]):focus-visible{
  outline:var(--focus-ring-width) solid var(--focus-ring-color);
  outline-offset:var(--focus-ring-offset);
}
```

## 15.4 Disabled

```css
.disabled,
button:disabled{
  opacity:.42;
  cursor:not-allowed;
  pointer-events:none;
}
```

---

# 16. Accessibility Tokens

```css
:root{
  --a11y-target-size-min: 44px;
  --a11y-focus-width: 2px;
  --a11y-focus-offset: 2px;
  --a11y-focus-color: var(--color-focus);
  --a11y-text-min: 14px;
  --a11y-ui-text-min: 13px;
}
```

## 16.1 Visually Hidden

```css
.visually-hidden,
.sr-only{
  position:absolute!important;
  width:1px!important;
  height:1px!important;
  padding:0!important;
  margin:-1px!important;
  overflow:hidden!important;
  clip:rect(0,0,0,0)!important;
  white-space:nowrap!important;
  border:0!important;
}
```

## 16.2 ARIA-Pflicht

| Element | Pflicht |
|---|---|
| Canvas | `aria-label` |
| Node | `role="group"` |
| Selectable Node | `aria-selected` |
| Popover | `role="dialog"` oder `role="menu"` |
| Menu Trigger | `aria-haspopup`, `aria-expanded`, `aria-controls` |
| Menu Item | `role="menuitem"` |
| contenteditable | `role="textbox"`, `aria-label` |
| decorative SVG | `aria-hidden="true"` |

## 16.3 Minimum

- Text 14px für Inhaltswerte.
- 13px für UI-Labels.
- Touch targets 44x44px.
- Fokus sichtbar.
- 200% Zoom muss funktionieren.
- Kein Drag-only ohne Keyboard-Alternative.

---

# 17. Responsive / Fluid Behavior

## 17.1 Breakpoints

```css
:root{
  --bp-mobile: 560px;
  --bp-tablet: 900px;
  --bp-desktop: 1200px;
  --bp-wide: 1500px;
  --bp-ultra: 1800px;
}
```

## 17.2 Layout Breaks

```css
@media (max-width: 900px){
  .app{
    display:block;
    height:auto;
    min-height:100vh;
  }

  .sidebar{
    max-height:44vh;
    border-right:0;
    border-bottom:.5px solid var(--color-sidebar-border);
  }

  .floating-header{
    left:50%;
    width:calc(100vw - 24px);
    max-width:calc(100vw - 24px);
    overflow:auto;
  }
}
```

## 17.3 Fluid Typography

Für Webseiten/Marketing erlaubt:

```css
.hero-title{
  font-size:clamp(32px, 5vw, 88px);
}
```

Für Tools vorsichtig einsetzen:

```css
.tool-title{
  font-size:clamp(16px, 1vw, 18px);
}
```

Regel:

- Tool-UIs brauchen stabile Größen.
- Content-Websites können stärker fluid sein.
- Canvas-Tools dürfen nicht bei jeder Viewportänderung unkontrollierbar reflowen.

---

# 18. Canvas / Zoom System

Nur für Canvas-Tools relevant.

## 18.1 Zoom Steps

```js
const ZOOM_STEPS = [
  0.5,
  0.625,
  0.75,
  0.875,
  1,
  1.125,
  1.25,
  1.5,
  1.75,
  2
];
```

## 18.2 Regeln

- Keine freien Zoomwerte.
- Zoom immer quantisiert.
- Punkt unter Maus bleibt unter Maus.
- Text darf nicht blurry werden.
- Pan auf ganze Pixel runden.

## 18.3 CSS Zoom Formel

Für Chromium/WebKit mit CSS `zoom`:

```js
world = screen / zoom - pan;
pan = screen / zoom - world;
```

## 18.4 Transform Fallback

```js
world = (screen - pan) / zoom;
pan = screen - world * zoom;
```

## 18.5 Pan

```txt
Wheel = Pan
Cmd/Ctrl/Alt + Wheel = Zoom
Drag empty canvas = Pan
```

---

# 19. Drag / Drop System

## 19.1 Node Drag Rules

```txt
Click node = select
Click text = edit
Pointer movement < 4px = click
Pointer movement >= 4px = drag
Shift + drag = snap
Drag socket = connect
Release socket on empty canvas = spawn connected node
Click empty canvas = deselect
```

## 19.2 Rules

- Drag starts only after threshold.
- Textediting blocks drag.
- Sockets block card drag.
- Menus block card drag.
- Pointer capture on node.
- Save only after actual move.
- No native `grab` cursor.

---

# 20. Keyboard System

## 20.1 Shortcuts

```txt
Delete                 delete selected object
Cmd/Ctrl + S           save project
Cmd/Ctrl + E           export
Arrow                  nudge selected object 8px
Shift + Arrow          nudge 32px
Alt + Arrow            nudge 1px
1-8                    change selected object color
Escape                 close menus/popovers
Double click canvas    add object
Wheel                  pan
Cmd/Ctrl/Alt + Wheel   zoom
```

## 20.2 Guard

Shortcuts must not fire while editing text.

```js
function isEditingText(){
  const active = document.activeElement;
  return active?.matches?.('[contenteditable], input, textarea, select');
}
```

---

# 21. Data / Persistence

Wenn User Arbeit erzeugt, ist Persistenz Pflicht.

## 21.1 Project JSON

```js
const project = {
  version: 1,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  meta: {
    name: "Untitled Project"
  },
  view: {
    panX: 0,
    panY: 0,
    zoom: 1
  },
  nodes: [],
  edges: [],
  settings: {
    theme: "light"
  }
};
```

## 21.2 Autosave

```txt
- debounced
- clearable
- versioned key
- old data never silently crashes app
- import must validate
```

## 21.3 Import Validation

Jeder Import braucht Normalisierung:

```js
function normalizeProject(raw){
  return {
    nodes: Array.isArray(raw.nodes) ? raw.nodes.map(normalizeNode).filter(Boolean) : [],
    edges: Array.isArray(raw.edges) ? raw.edges.map(normalizeEdge).filter(Boolean) : [],
    view: normalizeView(raw.view)
  };
}
```

---

# 22. Export System

## 22.1 SVG Rules

Export must be self-contained:

```txt
- no dependency on external CSS
- no dependency on classes
- explicit fill/stroke attributes
- wrapped text
- viewBox correct
- background optional
- theme colors embedded
```

## 22.2 Icon Export

If exporting icons:

```txt
- currentColor mode
- transparent mode
- fixed frame mode
- trimmed viewBox mode
```

## 22.3 Canvas Export

If exporting tool canvas:

```txt
- nodes
- edges
- text
- sockets
- colors
- background
- rounded cards
```

---

# 23. Quality Checker

Optional for complex tools.

Checks:

```txt
- text too small
- contrast too low
- touch target below 44px
- focus missing
- unsupported empty labels
- off-grid objects
- object outside frame
- broken edges
- unvalidated import
- export missing objects
- text overflow
```

---

# 24. Figma / Penpot Token Mapping

## 24.1 Collections

```txt
Primitive Colors
Semantic Colors
Typography
Spacing
Radius
Elevation
Motion
Components
A11y
Z-Index
Iconography
```

## 24.2 Component Variants

```txt
Button: default / hover / active / focus / disabled
Chip: default / active / focus
Card: default / selected / dragging / error
Field: default / hover / focus / error / disabled
Popover: closed / open
Socket: default / hover / active / connected
```

## 24.3 Naming

```txt
color.text.primary
color.text.secondary
color.bg.canvas
color.surface.card
radius.card
space.card.padding
motion.spring.default
a11y.focus.width
z.popover
icon.stroke.default
```

---

# 25. Anti-Patterns

Nicht verwenden:

```txt
native RGB picker as main UI
native grab/grabbing cursor
massive blue selection rings
scale() on editable text cards
blur animation on cards or text
text-rendering: geometricPrecision
tiny 30px menu buttons
14px visual socket without 44px hit area
color-only information
placeholder-only labels
unbounded SVG text
CSS-dependent SVG export
unvalidated JSON load
free zoom values
connections from card center when sockets exist
bottom decoration lines on cards
overly bold UI typography
generic SaaS gradients
```

---

# 26. Implementation Blueprint

## 26.1 Minimum CSS File Structure

```txt
01-reset.css
02-primitives.css
03-semantic-tokens.css
04-theme-light-dark.css
05-typography.css
06-layout.css
07-components.css
08-interactions.css
09-accessibility.css
10-responsive.css
```

## 26.2 Minimum JS Modules

```txt
state.js
storage.js
render.js
selection.js
drag.js
zoom.js
keyboard.js
export.js
validation.js
accessibility.js
```

For single-file HTML tools, keep same conceptual sections inside one file.

---

# 27. Applicability Matrix

## 27.1 If the tool is a form generator

Use:

```txt
Tokens
Sidebar
Fields
Output cards
Autosave
Export
Accessibility
```

Skip:

```txt
Sockets
Canvas zoom
Node drag
Multi-connections
```

## 27.2 If the tool is a flow builder

Use:

```txt
Canvas
Nodes
Sockets
Edges
Zoom
Drag
Autosave
JSON
SVG Export
Shortcuts
```

Skip:

```txt
Long form wizard
Document pagination
```

## 27.3 If the tool is an invoice/document tool

Use:

```txt
Sidebar inputs
Document preview
A4 export
Typography system
Form validation
Autosave
```

Skip:

```txt
Sockets
Connections
Node graph
```

## 27.4 If the tool is an icon/vector tool

Use:

```txt
Grid
Canvas
Zoom
Primitive tools
Keylines
Export currentColor
Quality checker
Keyboard precision
```

Skip:

```txt
Large Bento cards
Long bullet notes
Form sections
```

---

# 28. Final System Rule

A tool built with this OS must feel like:

```txt
A precise local creative instrument.
Not a dashboard.
Not a template.
Not a generic SaaS app.
Not a decorative website.
```

The OS is:

```txt
canvas-first
glass-light
typographically calm
accessibility-aware
keyboard-aware
export-ready
locally persistent
minimal but not empty
structured but not rigid
```

---

# 29. Prompt for future extraction

Use this prompt when reverse-engineering another HTML/CSS file:

```txt
Reverse-engineer this HTML/CSS/JS file into a complete design-system specification.

Extract:
1. Primitive color tokens
2. Semantic color tokens
3. Theme mapping for light/dark
4. Typography scale
5. Font families, weights, line heights, letterspacing
6. Spacing scale and layout grid
7. Border radius scale
8. Shadows/elevation
9. Motion durations and easing
10. Component states: default, hover, active, focus, disabled
11. Z-index scale
12. Iconography rules: viewBox, stroke, fill, size
13. Accessibility tokens: focus rings, target sizes, visually-hidden, ARIA patterns
14. Responsive behavior and breakpoints
15. Fluid typography/spacing usage
16. Canvas/zoom/drag behavior if applicable
17. Keyboard shortcuts
18. Export behavior
19. Anti-patterns and fragile code
20. Applicability matrix: which parts are universal, which are tool-specific

Assume there is no prior design system.
Output one complete markdown document with CSS token blocks, JS behavior rules, component specs, implementation blueprint, and QA checklist.
```
