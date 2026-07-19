# Reconstruction Prompt: Nicks Pickup Lab v1.1

Rebuild the current application exactly from this specification. Do not depend on an existing implementation.

## Product objective

Create **Nicks Pickup Lab**, a polished, responsive, single-file browser application for comparative passive or active guitar/bass pickup measurement through an audio interface and a repeatable magnetic driver or tap fixture.

The current app provides:

- Input-device and input-channel selection plus live input metering
- Fixed operating-system-default output with no output selector
- One manually toggled 440 Hz sine test tone
- Multi-tap impulse response that captures 3, 5, or 7 events, scores them, and retains the cleanest
- Captured impulse waveform, logarithmic decay envelope, and resonant-ring FFT
- Ring frequency, T60 estimate, damping ratio ζ, Q, first-swing polarity, and rise time
- Band-selectable white-noise response for 2.5, 5, or 10 seconds
- 24 spectrum/time-domain metrics with detailed accessible tooltips
- Stepped magnetic saturation, 500 Hz–8 kHz Bode magnitude, and five-pulse relative polarity
- Version-2 JSON project save/load, CSV export, and current-theme PNG summary
- Four session-only themes: Light, Dark orange, Dark green, and Dark blue; Dark blue is the default

There is **no live oscilloscope/spectrum tab** and **no free-form excitation generator**. Do not reintroduce either.

## Deliverables

Create these files in one folder:

```text
index.html
README.md
PROMPT.md
```

All runtime HTML, CSS, JavaScript, SVG, favicons, and home-screen icon data must be in `index.html`. Do not use a framework, dependency, module, package manager, build process, external script, stylesheet, font, image, network request, upload, server API, analytics service, telemetry, cookie, localStorage, sessionStorage, or IndexedDB.

## Permission and privacy contract

- All audio processing is local.
- Never request input permission automatically.
- Show a branded splash immediately on load with theme-colored blurry ambient light and accents, a fancy two-line title, explanatory copy, and a translucent glass pickup icon.
- Splash actions are **Allow audio access** and **Explore first**.
- Only the splash's **Allow audio access** button may call `getUserMedia()`; there is no persistent Connect input button.
- Explain that no recordings are automatically saved and system output remains silent until explicitly armed.
- Input is never routed to audible output.

## Visual system

Use a refined technical-instrument aesthetic. Maximum shell width is `1580px`; desktop padding is `22px`, mobile padding `12px`; panel radius about `16px`. Use an Inter-style system sans-serif stack and a system monospace stack for measurements.

Required variables:

```css
/* Dark orange */
--bg: #0a0d0c;
--panel: #111715;
--panel-2: #151d1a;
--line: #28342f;
--ink: #e7eee9;
--muted: #93a29a;
--lime: #ffb24a;
--primary-fill: #f28c28;
--cyan: #ff7a3d;
--amber: #ffd166;
--red: #ff6470;
--canvas-bg: #090d0b;
--canvas-grid: #202b27;

/* Light */
--bg: #edf2ef;
--panel: #ffffff;
--panel-2: #f4f7f5;
--line: #c9d4ce;
--ink: #17231e;
--muted: #5b6c64;
--lime: #173f68;
--primary-fill: #214f7b;
--cyan: #0b5b96;
--amber: #a75b00;
--red: #cb3449;
--canvas-bg: #f8faf9;
--canvas-grid: #d9e1dd;

/* Dark green */
--bg: #080c09;
--panel: #101712;
--panel-2: #151e17;
--line: #2b3a2f;
--ink: #edf4ee;
--muted: #93a497;
--lime: #d5fe42;
--primary-fill: #9ecb2e;
--cyan: #b7ef38;
--canvas-bg: #070b08;
--canvas-grid: #202e24;

/* Dark blue */
--bg: #070b12;
--panel: #0d1420;
--panel-2: #111b2b;
--line: #263751;
--ink: #e9f1ff;
--muted: #90a3bd;
--lime: #4d9dff;
--primary-fill: #147cff;
--cyan: #00b8ff;
--canvas-bg: #060a10;
--canvas-grid: #1d2b40;
```

Use variables for every surface, canvas, grid, trace, point, export, label, page glow, permission splash, toaster, and large explanation tooltip. Dark orange glows and accents are orange, Dark green uses acid green, and Dark blue and Light use blue. Theme changes must recolor the visible permission splash immediately.

Create two translucent, blurred, inline-SVG single-coil pickup tiles—one in the header and one in the splash. Embed a graphical, no-text single-coil SVG favicon, a 32×32 PNG favicon fallback, and an opaque 180×180 PNG Apple touch icon as data URIs. Include `mobile-web-app-capable`, `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, and `apple-mobile-web-app-title` metadata. Keep every asset inside `index.html`; do not create external icon files.

## Header, hero, and layout

Header contains product identity, live status pill, and an accessible theme cycle button.

The four theme labels are:

- `Light`
- `Dark orange`
- `Dark green`
- `Dark blue`

Use values `light`, `dark-orange`, `dark-green`, and `dark-blue`. The button displays the active label and advances through the circular order Light → Dark orange → Dark green → Dark blue → Light. Never persist selection, always start in Dark blue, update the button's accessible label and browser `theme-color`, redraw every visible canvas on change, and use the current palette and theme name for PNG/CSV export.

Hero copy:

```text
See what the magnet
is really doing.
```

The supporting sentence ends with: `with your interface and exciter coil.`

Accent the second heading line. Use a two-column workspace:

- Left stack: **01 Audio routing**, **02 Project**
- Wide right panel: **03 Analyze pickup health**, with a glowing theme-accented **Measure All** button immediately left of **Clear measurements**

Stack below roughly 1100 px and use single-column mobile layout below roughly 760 px.

## Audio routing

Provide:

- Live input dBFS meter
- Input-device select
- Input-channel select derived from actual channel count
- Digital input trim from −18 to +18 dB
- Test-output meter labelled `TEST OUTPUT / SYSTEM DEFAULT`
- Test-output level slider from −48 to −6 dBFS, default −30 dBFS
- Driver/amplifier safety checkbox
- **Play 440 Hz test tone** and **Stop output**
- Note explaining fixed system-default output and no input monitoring

Do not render output-device or output-channel controls. Connect the output gain directly to `AudioContext.destination`; do not call `setSinkId()`.

Use `getUserMedia()` with audio only and request two channels where possible. Disable echo cancellation, noise suppression, and automatic gain control. Build:

```text
MediaStreamAudioSourceNode
  → ChannelSplitterNode
  → selected channel
  → digital trim GainNode
  → AnalyserNode for input meter
  → ScriptProcessorNode or equivalent local sample ring
  → zero-gain destination branch only to keep capture callbacks active
```

Retain approximately 15 seconds of selected-channel PCM. Rebuild the graph after input-channel change. Never connect input audibly to output.

## 440 Hz test tone

The only manual output generator is a fixed 440 Hz sine. It requires input connection and safety confirmation. Use short output ramps, toggle the button label between play/stop, update output meter and status, and allow **Stop output** at all times. Disable it while automated measurements run.

## Analysis tabs

Use accessible `role="tab"` controls in this order:

1. Bode response
2. Noise spectrum
3. Saturation
4. Polarity
5. Impulse / tap
6. Summary

The first tab is active. There is no Live scope tab.

The first five tabs are complete measurement workspaces: each keeps its description, native setup controls, run button, progress indicator, and its own result graphs and measurement cards. Do not add an Open Summary shortcut box to these tabs. Give each top measurement-action row approximately 18 px of space above and 20 px below; apply this independently of the Summary export toolbar.

**Measure All** runs the five measurements sequentially in visible tab order: Bode response → Noise spectrum → Saturation → Polarity → Impulse / tap. Activate each source tab when its test starts, await its real completion before continuing, keep Stop available, suppress per-test completion toasts during the batch, and show one centered `All five measurements complete.` toaster after full success. The final impulse stage continues to request the configured physical taps. On completion, cancellation, or failure, return to the first Bode tab and restore every control. A failed stage stops the remaining sequence and identifies the error in a toaster.

The Summary tab is a complete export dashboard. After the overview cards, create five semantic sections in the same order and with the same names as the source tabs. During startup, clone each source tab's graph and result DOM into its Summary section, rewrite cloned IDs with a `summary-` prefix, synchronize displayed values from the authoritative source elements, and render the cloned canvases from the same project data. The source results must remain in place. Project loading, clearing, theme redraws, and new measurements update both sets without recalculating measurements twice.

At the top of Summary, place **Export PNG** and **Export CSV** on one non-wrapping horizontal line. Do not include the word “complete” in either label. Give the toolbar clear breathing room above and below, approximately 18–20 px of vertical padding.

## Canvas requirements

All graphs use `<canvas>` with backing-store scale capped at `min(devicePixelRatio, 2)`. Use `ResizeObserver`. Every `.canvas-box` must set equal `height`, `min-height`, and `max-height`, plus `overflow:hidden`, so data can never enlarge the graph.

Every graph supports pointer hover/drag:

- Map cursor position to plot coordinates.
- Find the closest data value.
- Draw a vertical marker.
- Render a theme-aware tooltip inside the canvas.
- Clear it on pointer leave.

Use logarithmic x mapping for FFT/spectrum plots and appropriate log-dB y scales.

## Impulse / tap test

UI includes:

- Description emphasizing repeated taps and cleanest-capture selection
- Impulse-count select: 3, 5, or 7; default 5
- Detector-state surface using live status text
- Progress bar
- **Capture tap series**
- Captured waveform canvas
- Log decay-envelope canvas with fitted line
- Resonant-ring FFT canvas
- Result fields for ring frequency, T60, ζ, Q, first-swing polarity, and rise time

The impulse test is input-only and does not require the safety checkbox.

For each tap:

1. Display a short `KEEP QUIET` period of about 550 ms.
2. Measure roughly 400 ms of quiet RMS.
3. Use a trigger threshold of `max(0.0025, quietRms × 8)`.
4. Display `TAP NOW` and wait up to 15 seconds.
5. After detection, capture enough ring to retain about 1.5 seconds aligned around the event.
6. Measure peak, quiet noise, clipping, and strong secondary impacts.
7. Score roughly as `20log10(peak/noise) − secondaryPenalty − clippingPenalty`.

After all events, sort by score and retain/analyze the highest score. Save compact metadata for every capture, including original tap number, score, peak dB, noise dB, and clipped count. Save full derived data only for the winner.

### Impulse derivation

- Remove DC mean.
- Locate absolute peak.
- Find 10% and 90% threshold crossings before the first peak; rise time is their interval.
- Find the strongest signed excursion in approximately the first 12 ms after onset; report POSITIVE or NEGATIVE.
- Build 5 ms RMS envelope blocks from the peak.
- Normalize envelope peak to 0 dB and clamp plot floor near −100 dB.
- Fit a line primarily to envelope points from −5 to −40 dB; fall back to approximately −3 to −25 dB.
- If no meaningful negative slope exists, show T60/Q/ζ as unresolved.
- Otherwise `T60 = −60 / slope`.
- FFT the early ring with an 8192-point Hann window.
- Search approximately 60 Hz–10 kHz for the strongest ring component.
- `Q = π × ringFrequency × T60 / 6.907755`.
- `ζ = 1 / (2Q)`.
- Downsample the plotted waveform by keeping the maximum-magnitude sample per bucket so narrow transients survive.

Save:

```js
{
  sampleRate, captures, selectedIndex, score, peakDb,
  ringFrequency, t60, q, damping, polarity, riseMs,
  wave: [{x, y}],
  envelope: [{x, y}],
  decayFit: [{x, y}],
  spectrum: [{x, y}]
}
```

## White-noise spectrum

UI includes:

- Presets: Pickup focus 500–8,000 Hz; Guitar/bass 40–8,000 Hz; Full audio 20–20,000 Hz; Custom
- Editable numeric low/high Hz controls
- Durations: 2.5, 5, or 10 seconds; default 5
- **Measure white-noise spectrum**
- Progress bar
- One fixed-height logarithmic selected-spectrum canvas
- 24 metric cards

Changing numeric endpoints switches the preset to Custom. Clamp high frequency below Nyquist. Generate local white noise and pass it through high-pass and low-pass biquads with Q about 0.707, then through test-level gain to the system-default output. Capture selected-channel input during the run. Stop safely on cancellation.

Average several 8192-point Hann FFT power frames (roughly 4–16 depending on duration). Store a plot downsampled to at most about 1200 points, normalized so the strongest selected-band point is 0 dB.

### Required metrics

Compute and display all of these:

1. Peak frequency — strongest averaged selected-band bin.
2. Fundamental — lowest candidate maximizing weighted power at itself and harmonics.
3. RMS level — DC-removed time-domain RMS in dBFS.
4. Sample peak — absolute time-domain maximum in dBFS.
5. Crest factor — `20log10(peak/RMS)`.
6. DC offset — raw sample mean as percent full scale.
7. Noise floor — median selected-band spectral-bin dB.
8. SNR estimate — peak spectral dB minus median spectral floor.
9. Spectral centroid — power-weighted mean frequency.
10. 85% roll-off — frequency at cumulative 85% selected-band power.
11. Spectral bandwidth — power-weighted standard deviation around centroid.
12. Spectral flatness — geometric/arithmetic mean power ratio as percent.
13. Spectral slope — least-squares spectral dB versus log2 frequency in dB/octave.
14. THD estimate — RMS harmonics 2–8 relative to estimated fundamental.
15. Even / odd — even-harmonic to odd-harmonic power ratio in dB.
16. Peak asymmetry — positive/negative peak ratio in dB.
17. Zero crossings — DC-removed sign changes per second.
18. Clipped samples — count with absolute raw value at least 0.999.
19. Transient index — maximum 20 ms RMS block divided by median block RMS.
20. Nearest note — equal-tempered note and cent offset, A4 = 440 Hz.
21. Low band — integrated selected spectral power below 250 Hz.
22. Mid band — integrated selected spectral power from 250 Hz to 2 kHz.
23. High band — integrated selected spectral power above 2 kHz.
24. Tone confidence — map harmonic-score prominence over the median floor to 0–100%.

The UI must explain that broadband excitation makes fundamental, THD, even/odd, and nearest note lower-authority when tone confidence is low.

### Result and graph tooltips

Every result value in Impulse, Noise spectrum, Saturation, Bode response, and Polarity includes a keyboard-focusable `?` button with detailed explanation text. Every graph heading also includes a `?` button explaining the graph's role, how to read it, and its main confounder. The Summary copies retain these controls. Use one global, theme-aware, fixed-position `role="tooltip"` element. Show it on `mouseenter`, `focus`, and `click` so it works on touch screens; position it above or below without leaving the viewport. Hide it on `mouseleave`, `blur`, outside pointer press, or Escape. Style the tooltip as a large panel up to roughly 520 px wide with about 18 × 22 px padding, 14 px text, a 15 px radius, translucent blurred glass, and the same warm-orange border and glow treatment as the centered toaster message in all four themes.

Each tooltip explains:

- What is calculated
- What it indicates about a pickup or measurement chain
- The main caveat or confounder

Do not rely only on abbreviated labels or native `title` attributes.

## Existing tests retained

### Saturation

Keep eight relative 1 kHz drive steps:

```js
[-42, -36, -30, -24, -18, -12, -6, 0]
```

Actual drive is `testOutputLevel + relativeStep`. Store output RMS, fundamental, even harmonics, odd harmonics, asymmetry, and peak. Plot harmonic groups and transfer response.

### Bode magnitude

Keep 30 log-spaced sine points from 500 to 8000 Hz. Normalize to the strongest point, detect peak resonance, and show peak level, endpoint tilt, and count. This is magnitude-only.

### Relative polarity

Keep five shaped low-level pulses. Capture enough pre/post time for common interface latency, locate strongest excursion, keep a normalized 30 ms view, and vote on sign. Report POSITIVE, NEGATIVE, or INDETERMINATE when response is below about −80 dBFS or fewer than four votes agree.

All output-producing tests require input plus safety confirmation.

## Project schema

Use version 2:

```js
{
  version: 2,
  id, name, notes, created, updated,
  settings: {
    inputTrim, masterLevel, inputChannel,
    noiseLow, noiseHigh, noiseDuration, tapCount
  },
  impulse: null | { /* complete cleanest-tap result */ },
  noise: null | { low, high, duration, sampleRate, spectrum, metrics },
  saturation: [],
  bode: [],
  polarity: []
}
```

Save as pretty JSON data named `<safe-name>.pickup-health`, using no additional `.json` suffix. Load version 2 and migrate compatible version-1 projects by setting missing impulse/noise fields to null. Restore all relevant controls and redraw every result.

CSV export includes project metadata and notes, the complete Summary overview, every displayed measurement, and raw data for all eight graphs: impulse waveform/envelope/fit/FFT, white-noise spectrum, saturation harmonic/transfer rows, Bode magnitude, and all polarity pulse waveforms.

## Summary and PNG

Summary cards include:

- Bode resonance
- Saturation signature
- Relative polarity
- Measurement record

Do not place Impulse ring or Noise spectrum overview cards at the top of Summary; their detailed measurements remain available in their sections below.

Below the cards, Summary contains five separated, labelled result sections in this order: Bode response, Noise spectrum, Saturation, Polarity, and Impulse / tap. Together they contain synchronized copies of all eight graphs and every detailed measurement. The original graphs and measurements remain visible in their source tabs.

PNG is a tall, complete report canvas at 2× backing scale using the current theme. It contains the four remaining overview cards and their notes, project notes, all 42 detailed measurement values, and all eight graphs in Summary order: Bode magnitude, noise spectrum, harmonics versus drive, transfer curve, five polarity pulse responses, impulse waveform, decay envelope/fit, and impulse FFT.

CSV contains every item represented by Summary and the raw series needed to reconstruct every graph in Summary order: overview values and notes; Bode rows; raw white-noise metrics and spectrum; saturation harmonic/transfer rows; polarity votes and pulse waveform samples; impulse waveform, envelope, decay fit, and FFT.

## Error handling and cancellation

- Refuse output without input and safety confirmation.
- Allow input-only tap capture without safety confirmation.
- Disable all run buttons, **Measure All**, **Clear measurements**, and the 440 Hz button during a test or Measure All sequence. Keep Stop available; stopping a batch cancels its remaining stages.
- Keep Stop available.
- Cancellation clears the active-test marker; loops check it after every short wait.
- Always ramp output down in `finally` and on `beforeunload`.
- Show concise toasts for permission denial, missing input, safety confirmation, tap timeout, absent response, invalid project, completion, and cancellation. Toasts are large and centered in the viewport, with a translucent blurred panel, theme-colored border/dot/glow accents, centered text, and a subtle scale/vertical entrance transition.
- Never manufacture or simulate results when signal is absent.

## Accessibility and responsive behavior

- Use semantic headings, labels, native inputs/selects/buttons, tab roles, status regions, and visible focus.
- Buttons have a minimum practical height of about 38 px. Every native dropdown and single-line text or number input has an explicit, matching 40 px height; multiline textareas remain vertically resizable.
- Measurement and graph explanation tooltips work by keyboard focus, hover, and touch click; outside press and Escape dismiss them.
- Respect `prefers-reduced-motion`.
- Avoid horizontal page overflow down to 300 px.
- Metric grid is four columns on wide screens, three at medium width, two on tablets, and one on narrow phones.
- Noise options and tap controls stack responsively.
- Plot heights remain fixed on every breakpoint.

## README requirements

Document:

- Local-server startup and privacy
- Fixed system-output behavior
- 440 Hz workflow
- Electrical, thermal, feedback, hearing, and instrument-finish safety
- Air-core driver construction using a nonmagnetic former, roughly 0.25–0.35 mm wire, 220–350 turns, commonly 6–12 Ω measured DCR, twisted strain-relieved leads, optional gapped shield, and strict amplifier-load caveats
- Input preparation and repeatable geometry
- Detailed tap workflow, scoring, plots, formulas, and limitations
- Noise spans, durations, FFT averaging, all 24 metrics, and caveats
- Retained saturation/Bode/polarity tests
- Projects, CSV, PNG, themes, accessibility, quality checklist, limitations, and troubleshooting

## Validation checklist

1. Only `index.html`, `README.md`, and `PROMPT.md` are primary deliverables.
2. Inline script passes `node --check` after extraction.
3. No external runtime or network/storage APIs exist.
4. There is no Live scope tab, free-form generator, waveform selector, frequency slider, output device selector, output channel selector, or `setSinkId()`.
5. A fixed 440 Hz button is present.
6. Output connects only to system-default `AudioContext.destination`.
7. Splash is visible on Dark blue reload and does not call `getUserMedia()` automatically.
8. Impulse count offers exactly 3, 5, and 7 and defaults to 5.
9. Impulse result includes all three requested plots and six requested values.
10. White-noise duration offers exactly 2.5, 5, and 10 seconds.
11. Frequency span is selectable and custom endpoints are editable.
12. All 24 noise metrics and all 18 scalar results from the other tests exist with nonempty detailed explanation text.
13. Every graph heading has a detailed explanation button; the single global tooltip is accessible by focus, hover, and touch click and dismisses on outside press or Escape.
14. Every plot has cursor inspection and fixed height.
15. Canvas DPR is capped at 2.
16. Project version 2 contains complete impulse/noise data.
17. CSV and PNG include the new measurements.
18. One button cycles through Light, Dark orange, Dark green, and Dark blue; Dark blue is the reload default, theme changes redraw every plot, and exports use the current theme.
19. Desktop and mobile layouts have no horizontal overflow.
20. At runtime the five source tabs retain eight original canvases and all result cards; Summary contains eight additional synchronized canvases and copied result cards grouped into five sections.
21. No measurement tab contains an Open Summary copy box; Summary export buttons read **Export PNG** and **Export CSV**, remain on one horizontal line, and have space above and below.
22. A glowing, theme-accented **Measure All** button sits immediately left of **Clear measurements**, runs Bode → Noise → Saturation → Polarity → Impulse sequentially with automatic tab changes, returns to Bode, and shows a final completion toaster.
22. Complete PNG includes four overview cards, all 42 measurements, project notes, and all eight graphs; complete CSV includes all displayed information and raw data for every graph.
23. Large explanation tooltips use the same orange glass, blur, border, and glow language as toaster messages.
24. Browser console has no startup errors.
