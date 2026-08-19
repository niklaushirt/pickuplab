# Reconstruction Prompt: ИH Custom Winds v.2.1

Rebuild the current application exactly from this specification. Do not depend on an existing implementation.

## Product objective

Create **ИH Custom Winds**, a polished, responsive, single-file browser application for comparative passive or active guitar/bass pickup measurement through an audio interface and a repeatable magnetic driver fixture.

The current app provides:

- Input-device and input-channel selection plus live input metering
- Fixed operating-system-default output with no output selector
- One manually toggled 440 Hz sine test tone
- Band-selectable white-noise response for 2.5, 5, or 10 seconds
- 16 spectrum/time-domain metrics with detailed accessible tooltips
- Stepped magnetic saturation, continuous-sweep 500 Hz–8 kHz Bode magnitude, and five-pulse relative phase
- Version-2 JSON project save/load, CSV export, and current-theme PNG summary
- Four locally persisted themes: Light, Dark orange, Dark green, and Dark blue; Dark blue is the first-run default

There is **no live oscilloscope/spectrum tab** and **no free-form excitation generator**. Do not reintroduce either.

## Deliverables

Create these files in one folder:

```text
index.html
logo.png
README.md
PROMPT.md
```

All runtime HTML, CSS, and JavaScript must be in `index.html`. Local visual assets are `logo.png`, `favicon.svg`, `favicon-32x32.png`, `favicon.ico`, and `apple-touch-icon.png`; `scripts/generate-icons.py` reproducibly rebuilds the raster icons but is not required at runtime. Do not use a framework, runtime dependency, module, package manager, external script, stylesheet, font, remote image, network request, upload, server API, analytics service, telemetry, cookie, sessionStorage, or IndexedDB. Use `localStorage` only for the automatic application-state persistence described below.

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

Use values `light`, `dark-orange`, `dark-green`, and `dark-blue`. The button displays the active label and advances through the circular order Light → Dark orange → Dark green → Dark blue → Light. Start in Dark blue only when no stored state exists; otherwise restore the saved theme. Update the button's accessible label and browser `theme-color`, redraw every visible canvas on change, persist the selection, and use the current palette and theme name for PNG/CSV export.

Default hero copy:

```text
Nicks Pickup Lab
```

The supporting sentence ends with: `with your interface and exciter coil.` Keep the hero title on one line where space allows. With the default name, accent only the words `Pickup Lab`; for a customized lab name, accent its final two words.

Use a two-column upper workspace:

- Narrow left panel: **01 Audio routing**
- Wide right panel: **02 Analyze pickup**, with a glowing theme-accented **Measure All** button immediately left of **Clear measurements**
- Full-width lower panel: **03 Project**, spanning both upper columns. Place Customer on the left and Pickup on the right at desktop widths, then stack them on narrow screens.
- Display `logo.png` at the far upper-right of the header, after the status and theme controls. Keep its aspect ratio and scale it down on mobile.

Stack below roughly 1100 px and use single-column mobile layout below roughly 760 px.

## Audio routing

Provide:

- Two clearly separated bordered groups inside Audio routing: a green-accented **Input** group for captured-interface controls and a blue-accented **Output** group for system-output controls. Keep the groups vertically stacked and preserve semantic `fieldset`/`legend` labelling.
- Live input dBFS meter
- Input-device select
- Input-channel select derived from actual channel count
- Digital input trim from −48 to +18 dB. Only after an input-device or input-channel change, reset Input trim to 0 dB and Output level to −30 dBFS, remove the previous route correction, and capture exactly one quiet analyser window lasting no more than three seconds from the same `AnalyserNode` used by the INPUT meter. During the entire calibration show a blocking overlay with the exact message **Calibrating, please wait.** plus a short instruction to keep the input quiet; remove it in the calibration `finally` path. Do not depend on `ScriptProcessorNode` callbacks for route calibration. Use the complete window's raw RMS, including visible DC, and apply at most one whole-dB Input-trim reduction when the baseline is louder than −70 dBFS. Raise Output level by the matching amount within its safe range and report any uncompensated amount. Do not perform verification passes. Lock measurement launch and route selectors during calibration, lock route selectors during measurements, and refuse measurement start while calibration is active. Measurements reuse the learned route profile and never recalibrate or change Input trim/Output automatically. Draw a small green reference line at −70 dBFS on the INPUT meter while retaining the red −12 dBFS line.
- Output meter labelled `OUTPUT LEVEL / SYSTEM DEFAULT`
- Output-level slider from −48 to −6 dBFS, default −30 dBFS
- **Play 440 Hz test tone** and **Stop output**
- Note explaining fixed system-default output, no input monitoring, and automatic route-specific noise-floor learning

Do not render output-device or output-channel controls. Connect the output gain directly to `AudioContext.destination`; do not call `setSinkId()`.

Use `getUserMedia()` with audio only and request two channels where possible. Disable echo cancellation, noise suppression, and automatic gain control.

After every input-device or input-channel change, keep output silent, discard the previous profile, allow the new route to settle, and record roughly 900 ms of quiet input. Store this profile only in the current browser session. Measure its RMS/peak floor and persistent 50/60 Hz harmonics. Conservatively subtract learned stationary hum from subsequent captures while protecting any active test frequency that overlaps a learned harmonic. The Bode estimator additionally subtracts the learned noise power from each local continuous-sweep analysis window. Show learning and the resulting input-noise level in the top-right status field.

Build:

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

The **Customer** subsection contains labelled fields for Name, Address, Phone, eMail, Notes, and Wind Date. Use suitable text, telephone, email, numeric-text, and multiline controls. Wind Date uses European `DD.MM.YYYY` formatting and formats digits as the user types; use `DD.MM.YYYY` as the placeholder without a separate format-hint string.

The **Pickup** subsection starts with Pickup ID, defaulting to `NH 7k42 #1`, then contains independent checkboxes for Guitar, Bass, Single Coil, Humbucker, Clockwise, and Counterclockwise. Wire Type is a dropdown containing Plain Enamel, Heavy Formvar, and Poly, with Plain Enamel selected by default. Gauge is a dropdown containing AWG41, AWG42, AWG43, and AWG44, with AWG42 selected by default. Polarity is a dropdown containing North and South, with South selected by default. Phase is a dropdown containing Negative and Positive, with Negative selected by default. It also contains fields for # Winds, Pole Insulator, Protection, Leads, Start Wire (Hot), and End Wire (Ground). Wind count is a non-negative whole number. Remaining defaults are 7000 winds, Kapton Tape, Tissue, Waxed Pushback, Yellow, and Black respectively.

Every customer and pickup value participates in dirty-state tracking, project save/load, legacy-project migration, CSV export, and PNG summary export.

## 440 Hz test tone

The only manual output generator is a fixed 440 Hz sine. It requires an input connection. Use short output ramps, toggle the button label between play/stop, update output meter and status, and allow **Stop output** at all times. Disable it while measurements run.

## Analysis tabs

Use accessible `role="tab"` controls in this order:

1. Bode response
2. Phase
3. Spectrum
4. Saturation
5. Summary
6. Settings

The first tab is active. There is no Live scope tab.

The first four tabs are complete measurement workspaces: each keeps its description, native setup controls, run button, progress indicator, and its own result graphs and measurement cards. Do not add an Open Summary shortcut box to these tabs. Give each top measurement-action row approximately 18 px of space above and 20 px below; apply this independently of the Summary export toolbar.

**Measure All** runs the four measurements sequentially in visible tab order: Bode response → Phase → Spectrum → Saturation. Activate each source tab when its test starts, await its real completion before continuing, keep Stop available, suppress per-test completion toasts during the batch, and show one centered `All four measurements complete.` toaster after full success. On completion, cancellation, or failure, return to the first Bode tab and restore every control. A failed stage stops the remaining sequence and identifies the error in a toaster.

The Summary tab is a complete export dashboard. After the overview cards, create four semantic sections in the same order and with the same names as the source tabs. During startup, clone each source tab's graph and result DOM into its Summary section, rewrite cloned IDs with a `summary-` prefix, synchronize displayed values from the authoritative source elements, and render the cloned canvases from the same project data. The source results must remain in place. Project loading, clearing, theme redraws, and new measurements update both sets without recalculating measurements twice.

The Settings tab contains labelled Tool name and Lab name fields, defaulting to `ИH Custom Winds` and `Nicks Pickup Lab`, plus an **Apply** button. Apply trims blank values back to their defaults, updates the visible header, hero, browser title, splash product name, logo alternative text, CSV/PNG branding, and PDF header/footer. Accent the last two words of a customized lab name in the hero. Store both names in the current project and restore them on project load.

Place **Export PDF** in the Project action row immediately to the right of **Load project**. At the top of Summary, keep **Export PNG** and **Export CSV** on one non-wrapping horizontal line. Do not include the word “complete” in the labels. Give the Summary toolbar clear breathing room above and below, approximately 18–20 px of vertical padding.

**Export PDF** builds a real multi-page A4 PDF locally without external libraries or uploads. Every page uses a clean light print palette, the configurable tool name (default `ИH Custom Winds`) at upper left, the logo at upper right, and a section title. The footer contains only the configurable lab name; it has no separator, timestamp, or page number. Embed a compact copy of the logo as a data URL specifically for PDF rendering; never draw the external `logo.png` element into the PDF canvas, because that can taint canvases and make `toBlob()` fail with an insecure-operation error under `file://`. Pages 1–2 contain Project Information: project metadata without Project ID, customer record, pickup properties, Bode sweep-point selection, and measurement settings. Created and Updated use European `DD.MM.YYYY` formatting. Pickup ID is the first field in the PDF Pickup section. Render Guitar, Bass, Single Coil, Humbucker, Clockwise, and Counterclockwise as checked or empty boxes in three vertical pairs: Guitar above Bass, Single Coil above Humbucker, and Clockwise above Counterclockwise. Page 3 places Bode response above Relative phase, and page 4 places Saturation above Spectrum. The page-4 section is titled **Spectrum Data** and contains the measured spectral-waterfall graph plus the Spectrum metrics; Relative phase remains data-only. The Bode PDF graph uses the same minimum-at-0 positive scale and marked fitted resonance as the application, and lists fitted resonance, strongest measured bin, and fit uncertainty. In every Harmonics vs Drive rendering, Even is red and Odd is green. All graphs have labelled x/y values. Append an Annex titled `Measurement glossary`, spanning as many pages as needed, containing every displayed measurement term and the exact explanatory text from its tooltip. Include all 28 displayed measurement fields. Download as `<safe-name>-complete-record.pdf`.

## Canvas requirements

All graphs use `<canvas>` with backing-store scale capped at `min(devicePixelRatio, 2)`. Use `ResizeObserver`. Every `.canvas-box` must set equal `height`, `min-height`, and `max-height`, plus `overflow:hidden`, so data can never enlarge the graph.

Every graph supports pointer hover/drag:

- Map cursor position to plot coordinates.
- Find the closest data value.
- Draw a vertical marker.
- Render a theme-aware tooltip inside the canvas.
- Clear it on pointer leave.

Use logarithmic x mapping for spectrum plots and appropriate log-dB y scales.

## Spectrum

UI includes:

- Presets: Pickup focus 500–8,000 Hz; Guitar/bass 40–8,000 Hz; Full audio 20–20,000 Hz; Custom
- Editable numeric low/high Hz controls
- Durations: 2.5, 5, or 10 seconds; default 5
- **Measure spectrum**
- Progress bar
- One fixed-height logarithmic graph titled **Measured frequency spectrum**, plotting the averaged measured response across the selected frequencies
- One fixed-height **Spectral waterfall** graph plotting the same measured frequencies over capture time, with frequency from left to right, time from top to bottom, and relative level encoded from −90 dB to 0 dB by color
- 16 metric cards

Changing numeric endpoints switches the preset to Custom. Clamp high frequency below Nyquist. Generate local white noise and pass it through high-pass and low-pass biquads with Q about 0.707, then through test-level gain to the system-default output. Capture selected-channel input during the run. Stop safely on cancellation.

Average several 8192-point Hann FFT power frames (roughly 4–16 depending on duration). Store a plot downsampled to at most about 1200 points, normalized so the strongest selected-band point is 0 dB. Also retain 12–28 evenly spaced 4096-point measured frames, each compacted to 96 logarithmically spaced frequency cells and normalized against the strongest waterfall cell, so the waterfall persists in localStorage and project files.

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

Every result value in Spectrum, Saturation, Bode response, and Phase includes a keyboard-focusable `?` button with detailed explanation text. Every graph heading also includes a `?` button explaining the graph's role, how to read it, and its main confounder. The Summary copies retain these controls. Use one global, theme-aware, fixed-position `role="tooltip"` element. Show it on `mouseenter`, `focus`, and `click` so it works on touch screens; position it above or below without leaving the viewport. Hide it on `mouseleave`, `blur`, outside pointer press, or Escape. Style the tooltip as a large panel up to roughly 520 px wide with about 18 × 22 px padding, 14 px text, a 15 px radius, translucent blurred glass, and the same warm-orange border and glow treatment as the centered toaster message in all four themes.

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

Provide a native **Sweep points** dropdown with 20, 30, 40, 50, and 60; default to 60 and store the selection in project settings. Treat this value as analysis density, not as the number of separately emitted tones. Use the selected test-output level unchanged throughout the sweep.

Emit one phase-continuous logarithmic chirp from 500 Hz to 8000 Hz, with brief endpoint holds and approximately 55 ms fade-in/fade-out ramps so the excitation has no stepped-frequency discontinuities or abrupt endpoint peaks. Capture the entire return once. Locate the returned sweep using the audio API latency estimate plus a bounded onset search. Analyze the requested high-frequency-dense exponential point schedule from overlapping local chirp windows, use windowed RMS medians, compare them with the learned input-noise profile, and subtract noise in the power domain. Require at least 60% of the requested points to clear the noise floor; otherwise fail with routing/gain guidance.

Interpolate rejected gaps only for curve continuity and exclude them from the direct-point count and peak selection. Apply a local median outlier guard plus light three-point smoothing before candidate detection so a single noise spike cannot become the resonance. After the normal point schedule is complete, identify the strongest direct candidate and add nine closely spaced log-frequency analysis points between its neighboring normal bins, sampled from the same captured chirp. Keep the graph hidden through this adaptive refinement and publish all normal and refinement points only after successful completion. During the chirp, the top-right status field shows the instantaneous frequency plus live input dBFS. During post-analysis and refinement, it shows the point frequency plus measured dBFS, never the commanded test-output value.

Normalize the completed curve by subtracting its lowest robust value and present it on the established 1:6 display scale with a minimum of exactly 0. Draw the Gaussian-smoothed curve first, then draw the measured robust line and points above it at roughly 80% opacity so the original response is only slightly dimmed and remains clearly visible. Provide a native **Curve smoothing** range control from 0% to 100%, default 45%, and calculate smoothing in logarithmic-frequency space so its bandwidth is consistent by octave. Use a strongly progressive slider mapping so low and middle settings retain much more local variation and strong smoothing is concentrated near the upper end. Smoothing is display-only: it must not change the resonance fit, uncertainty, measurement arrays, result cards, or CSV raw values. Store the setting as `bodeSmoothing`, restore it on load, redraw the source and Summary plots live, and apply the selected overlay to PNG and PDF Bode graphs.

Fit a quadratic curve in log-frequency through the strongest local seven direct points, using five when only five are available. Report the fitted resonance frequency, the strongest actually measured bin, and a conservative plus/minus uncertainty that combines half the closest bin spacing with leave-one-out fit variation. If a concave in-range fit is impossible, explicitly retain the strongest-bin fallback in saved/exported fit metadata. Use the same scale for the graph, fitted peak marker, peak-above-minimum value, endpoint tilt, PNG, and PDF. Keep both raw relative dB and the displayed value in CSV, plus the refinement flag and fit metadata. Also report endpoint tilt and direct/total point count. This is magnitude-only. Every graph retains readable x- and y-axis tick values before data exists.

### Relative phase

Keep five shaped low-level pulses. Capture enough pre/post time for common interface latency, locate strongest excursion, keep a normalized 30 ms view, and vote on sign. Report POSITIVE, NEGATIVE, or INDETERMINATE when response is below about −80 dBFS or fewer than four votes agree.

All output-producing tests require an input connection.

## Project schema

Use version 2:

```js
{
  version: 2,
  id, name, notes, created, updated, // dates stored as DD.MM.YYYY
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
    noiseLow, noiseHigh, noiseDuration, bodeSteps, bodeSmoothing
  },
  noise: null | { low, high, duration, sampleRate, spectrum, metrics },
  saturation: [],
  bode: [],
  bodeFit: null,
  polarity: []
}
```

Save as pretty JSON data named `<safe-name>.custom-winds`, using no additional `.json` suffix. Load version 2 and migrate compatible version-1 projects by setting missing Spectrum data to null and missing customer/pickup records to the current form defaults. Explicitly discard legacy impulse result and impulse-count fields during normalization so they do not persist into a new save. Continue accepting legacy `.pickup-health` files. Restore all relevant controls and redraw every result.

## Local persistence

Persist the complete serializable application state in `localStorage` under the versioned key `ih-custom-winds.local-state.v1`. The payload contains the entire version-2 project including all measurement arrays, plus UI state for theme, active tab, preferred input-device ID, and preferred input channel. Debounce form/control writes, save immediately before page exit and explicit JSON download, and update local state after project import, measurement completion, clearing, theme changes, and tab changes. On startup, validate and normalize the stored project, migrate legacy ISO dates, restore every compatible control and graph, and ignore/remove only this app's key if parsing or validation fails. Report storage quota/security failures once without preventing the app from running.

Do not persist live `MediaStream`, Web Audio nodes, active generators/tests, sample ring buffers, or the learned input noise/calibration profile. Audio must reconnect through user permission and perform the required route-change calibration after reload. A missing stored device should fall back safely while keeping the app usable.

CSV export includes customer and pickup records, project metadata and notes, the complete Summary overview, every displayed measurement, white-noise spectrum, saturation harmonic/transfer rows, Bode measured noise-subtracted dBFS, actual output dBFS, robust-filtered dBFS, positive raw relative dB, displayed relative value, SNR, learned-noise dBFS, interpolation/refinement flags, fitted-resonance metadata, and all phase pulse waveforms.

## Summary and PNG

Summary cards include:

- Bode resonance
- Saturation signature
- Relative phase
- Measurement record

Do not place a Spectrum overview card at the top of Summary; its detailed measurements remain available in its section below.

Below the cards, Summary contains four separated, labelled result sections in this order: Bode response, Phase, Spectrum, and Saturation. Together they contain synchronized copies of all six graphs and every detailed measurement. The original graphs and measurements remain visible in their source tabs.

PNG is a tall, complete report canvas at 2× backing scale using the current theme. It contains the four overview cards and their notes, project notes, all 28 detailed measurement values, and all six graphs in Summary order: Bode magnitude, five phase pulse responses, averaged spectrum, spectral waterfall, harmonics versus drive, and transfer curve.

CSV contains every item represented by Summary and the raw series needed to reconstruct every graph in Summary order: overview values and notes; complete Bode rows with noise/SNR/interpolation metadata; phase votes and pulse waveform samples; raw white-noise metrics, spectrum, and waterfall cells; and saturation harmonic/transfer rows.

## Error handling and cancellation

- Refuse output without an input connection.
- Disable all run buttons, **Measure All**, **Clear measurements**, and the 440 Hz button during a test or Measure All sequence. Keep Stop available; stopping a batch cancels its remaining stages.
- Keep Stop available.
- Cancellation clears the active-test marker; loops check it after every short wait.
- Always ramp output down in `finally` and on `beforeunload`.
- Show concise toasts for permission denial, missing input, invalid project, completion, and cancellation. Toasts are large and centered in the viewport, with a translucent blurred panel, theme-colored border/dot/glow accents, centered text, and a subtle scale/vertical entrance transition.
- Never manufacture or simulate results when signal is absent.

## Accessibility and responsive behavior

- Use semantic headings, labels, native inputs/selects/buttons, tab roles, status regions, and visible focus.
- Buttons have a minimum practical height of about 38 px. Every native dropdown and single-line text or number input has an explicit, matching 40 px height; multiline textareas remain vertically resizable.
- Measurement and graph explanation tooltips work by keyboard focus, hover, and touch click; outside press and Escape dismiss them.
- Respect `prefers-reduced-motion`.
- Avoid horizontal page overflow down to 300 px.
- Metric grid is four columns on wide screens, three at medium width, two on tablets, and one on narrow phones.
- Spectrum options and measurement-status controls stack responsively.
- Plot heights remain fixed on every breakpoint.

## README requirements

Document:

- Local-server startup and privacy
- Fixed system-output behavior
- 440 Hz workflow
- Electrical, thermal, feedback, hearing, and instrument-finish safety
- Air-core driver construction using a nonmagnetic former, roughly 0.25–0.35 mm wire, 220–350 turns, commonly 6–12 Ω measured DCR, twisted strain-relieved leads, optional gapped shield, and strict amplifier-load caveats
- Input preparation and repeatable geometry
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
7. Splash is visible on Dark blue reload and does not call `getUserMedia()` automatically.
8. The visible tabs are Bode response, Phase, Spectrum, Saturation, Summary, and Settings; no Impulse / Tap UI or results section exists.
9. White-noise duration offers exactly 2.5, 5, and 10 seconds.
10. Frequency span is selectable and custom endpoints are editable.
11. All 16 Spectrum metrics and all 12 scalar results from the other tests exist with nonempty detailed explanation text.
12. Every graph heading has a detailed explanation button; the single global tooltip is accessible by focus, hover, and touch click and dismisses on outside press or Escape.
13. Every plot has cursor inspection and fixed height.
14. Canvas DPR is capped at 2.
15. Project version 2 contains complete Spectrum data and preserves the selected Bode sweep-point count and Bode display-smoothing level. Legacy impulse results and settings are discarded on load.
16. CSV, PNG, and PDF contain no impulse data, waveform, metric, or section.
17. One button cycles through Light, Dark orange, Dark green, and Dark blue; Dark blue is the first-run default, the restored theme redraws every plot, and exports use the current theme.
18. Desktop and mobile layouts have no horizontal overflow.
19. At runtime the four source tabs retain six original canvases and all result cards; Summary contains six additional synchronized canvases and copied result cards grouped into four sections.
20. No measurement tab contains an Open Summary copy box; **Export PDF** sits beside **Load project**, while Summary buttons read **Export PNG** and **Export CSV**, remain on one horizontal line, and have space above and below.
21. A glowing, theme-accented **Measure All** button sits immediately left of **Clear measurements**, runs Bode → Phase → Spectrum → Saturation sequentially with automatic tab changes, returns to Bode, and shows a final completion toaster.
22. Complete PNG includes four overview cards, all 28 measurements, project notes, and all six graphs; complete CSV includes all displayed information and raw data for every graph, including time/frequency/level waterfall cells.
23. Large explanation tooltips use the same orange glass, blur, border, and glow language as toaster messages.
24. Settings defaults to `ИH Custom Winds` and `Nicks Pickup Lab`; Apply updates the UI and all exports, and saved projects preserve both names.
25. PDF places Bode above Relative phase on page 3 and Saturation above Spectrum on page 4, names the section **Spectrum Data**, includes the measured spectral waterfall there, keeps Relative phase data-only, colors Even red and Odd green in Harmonics vs Drive, arranges checkbox pickup selections in the requested vertical pairs, uses the lab name alone in the footer, contains no page numbers or footer timestamps, contains no Impulse / Tap page, and appends a complete tooltip-derived measurement glossary annex.
26. Every input-device or input-channel change first resets Input trim to 0 dB and Output level to −30 dBFS, removes the previous route correction, shows the blocking **Calibrating, please wait.** overlay, and captures exactly one quiet profile lasting no more than three seconds; a baseline louder than −70 dBFS causes one whole-dB Input-trim reduction and matching Output increase within safe limits, with no verification passes; measurement launch and route changes are locked during calibration, route changes are locked during measurements, and no measurement recalibrates or automatically moves either level control; the INPUT meter marks −70 dBFS in green and −12 dBFS in red.
27. Bode emits one phase-continuous logarithmic 500 Hz–8 kHz chirp with smooth endpoint fades; offers 20/30/40/50/60 normal analysis points with 60 default and high-frequency-dense exponential spacing; uses learned-noise power subtraction; keeps the selected output level constant; adds nine adaptive analysis points around the candidate peak from the same capture; hides partial curves; shows frequency plus measured dBFS in the top status; publishes a robust minimum-at-0 positive curve only after completion; dims that raw curve beneath a brighter 0–100% adjustable logarithmic-frequency smoothing overlay (45% default) in UI, Summary, PNG, and PDF without changing fitted results; fits the strongest local 5–7 points in log-frequency; and reports/exports fitted resonance, strongest measured bin, and uncertainty.
28. Browser console has no startup errors.
29. Every date uses exactly `DD.MM.YYYY`, including saved-project Created/Updated fields, Wind Date, Summary measurement dates, CSV Created/Updated fields, and PDF Created/Updated fields. Loading migrates legacy ISO timestamps to this format.
30. Versioned `localStorage` persistence restores the full project, every measurement array, settings, branding, theme, active tab, and preferred input route after reload; malformed/quota-blocked storage fails safely, while live audio and route calibration remain session-only and are relearned after reconnection.
