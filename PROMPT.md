# Reconstruction Prompt: ИH Custom Winds v1.1

Rebuild the current application exactly from this specification. Do not depend on an existing implementation.

## Product objective

Create **ИH Custom Winds**, a polished, responsive, single-file browser application for comparative passive or active guitar/bass pickup measurement through an audio interface and a repeatable magnetic driver or tap fixture.

The current app provides:

- Input-device and input-channel selection plus live input metering
- Fixed operating-system-default output with no output selector
- One manually toggled 440 Hz sine test tone
- Manual-tap impulse response with selectable 3, 5, or 7 taps plus a separate automatic mode that emits exactly three sharp bipolar impulses, with adaptive noise rejection, stationary-hum cancellation, and robust aligned stacking
- Captured impulse waveform, logarithmic decay envelope, and resonant-ring FFT
- Ring frequency, T60 estimate, damping ratio ζ, Q, and rise time
- Band-selectable white-noise response for 2.5, 5, or 10 seconds
- 16 spectrum/time-domain metrics with detailed accessible tooltips
- Stepped magnetic saturation, 500 Hz–8 kHz Bode magnitude, and five-pulse relative phase
- Version-2 JSON project save/load, CSV export, and current-theme PNG summary
- Four session-only themes: Light, Dark orange, Dark green, and Dark blue; Dark green is the default

There is **no live oscilloscope/spectrum tab** and **no free-form excitation generator**. Do not reintroduce either.

## Deliverables

Create these files in one folder:

```text
index.html
logo.png
README.md
PROMPT.md
```

All runtime HTML, CSS, and JavaScript must be in `index.html`. Local visual assets are `logo.png`, `favicon.svg`, `favicon-32x32.png`, `favicon.ico`, and `apple-touch-icon.png`; `scripts/generate-icons.py` reproducibly rebuilds the raster icons but is not required at runtime. Do not use a framework, runtime dependency, module, package manager, external script, stylesheet, font, remote image, network request, upload, server API, analytics service, telemetry, cookie, localStorage, sessionStorage, or IndexedDB.

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

Create two translucent, blurred, inline-SVG single-coil pickup tiles—one in the header and one in the splash. Use matching graphical, no-text pickup artwork for the local favicon assets and the opaque 180×180 iPhone home-screen PNG. Include Apple web-app title, capability, status-bar, and touch-icon metadata; update the Apple title when configurable branding changes.

## Header, hero, and layout

Header contains product identity, live status pill, and an accessible theme cycle button.

The four theme labels are:

- `Light`
- `Dark orange`
- `Dark green`
- `Dark blue`

Use values `light`, `dark-orange`, `dark-green`, and `dark-blue`. The button displays the active label and advances through the circular order Light → Dark orange → Dark green → Dark blue → Light. Never persist selection, always start in Dark green, update the button's accessible label and browser `theme-color`, redraw every visible canvas on change, and use the current palette and theme name for PNG/CSV export.

Default hero copy:

```text
Nicks Pickup Lab
```

The supporting sentence ends with: `with your interface and exciter coil.` Keep the hero title on one line where space allows. With the default name, accent only the words `Pickup Lab`; for a customized lab name, accent its final two words.

Use a two-column workspace:

- Left stack: **01 Audio routing**, **02 Project**
- Wide right panel: **03 Analyze pickup health**, with a glowing theme-accented **Measure All** button immediately left of **Clear measurements**
- Display `logo.png` at the far upper-right of the header, after the status and theme controls. Keep its aspect ratio and scale it down on mobile.

Stack below roughly 1100 px and use single-column mobile layout below roughly 760 px.

## Audio routing

Provide:

- Live input dBFS meter
- Input-device select
- Input-channel select derived from actual channel count
- Digital input trim from −18 to +18 dB
- Test-output meter labelled `TEST OUTPUT / SYSTEM DEFAULT`
- Test-output level slider from −48 to −6 dBFS, default −30 dBFS
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

## Project records

Begin with fields labelled **Project Name** and **Project Notes**, then add two bordered subsections.

The **Customer** subsection contains labelled fields for Name, Address, Phone, eMail, Notes, and Wind Date. Use suitable text, telephone, email, numeric-text, and multiline controls. Wind Date uses Swiss `DD.MM.YYYY` formatting and formats digits as the user types; use `DD.MM.YYYY` as the placeholder without a separate format-hint string.

The **Pickup** subsection starts with Pickup ID, defaulting to `NH 7k42 #1`, then contains independent checkboxes for Guitar, Bass, Single Coil, Humbucker, Clockwise, and Counterclockwise. It also contains fields for Wire Type, Gauge, # Winds, Polarity, Phase, Pole Insulator, Protection, Leads, Start Wire (Hot), and End Wire (Ground). Wind count is a non-negative whole number. Defaults are Plain Enamel, AWG42, 7000 winds, South, Negative, Kapton Tape, Tissue, Waxed Pushback, Yellow, and Black respectively.

Every customer and pickup value participates in dirty-state tracking, project save/load, legacy-project migration, CSV export, and PNG summary export.

## 440 Hz test tone

The only manual output generator is a fixed 440 Hz sine. It requires an input connection. Use short output ramps, toggle the button label between play/stop, update output meter and status, and allow **Stop output** at all times. Disable it while measurements run.

## Analysis tabs

Use accessible `role="tab"` controls in this order:

1. Bode response
2. Noise spectrum
3. Saturation
4. Phase
5. Impulse / tap
6. Summary
7. Settings

The first tab is active. There is no Live scope tab.

The first five tabs are complete measurement workspaces: each keeps its description, native setup controls, run button, progress indicator, and its own result graphs and measurement cards. Do not add an Open Summary shortcut box to these tabs. Give each top measurement-action row approximately 18 px of space above and 20 px below; apply this independently of the Summary export toolbar.

**Measure All** runs the five measurements sequentially in visible tab order: Bode response → Noise spectrum → Saturation → Phase → Impulse / tap. Activate each source tab when its test starts, await its real completion before continuing, keep Stop available, suppress per-test completion toasts during the batch, and show one centered `All five measurements complete.` toaster after full success. The final impulse stage uses Capture Auto and emits exactly three impulses, so the batch never pauses for manual taps. On completion, cancellation, or failure, return to the first Bode tab and restore every control. A failed stage stops the remaining sequence and identifies the error in a toaster.

The Summary tab is a complete export dashboard. After the overview cards, create five semantic sections in the same order and with the same names as the source tabs. During startup, clone each source tab's graph and result DOM into its Summary section, rewrite cloned IDs with a `summary-` prefix, synchronize displayed values from the authoritative source elements, and render the cloned canvases from the same project data. The source results must remain in place. Project loading, clearing, theme redraws, and new measurements update both sets without recalculating measurements twice.

The Settings tab contains labelled Tool name and Lab name fields, defaulting to `ИH Custom Winds` and `Nicks Pickup Lab`, plus an **Apply** button. Apply trims blank values back to their defaults, updates the visible header, hero, browser title, splash product name, logo alternative text, CSV/PNG branding, and PDF header/footer. Accent the last two words of a customized lab name in the hero. Store both names in the current project and restore them on project load.

Place **Export PDF** in the Project action row immediately to the right of **Load project**. At the top of Summary, keep **Export PNG** and **Export CSV** on one non-wrapping horizontal line. Do not include the word “complete” in the labels. Give the Summary toolbar clear breathing room above and below, approximately 18–20 px of vertical padding.

**Export PDF** builds a real multi-page A4 PDF locally without external libraries or uploads. Every page uses a clean light print palette, the configurable tool name (default `ИH Custom Winds`) at upper left, the logo at upper right, and a section title. The footer contains only the configurable lab name; it has no separator, timestamp, or page number. Embed a compact copy of the logo as a data URL specifically for PDF rendering; never draw the external `logo.png` element into the PDF canvas, because that can taint canvases and make `toBlob()` fail with an insecure-operation error under `file://`. Pages 1–2 contain Project Information: project metadata without Project ID, customer record, pickup properties, and measurement settings. Created and Updated use date-only Swiss formatting. Pickup ID is the first field in the PDF Pickup section. Render Guitar, Bass, Single Coil, Humbucker, Clockwise, and Counterclockwise as checked or empty boxes in three vertical pairs: Guitar above Bass, Single Coil above Humbucker, and Clockwise above Counterclockwise. Page 3 places Bode response above Relative phase, page 4 places Saturation above Noise spectrum, and page 5 contains Impulse / tap. Omit graphs from Noise spectrum and Relative phase; retain the Bode graph, both Saturation graphs, and all three Impulse graphs, with graphs before data fields and labelled x/y values. Mark the Bode peak-resonance point. Append an Annex titled `Measurement glossary`, spanning as many pages as needed, containing every displayed measurement term and the exact explanatory text from its tooltip. Include all 33 displayed measurement fields. Download as `<safe-name>-complete-record.pdf`.

## Canvas requirements

All graphs use `<canvas>` with backing-store scale capped at `min(devicePixelRatio, 2)`. Use `ResizeObserver`. Every `.canvas-box` must set equal `height`, `min-height`, and `max-height`, plus `overflow:hidden`, so data can never enlarge the graph.

Every graph supports pointer hover/drag:

- Map cursor position to plot coordinates.
- Find the closest data value.
- Draw a vertical marker.
- Render a theme-aware tooltip inside the canvas.
- Clear it on pointer leave.

Use logarithmic x mapping for FFT/spectrum plots and appropriate log-dB y scales.

## Impulse-response / tap test

UI includes:

- Description explaining both physical manual taps and the three-impulse automatic mode, adaptive noise rejection, and noise-reduced aligned stacking
- Native tap-count selector with 3, 5, and 7 choices; default 3
- Detector-state surface using live status text
- Progress bar
- **Manual Capture** for the selected 3, 5, or 7 physical taps
- **Capture Auto** for exactly three output-generated impulses
- Captured waveform canvas limited to an aligned 20 ms onset view
- Log decay-envelope canvas covering the captured decay, with fitted line
- Resonant-ring FFT canvas
- Result fields for ring frequency, T60, ζ, Q, and rise time

Manual Capture is input-only and uses the selected input. It never activates the output. The operator creates each physical or magnetic impulse after the detector displays **TAP NOW**.

For each selected tap:

1. Display **LEARNING NOISE**, allow the input to settle, and collect about 700 ms of baseline audio.
2. High-pass condition the detector path around 70 Hz, split it into short blocks, and measure median RMS, median absolute deviation, 95th-percentile RMS, and 97th-percentile peak to derive adaptive thresholds. Keep the saved measurement path full-band.
3. Require five stable frames before arming and displaying **TAP NOW · NOISE GATE ARMED**.
4. Trigger only on a fresh, steep transient that clears RMS, peak, crest-factor, novelty, peak-rise, and sample-difference roughness thresholds. Evaluate the strongest short slice in the latest input window so a ScriptProcessor block boundary cannot hide the attack.
5. Retain about 1.35 seconds aligned within a narrow trigger window for analysis, but store and display only the first 20 ms in the captured-waveform series.
6. Measure attack SNR/gain over baseline, decay from attack to tail, and clipping.
7. Reject weak, noise-like, non-decaying, or clipped captures and ask for another tap, with at most three rejected attempts per requested tap.
8. Score accepted responses from raw SNR, conditioned transient SNR, and decay quality with clipping and retry penalties.

For each accepted tap, use its pre-tap quiet reference to identify coherent 50 or 60 Hz mains hum and harmonics through 1.2 kHz. Fit candidate components to the final 480 ms of the capture and subtract only components whose amplitude remains consistent with the quiet reference. Do not use a hard amplitude gate or broadband smoothing that would shorten the measured decay.

After all selected taps, rank them by score and use the highest-scoring tap as the alignment, amplitude, and phase anchor. Peak-align the cleaned captures, conservatively normalize their amplitudes, reject captures with early-ring correlation below about 0.38, and compute a sample-wise median of the remaining taps. Analyze this robust stack. Save compact per-tap metadata plus a `denoising` record containing the method, stacked-tap count, late-tail noise reduction in dB, and removed hum frequencies. If a clean tap cannot be obtained, report a clear capture error and never manufacture results.

Capture Auto emits exactly three independent 4.5 ms, zero-DC bipolar impulses through the operating system's default output at the selected test-output level. Before each output event, learn approximately 700 ms of quiet input. Schedule one short AudioBufferSource pulse, capture the return for long enough to retain approximately 1.35 seconds from its detected onset, and locate the response within a bounded post-output latency window using the high-pass-conditioned signal. Validate raw and transient SNR, attack gain, decay, and clipping. Do not retry a rejected automatic response with an extra pulse: each run must emit exactly three. Apply the same stationary-hum cancellation, alignment, correlation rejection, robust stacking, and impulse analysis to accepted responses. Save `captureMode: "auto"` plus excitation type, emitted/accepted counts, 4.5 ms duration, and output level. If all three are rejected, give concrete routing/gain guidance and do not manufacture a result.

### Impulse derivation

- Remove DC mean.
- Locate absolute peak.
- Find 10% and 90% threshold crossings before the first peak; rise time is their interval.
- Find the strongest signed excursion in approximately the first 12 ms after onset; report POSITIVE or NEGATIVE.
- Build 5 ms RMS envelope blocks across the aligned capture.
- Normalize the envelope peak to 0 dB and clamp the plot floor near −100 dB.
- Fit a line primarily to envelope points from −5 to −40 dB; fall back to approximately −3 to −25 dB.
- If no meaningful negative slope exists, show T60/Q/ζ as unresolved.
- Otherwise `T60 = −60 / slope`.
- FFT the early ring with an 8192-point Hann window.
- Search approximately 60 Hz–10 kHz for the strongest ring component.
- `Q = π × ringFrequency × T60 / 6.907755`.
- `ζ = 1 / (2Q)`.
- Downsample only the aligned 20 ms onset waveform by keeping the maximum-magnitude sample per bucket so narrow transients survive.

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
- 16 metric cards

Changing numeric endpoints switches the preset to Custom. Clamp high frequency below Nyquist. Generate local white noise and pass it through high-pass and low-pass biquads with Q about 0.707, then through test-level gain to the system-default output. Capture selected-channel input during the run. Stop safely on cancellation.

Average several 8192-point Hann FFT power frames (roughly 4–16 depending on duration). Store a plot downsampled to at most about 1200 points, normalized so the strongest selected-band point is 0 dB.

### Required metrics

Compute and display all of these:

1. Peak frequency — strongest averaged selected-band bin.
2. Fundamental — lowest candidate maximizing weighted power at itself and harmonics.
3. RMS level — DC-removed time-domain RMS in dBFS.
4. Sample peak — absolute time-domain maximum in dBFS.
5. Spectral centroid — power-weighted mean frequency.
6. 85% roll-off — frequency at cumulative 85% selected-band power.
7. Spectral bandwidth — power-weighted standard deviation around centroid.
8. Spectral flatness — geometric/arithmetic mean power ratio as percent.
9. Spectral slope — least-squares spectral dB versus log2 frequency in dB/octave.
10. THD estimate — RMS harmonics 2–8 relative to estimated fundamental.
11. Even / odd — even-harmonic to odd-harmonic power ratio in dB.
12. Peak asymmetry — positive/negative peak ratio in dB.
13. Transient index — maximum 20 ms RMS block divided by median block RMS.
14. Low band — integrated selected spectral power below 250 Hz.
15. Mid band — integrated selected spectral power from 250 Hz to 2 kHz.
16. High band — integrated selected spectral power above 2 kHz.

The UI explains that broadband excitation makes fundamental, THD, and even/odd comparative screening indicators rather than calibrated measurements.

### Result and graph tooltips

Every result value in Impulse, Noise spectrum, Saturation, Bode response, and Phase includes a keyboard-focusable `?` button with detailed explanation text. Every graph heading also includes a `?` button explaining the graph's role, how to read it, and its main confounder. The Summary copies retain these controls. Use one global, theme-aware, fixed-position `role="tooltip"` element. Show it on `mouseenter`, `focus`, and `click` so it works on touch screens; position it above or below without leaving the viewport. Hide it on `mouseleave`, `blur`, outside pointer press, or Escape. Style the tooltip as a large panel up to roughly 520 px wide with about 18 × 22 px padding, 14 px text, a 15 px radius, translucent blurred glass, and the same warm-orange border and glow treatment as the centered toaster message in all four themes.

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

Keep 30 log-spaced sine points from 500 to 8000 Hz. Normalize to the strongest point, detect peak resonance, visibly mark that point on the Bode plot, and show peak level, endpoint tilt, and count. This is magnitude-only. Every graph retains readable x- and y-axis tick values even before measurement data exists; PDF graphs do the same.

### Relative phase

Keep five shaped low-level pulses. Capture enough pre/post time for common interface latency, locate strongest excursion, keep a normalized 30 ms view, and vote on sign. Report POSITIVE, NEGATIVE, or INDETERMINATE when response is below about −80 dBFS or fewer than four votes agree.

All output-producing tests require an input connection.

## Project schema

Use version 2:

```js
{
  version: 2,
  id, name, notes, created, updated,
  branding: { toolName, labName },
  customer: {
    name, address, phone, email, notes, windDate, pickupId
  },
  pickup: {
    guitar, bass, singleCoil, humbucker,
    clockwise, counterclockwise,
    wireType, gauge, winds, polarity, phase,
    poleInsulator, protection, leads, startWire, endWire
  },
  settings: {
    inputTrim, masterLevel, inputChannel,
    noiseLow, noiseHigh, noiseDuration, tapCount
  },
  impulse: null | { /* complete noise-reduced manual or automatic result, including captureMode, optional excitation metadata, and denoising metadata */ },
  noise: null | { low, high, duration, sampleRate, spectrum, metrics },
  saturation: [],
  bode: [],
  polarity: []
}
```

Save as pretty JSON data named `<safe-name>.custom-winds`, using no additional `.json` suffix. Load version 2 and migrate compatible version-1 projects by setting missing impulse/noise fields to null and missing customer/pickup records to the current form defaults. Continue accepting legacy `.pickup-health` files. Restore all relevant controls and redraw every result.

CSV export includes customer and pickup records, project metadata and notes, the complete Summary overview, every displayed measurement, impulse capture-mode/automatic-excitation metadata, impulse noise-cancellation metadata, and raw data for all eight graphs: impulse waveform/envelope/fit/FFT, white-noise spectrum, saturation harmonic/transfer rows, Bode magnitude, and all phase pulse waveforms. PDF and PNG exports identify Manual versus Automatic capture, the aligned-response count, and achieved late-tail noise reduction; PDF also lists removed hum frequencies.

## Summary and PNG

Summary cards include:

- Bode resonance
- Saturation signature
- Relative phase
- Measurement record

Do not place Impulse ring or Noise spectrum overview cards at the top of Summary; their detailed measurements remain available in their sections below.

Below the cards, Summary contains five separated, labelled result sections in this order: Bode response, Noise spectrum, Saturation, Phase, and Impulse / tap. Together they contain synchronized copies of all eight graphs and every detailed measurement. The original graphs and measurements remain visible in their source tabs.

PNG is a tall, complete report canvas at 2× backing scale using the current theme. It contains the four remaining overview cards and their notes, project notes, all 33 detailed measurement values, and all eight graphs in Summary order: Bode magnitude, noise spectrum, harmonics versus drive, transfer curve, five phase pulse responses, impulse waveform, decay envelope/fit, and impulse FFT.

CSV contains every item represented by Summary and the raw series needed to reconstruct every graph in Summary order: overview values and notes; Bode rows; raw white-noise metrics and spectrum; saturation harmonic/transfer rows; phase votes and pulse waveform samples; impulse waveform, envelope, decay fit, and FFT.

## Error handling and cancellation

- Refuse output without an input connection.
- Require an input connection before either impulse mode can run. Manual Capture is input-only; Capture Auto additionally uses the fixed system-default output.
- Disable all run buttons, **Measure All**, **Clear measurements**, and the 440 Hz button during a test or Measure All sequence. Keep Stop available; stopping a batch cancels its remaining stages.
- Keep Stop available.
- Cancellation clears the active-test marker; loops check it after every short wait.
- Always ramp output down in `finally` and on `beforeunload`.
- Show concise toasts for permission denial, missing input, tap timeout, rejected tap series, invalid project, completion, and cancellation. Toasts are large and centered in the viewport, with a translucent blurred panel, theme-colored border/dot/glow accents, centered text, and a subtle scale/vertical entrance transition.
- Never manufacture or simulate results when signal is absent.

## Accessibility and responsive behavior

- Use semantic headings, labels, native inputs/selects/buttons, tab roles, status regions, and visible focus.
- Buttons have a minimum practical height of about 38 px. Every native dropdown and single-line text or number input has an explicit, matching 40 px height; multiline textareas remain vertically resizable.
- Measurement and graph explanation tooltips work by keyboard focus, hover, and touch click; outside press and Escape dismiss them.
- Respect `prefers-reduced-motion`.
- Avoid horizontal page overflow down to 300 px.
- Metric grid is four columns on wide screens, three at medium width, two on tablets, and one on narrow phones.
- Noise options and impulse-status controls stack responsively.
- Plot heights remain fixed on every breakpoint.

## README requirements

Document:

- Local-server startup and privacy
- Fixed system-output behavior
- 440 Hz workflow
- Electrical, thermal, feedback, hearing, and instrument-finish safety
- Air-core driver construction using a nonmagnetic former, roughly 0.25–0.35 mm wire, 220–350 turns, commonly 6–12 Ω measured DCR, twisted strain-relieved leads, optional gapped shield, and strict amplifier-load caveats
- Input preparation and repeatable geometry
- Detailed manual-tap and three-pulse automatic workflows, adaptive detection, hum cancellation, robust stacking, scoring, plots, formulas, and limitations
- Noise spans, durations, FFT averaging, all 16 metrics, and caveats
- Retained saturation/Bode/phase tests
- Projects, CSV, PNG, themes, accessibility, quality checklist, limitations, and troubleshooting

## Validation checklist

1. Only `index.html`, `README.md`, and `PROMPT.md` are primary deliverables.
2. Inline script passes `node --check` after extraction.
3. No external runtime or network/storage APIs exist.
4. There is no Live scope tab, free-form generator, waveform selector, frequency slider, output device selector, output channel selector, or `setSinkId()`.
5. A fixed 440 Hz button is present.
6. Output connects only to system-default `AudioContext.destination`.
7. Splash is visible on Dark green reload and does not call `getUserMedia()` automatically.
8. Impulse / tap offers Manual Capture with exactly 3, 5, and 7 taps (3 default) and Capture Auto with exactly three emitted impulses. Manual waits for a fresh transient after **TAP NOW** and never activates output; Auto uses only the fixed system-default output.
9. Impulse result includes all three requested plots and six requested values.
10. White-noise duration offers exactly 2.5, 5, and 10 seconds.
11. Frequency span is selectable and custom endpoints are editable.
12. All 16 noise metrics and all 18 scalar results from the other tests exist with nonempty detailed explanation text.
13. Every graph heading has a detailed explanation button; the single global tooltip is accessible by focus, hover, and touch click and dismisses on outside press or Escape.
14. Every plot has cursor inspection and fixed height.
15. Canvas DPR is capped at 2.
16. Project version 2 contains complete impulse/noise data.
17. CSV and PNG include the new measurements.
18. One button cycles through Light, Dark orange, Dark green, and Dark blue; Dark green is the reload default, theme changes redraw every plot, and exports use the current theme.
19. Desktop and mobile layouts have no horizontal overflow.
20. At runtime the five source tabs retain eight original canvases and all result cards; Summary contains eight additional synchronized canvases and copied result cards grouped into five sections.
21. No measurement tab contains an Open Summary copy box; **Export PDF** sits beside **Load project**, while Summary buttons read **Export PNG** and **Export CSV**, remain on one horizontal line, and have space above and below.
22. A glowing, theme-accented **Measure All** button sits immediately left of **Clear measurements**, runs Bode → Noise → Saturation → Phase → automatic three-impulse capture sequentially with automatic tab changes, returns to Bode, and shows a final completion toaster.
22. Complete PNG includes four overview cards, all 33 measurements, project notes, and all eight graphs; complete CSV includes all displayed information and raw data for every graph.
23. Large explanation tooltips use the same orange glass, blur, border, and glow language as toaster messages.
24. Settings defaults to `ИH Custom Winds` and `Nicks Pickup Lab`; Apply updates the UI and all exports, and saved projects preserve both names.
25. PDF places Bode above Relative phase on page 3 and Saturation above Noise spectrum on page 4, omits Noise and Phase graphs, arranges checkbox pickup selections in the requested vertical pairs, uses the lab name alone in the footer, contains no page numbers or footer timestamps, and appends a complete tooltip-derived measurement glossary annex.
26. Browser console has no startup errors.
