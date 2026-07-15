# Reconstruction Prompt — Nicks Pickup Lab

Use this document as the complete implementation brief for rebuilding the current application from scratch. Do not rely on prior conversation history.

## Objective

Build **Nicks Pickup Lab**, a polished, responsive, single-file browser application for measuring passive or active guitar/bass pickups through an audio interface and a repeatable magnetic driver coil.

The application must provide:

- Live time-domain and frequency-domain analysis
- Input and output meters
- Input/output device and channel routing
- A controllable excitation generator
- Magnetic saturation mapping
- A 500 Hz–8 kHz Bode magnitude measurement
- Relative pickup polarity detection
- A measurement summary with PNG and CSV export
- Dark and light themes
- A detailed README explaining use and magnetic-driver construction

## Deliverables

Create these files in one folder:

```text
pickup-lab.html   Entire application, including CSS and JavaScript
README.md         User guide, safety notes, workflows, and magnetic-driver instructions
PROMPT.md         This reconstruction specification
```

The application itself must be completely contained in **one HTML file**. Do not use a build system, framework, package manager, external JavaScript library, remote font, image, stylesheet, module, server API, upload endpoint, or telemetry service.

## Non-negotiable behavior

1. All audio processing is local in the browser.
2. Never request microphone/audio-input permission automatically.
3. Show a splash permission modal on load, but call `getUserMedia()` only when the user clicks **Allow audio input**.
4. The **Not now** button only dismisses the modal.
5. Clicking **Start analyzer** without a previously granted stream must reopen the modal without triggering permission itself.
6. Dark theme is always the initial/default theme.
7. Preserve the `PL` icon while using the title **Nicks Pickup Lab**.
8. Keep graph and oscilloscope containers fixed in size while measuring; they must never grow with data.
9. Use responsive, accessible native buttons, sliders, selects, and checkboxes.
10. Use canvas for all plots, scaled for device pixel ratio and capped at `2×` DPR.

---

## Visual design

### General style

Use a refined technical-instrument aesthetic:

- Near-black green/neutral surfaces in dark mode
- Warm orange accents throughout dark mode
- Light neutral surfaces with dark-blue accents in light mode
- Rounded panels, fine borders, restrained shadows, monospaced values, and compact controls
- Maximum shell width: `1580px`
- Desktop shell padding: `22px`; mobile padding: `12px`
- Panel radius: approximately `16px`
- Body font: Inter-style system sans-serif stack
- Numeric values and graph labels: system monospace stack

### Theme toggle

Place a compact theme button in the header beside the status pill.

- Dark-state label: `☀ Light theme`
- Light-state label: `☾ Dark theme`
- Update `aria-pressed`
- Do not persist the selection; reloading starts in dark mode
- Redraw all visible canvases after a theme change
- PNG summary export uses the currently selected theme

### Core colors

Use theme variables. The important current palette is:

```css
/* Dark, default */
--bg: #0a0d0c;
--panel: #111715;
--panel-2: #151d1a;
--line: #28342f;
--ink: #e7eee9;
--muted: #93a29a;
--lime: #ffb24a;          /* secondary orange accent */
--primary-fill: #f28c28;  /* primary orange */
--cyan: #ff7a3d;          /* graph-trace orange */
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
--lime: #173f68;          /* secondary dark blue */
--primary-fill: #214f7b;  /* primary dark blue */
--cyan: #0b5b96;          /* graph-trace blue */
--amber: #a75b00;
--red: #cb3449;
--canvas-bg: #f8faf9;
--canvas-grid: #d9e1dd;
```

Use theme variables for every canvas fill, grid, trace, marker, tooltip, panel, export, glow, and label. Dark mode background glows must be orange; light mode background glows must be blue.

### Responsive layout

Desktop top row:

```css
grid-template-columns:
  minmax(300px, 1.2fr)
  minmax(390px, 2.4fr)
  minmax(64px, .18fr);
```

The columns are:

1. Input
2. Oscilloscope + spectrum
3. Meters

The meter panel is intentionally about one-third of its former width. On desktop, stack the Input and Output meters vertically in the narrow column. Put each `Input` or `Output` label above its meter bar and its dBFS value below.

At `1120px` and below:

- Use two top columns for Input and Oscilloscope + spectrum
- Move the Meters panel to a full-width row
- Put Input and Output meters side by side
- Render them as horizontal meters
- Display live measurements in four columns

At `760px` and below:

- Use one column for the main and lower layouts
- Display live measurements in two columns
- Stack summary sections
- Use two columns for measurement result strips

### Fixed graph sizing

The combined scope/spectrum panel must retain a fixed internal layout:

- Minimum combined plot height: about `332px`
- Oscilloscope height: exactly `208px`
- Spectrum takes the remaining height, with a minimum near `124px`
- Use CSS containment so canvas backing-store changes cannot grow the layout

---

## Page hierarchy and exact labels

### Permission modal

Show on page load:

- Kicker: `Audio permission`
- Heading: `Connect your audio interface`
- Explain that the app needs microphone access for the Hi-Z/instrument input and does not upload audio
- Safety notice recommending an interface Hi-Z input and low monitoring/gain
- Buttons: **Allow audio input**, **Not now**
- Text: `The browser permission prompt appears only after you click “Allow audio input”.`

### Header

- Square rounded gradient icon containing `PL`
- Heading: `Nicks Pickup Lab`
- Subtitle: `Single-file pickup measurement workbench`
- Theme button
- Status pill with dot and status text

### Top row: Input

Panel title: **Input**

Controls, in this order:

| Control | Values/default |
| --- | --- |
| Input device | Permission required until access is granted; then enumerate all audio inputs |
| Channel | `Input 1`, `Input 2`, `1 + 2 mono`, `1 − 2`; default Input 1 |
| FFT size | `4096`, `8192`, `16384`, `32768`; default `16384` |
| Input trim | −24 to +24 dB, step 0.5, default 0.0 dB |
| Analysis smoothing | 0–95%, step 1, default 65% |
| Measurement averaging | 0–30 seconds, step 0.5, default 30.0 seconds; show `Realtime` at 0 |
| Noise floor threshold | −90 to 0 dBFS, step 1, default −80 dBFS |
| Monitor input to output | Off by default; label includes `(feedback risk)` |

Buttons:

- **Start analyzer** — primary accent
- **Stop** — danger styling, initially disabled
- **Freeze trace** — initially disabled; toggles to `Resume trace`

Include the notice:

`Microphone DSP is requested off. The OS or interface driver can still apply processing; use a raw audio interface input where possible.`

### Top row: Oscilloscope + spectrum

Panel title: **Oscilloscope + spectrum**

- Header state: `live` or `frozen`
- Legend: `input`, `held peak`
- Top canvas: Input waveform, fixed 208 px height, Y labels +1.0, 0, −1.0
- Bottom canvas: normalized log-frequency spectrum from 20 Hz to 20 kHz or Nyquist, whichever is lower
- Spectrum Y display: normalized 0 to −72 dB relative to the current peak
- Current trace and decaying held trace
- Vertical marker at detected peak frequency
- Annotation: `normalized · 0 dB = <absolute peak dBFS> dBFS peak`

When no spectrum bin is above the selected threshold, show a prominent centered rounded callout inside the spectrum graph:

```text
No Signal
Select input and launch generator or measurement
```

The box must:

- Be visible before audio starts, after stopping, and whenever no signal exceeds the threshold
- Use the theme panel background
- Use the primary accent border, glow, and title
- Scale the second line down if required so it fits on narrow screens

### Top row: Meters

Panel title: **Meters**, kicker `dBFS`

- Very narrow desktop panel: computed desktop width around `64px` at the tested viewport
- Stack Input and Output meters vertically on desktop
- Label each meter **Input** or **Output** above the bar
- Show dBFS readout below
- Scale −60 to 0 dBFS
- Solid `--primary-fill` only; no fill gradient
- Separate held-peak line
- Input meter follows the threshold-filtered input
- Output meter shows the output bus
- On narrower layouts, change the bars to horizontal using width and left-position updates

### Live Measurements

Put all metric cards inside one outer panel titled **Live Measurements**, with kicker `real-time analyzer`.

There are exactly 24 cards in this order:

| # | Label | Unit |
| --- | --- | --- |
| 1 | Peak frequency | Hz |
| 2 | Fundamental | Hz |
| 3 | RMS level | dBFS |
| 4 | Sample peak | dBFS |
| 5 | Crest factor | dB |
| 6 | DC offset | % FS |
| 7 | Noise floor | dBFS |
| 8 | SNR estimate | dB |
| 9 | Spectral centroid | Hz |
| 10 | 85% roll-off | Hz |
| 11 | Spectral bandwidth | Hz |
| 12 | Spectral flatness | 0…1 |
| 13 | Spectral slope | dB/oct |
| 14 | THD estimate | % |
| 15 | Even / odd | dB |
| 16 | Peak asymmetry | dB |
| 17 | Zero crossings | / sec |
| 18 | Clipped samples | % |
| 19 | Transient index | dB |
| 20 | Nearest note | cents |
| 21 | Low band | % |
| 22 | Mid band | % |
| 23 | High band | % |
| 24 | Tone confidence | % |

Use tooltips on cards to explain each measurement. Render unavailable/rejected values as `—` and do not let old averaged values leak through after the current value is rejected by the noise threshold.

### Lower left: Output Generator

Panel title: **Output Generator**, kicker `use with driver coil`

| Control | Values/default |
| --- | --- |
| Signal | Off, Sine, Square, White noise, Pink noise; default White noise |
| Output device | System default plus every browser-exposed audio output |
| Output channel | Dynamically generated from the destination channel count; `Outputs 1 + 2` plus individual channels |
| Frequency | 20–12000 Hz, step 1, default 440 Hz |
| Output level | −60 to 0 dBFS, step 0.5, default −3.0 dBFS |

Buttons:

- **Find devices** / `Refresh (N)`
- **Start generator** — primary style, orange in dark mode like Start analyzer
- **Mute** — danger style

Include this safety notice:

`Fixture: interface line/headphone out → current-limited driver coil → magnetic field → pickup → Hi-Z input. Do not connect an interface output directly to the pickup. The requested −3 dBFS default is hot: reduce the interface/headphone gain before starting.`

### Lower right: measurement tabs

Tabs:

1. Magnetic Saturation Mapper
2. Bode plot
3. Polarity
4. Test setup

Only one tab panel is visible at a time. Redraw its canvas after selection.

### Measurement summary

Full-width panel below the lower section:

- Title: **Measurement summary**
- Initial state: `not created`
- Buttons: **Create summary**, **Export PNG**, **Export CSV**
- Export buttons disabled until at least one valid value exists
- Placeholder: `Run measurements, then create a snapshot containing every available non-null result.`

### Footer

Left:

`Nicks Pickup Lab · local processing only · no uploads · no external libraries`

Right:

`Measurements are dBFS/referenced to the fixture unless calibrated externally.`

---

## Audio permission and device routing

### Input permission

On **Allow audio input**, call:

```js
navigator.mediaDevices.getUserMedia({
  audio: {
    echoCancellation: false,
    noiseSuppression: false,
    autoGainControl: false,
    channelCount: { ideal: 2 },
    sampleRate: { ideal: 48000 }
  },
  video: false
});
```

After permission:

- Store the stream
- Enumerate inputs and outputs
- Select the stream's current input device
- Hide the modal
- Update status to permission granted
- Do not start the analyzer automatically

Changing the input device must reacquire the stream with the selected exact `deviceId`. If the analyzer was running, stop without closing the reusable context, replace the stream, and restart.

Listen for `navigator.mediaDevices.devicechange` and refresh device lists.

### Output devices

Always include `System default`.

After permission, use `enumerateDevices()` to add every `audiooutput` exposed by the browser. The **Find devices** button should:

1. Call `navigator.mediaDevices.selectAudioOutput()` when available
2. Refresh the full output list
3. Select the returned device
4. Call `AudioContext.setSinkId()` when supported
5. Show a useful status if the browser exposes only the system default or denies access

Changing output device must call `setSinkId()` and rebuild output-channel routing.

### Output channels

Read `destination.maxChannelCount` or `channelCount`, clamp to 1–32, and create:

- `Outputs 1 + 2` when at least two channels exist
- `Output 1` through `Output N`

Use a `ChannelMerger` in explicit/discrete mode. Route the mono output analyzer to both channels for stereo or only the selected discrete channel.

---

## Web Audio graph

Create the `AudioContext` only after the user starts the analyzer and a stream exists. Use `latencyHint: "interactive"`.

### Input graph

```text
MediaStreamSource
  → ChannelSplitter(2)
  → selected channel / sum / difference
  → Input Gain
      ├─→ Input Analyser
      ├─→ ScriptProcessor capture path
      └─→ Monitor Gain → Output Bus
```

Channel modes:

- Input 1: splitter channel 0
- Input 2: splitter channel 1
- `1 + 2 mono`: two gains of +0.5 summed
- `1 − 2`: channel 0 at +0.5 and channel 1 at −0.5

### Analyzer settings

Input analyzer:

- FFT size from UI
- Smoothing from UI
- `minDecibels = -120`
- `maxDecibels = 0`

Output analyzer:

- FFT size 2048
- Smoothing 0.55

Use a deprecated `ScriptProcessorNode(2048, 1, 1)` only for measurement capture compatibility in this single-file implementation. Connect it through a zero-gain node to the destination so processing callbacks continue.

### Monitor safety

Monitoring is off by default. Toggle the monitor gain with a short `setTargetAtTime` ramp. Clearly label feedback risk.

---

## Live analysis algorithms

Use float time-domain and frequency-domain analyzer data on each animation frame.

### Noise-floor filtering

The threshold slider is globally visible in the Input panel.

- Time-domain gate: calculate raw frame RMS; if its dBFS is below the threshold, replace the entire analysis/scope frame with zeros
- Spectrum gate: keep only bins whose absolute analyzer dBFS is at or above the threshold; replace others with −120 dB
- Determine `hasSpectrum` only from 20 Hz to the lower of 20 kHz or Nyquist
- Input meter displays zero when the time gate is closed
- If time stats are gated, set RMS, peak, DC, clipping, ZCR, crest, asymmetry, and transient values to `NaN`
- If no spectrum exists, set spectral metrics to `NaN`
- Clear measurement history, RMS envelopes, and held spectrum whenever the threshold changes

### Averaging

- Slider range 0–30 seconds, default 30
- Keep a timestamped history of measurement objects
- Remove frames older than the selected window
- Average every finite numeric metric independently
- Do not average `peakBin`, `binHz`, booleans, or non-numbers
- If the current metric is non-finite, keep it non-finite rather than showing older history
- Clear history when the window changes

### Time-domain measurements

Calculate:

- RMS: square root of mean squared samples
- Sample peak: largest absolute sample
- Positive and negative waveform peaks
- DC offset: arithmetic mean
- Clipped samples: percentage with absolute value ≥ 0.995
- Zero-crossing rate: sign changes × sample rate / frame length
- Crest factor: `20 log10(peak / RMS)`
- Peak asymmetry: `20 log10(positivePeak / abs(negativePeak))`
- Transient index: short RMS envelope versus long RMS envelope in dB

Envelope constants:

```js
short = 0.82 * short + 0.18 * rms;
long  = 0.985 * long + 0.015 * rms;
```

### Spectral measurements

Analyze 20 Hz through `min(16000, sampleRate * 0.48)`.

- Find largest FFT bin
- Apply three-point parabolic interpolation around the peak
- Estimate the fundamental by scoring possible subharmonics `peakBin / 1…6` against up to six harmonics
- Convert dB bins to power with `10^(dB/10)`
- Noise floor: median spectrum bin from 80 Hz through analysis maximum
- SNR: peak-bin dB minus estimated noise-floor dB
- Spectral centroid: power-weighted frequency mean
- Spectral bandwidth: power-weighted standard deviation around centroid
- 85% roll-off: first frequency reaching 85% cumulative power
- Spectral flatness: geometric mean divided by arithmetic mean of power
- Spectral slope: least-squares dB slope versus `log2(f / 1000)`
- THD estimate: harmonics 2–8 relative to fundamental amplitude
- Even/odd balance: `10 log10(even harmonic power / odd harmonic power)`
- Low band: 20–150 Hz
- Mid band: 150 Hz–2 kHz
- High band: 2–16 kHz
- Tone confidence: clamp `(peak dB − noise dB − 6) × 2.2` to 0–100
- Nearest note: MIDI note calculation using A4 = 440 Hz, including cents offset

### Scope and spectrum drawing

- Scope uses the filtered frame
- Spectrum X axis is logarithmic, 20 Hz–20 kHz
- Spectrum Y axis is normalized to its highest surviving bin
- Display range is 0 to −72 dB relative to peak
- Held spectrum decays by approximately 0.12 dB per animation frame and is independently normalized
- Freeze prevents analyzer buffers and held trace from updating but keeps rendering

### Meters

- Meter scale: −60 to 0 dBFS
- Input/output peak-hold decay multiplier: approximately `0.986` each animation frame
- Fill is a single accent color
- Peak marker is a thin theme-ink line

---

## Generator

All generated test signals connect through a gain node to the common output bus.

### Sine and square

Use an oscillator with UI-selected type and frequency. Smooth frequency and level changes using short `setTargetAtTime` ramps.

### White noise

Create a reusable two-second looping audio buffer with random samples scaled to about `0.35`.

### Pink noise

Use a standard multi-pole filtered white-noise approximation with state variables and output scaling around `0.11`. Loop a two-second buffer.

The start button toggles to `Stop generator`. The separate Mute button stops the source.

---

## Magnetic Saturation Mapper

### UI

- Description: increasing-field transfer test
- Test frequency: 80–3000 Hz, default 440 Hz
- Maximum drive: −30 to −3 dBFS, default −6 dBFS
- Drive steps: 8, 12, 16; default 12
- Buttons: **Run saturation map**, shared **Abort active test**
- Progress bar and status
- Canvas: magnetic saturation transfer plot
- Results:
  - Onset
  - Max compression
  - Max asymmetry
  - THD at max

### Procedure

1. Stop any continuous generator.
2. Create a sine oscillator at the selected frequency.
3. Generate linearly spaced drive values from −42 dBFS to selected maximum.
4. At each step:
   - Ramp gain with time constant about 25 ms
   - Wait 260 ms
   - Capture 360 ms
   - Calculate RMS, positive peak, negative peak, Goertzel fundamental, and harmonics 2–8
5. Low-level reference gain is `dB(RMS at first point) − first drive`.
6. Compression at each point is measured gain minus reference gain.
7. Onset is the first drive with compression below −1 dB.
8. Asymmetry is positive versus absolute negative peak in dB.
9. Report most negative compression, largest absolute asymmetry, and last-point THD.

Plot pickup output dBFS versus drive dBFS, plus a dashed ideal linear reference. Make markers red when absolute asymmetry exceeds 1 dB; otherwise use the secondary accent.

State clearly that output dBFS is a repeatable field-strength proxy, not gauss.

---

## Bode plot

### UI

- Heading: `500 Hz–8 kHz magnitude response`
- Level at 500 Hz: −48 to −6 dBFS, default −6 dBFS
- Sweep duration choices: 2.5 s, 5 s, 10 s; default 2.5 s
- Explain that excitation falls by 6 dB/octave, approximately half voltage per octave
- Button: **Measure Bode plot**
- Progress/status
- Results:
  - Peak magnitude
  - 8 kHz / 500 Hz
  - Measured slope
  - Excitation slope (`−6.0 dB/oct`)

### Sweep generation

- Logarithmic sweep only from 500 Hz to `min(8000, sampleRate × 0.44)`
- Base level is selected at 500 Hz
- Apply `−6 dB × log2(f / 500)` amplitude contour
- Use approximately 30 ms fade-in/out
- Capture with about 120 ms pre-roll and 650 ms post-roll

### Deconvolution

- Build a stimulus array aligned at pre-roll
- Zero-pad stimulus and recording to next power of two
- Implement an in-file radix-2 complex FFT
- Divide recorded FFT by stimulus FFT with a small denominator regularizer
- Store magnitude in dB

### Display trace

- Generate 600 logarithmically spaced points from 500 Hz to 8 kHz
- Apply light 1/48-octave smoothing by amplitude-averaging within ±1/96 octave
- Normalize all values to the smoothed 500 Hz point
- Auto-scale Y range in 6 dB increments
- Keep at least 24 dB and at most 72 dB visible range
- X ticks: 500, 1k, 2k, 4k, 8k
- Draw a 0 dB reference line
- Find the highest smoothed value
- Mark the peak with a highlighted circle and a theme-aware label formatted like:

  ```text
  +3.2 dB / 2.45 kHz
  ```

- Place the annotation on whichever side avoids clipping

---

## Relative polarity

### UI

- Pulse level: −48 to −9 dBFS, default −9 dBFS
- Averages: 4, 8, 16; default 8
- Button: **Determine relative polarity**
- Progress/status
- Centered polarity-response graph
- Results:
  - Relative polarity
  - Confidence
  - First excursion
  - Peak response

Use only these classification labels:

- `POSITIVE ↑`
- `NEGATIVE ↓`
- `INCONCLUSIVE`

Do not use the word `REVERSED`.

### Pulse and detection

- Pulse duration about 12 ms
- Positive-leading shape: linear rise over first 8% followed by exponential decay with factor about 5.5
- Capture window: 260 ms
- Start pulse approximately 30 ms into capture
- Average selected number of captures
- Wait approximately 80 ms between pulses
- Estimate noise RMS from first 25 ms
- Detection threshold: maximum of `noise × 5` and `8% of full captured peak`
- Find first sample beyond threshold after noise window
- Search for peak within the next 30 ms
- Confidence: clamp `(peak / noise − 3) × 6` to 0–99
- Positive first excursion → POSITIVE; negative → NEGATIVE
- Positive result uses positive accent; negative uses red

Center the impulse in the graph. Show approximately a 100 ms span centered on the detected first excursion, or on the largest impulse when detection is inconclusive. Draw positive and negative detection thresholds and a vertical impulse-center marker.

Explain that polarity is relative to driver winding, driver face, output wiring, magnet face, and pickup leads.

---

## Test setup tab

Show five numbered instructions:

1. **Build a repeatable magnetic driver** — fix a small coil above the pickup at a recorded height/orientation and add suitable current limiting.
2. **Define positive** — mark coil winding direction, face toward pickup, cable polarity, magnet face, and pickup hot lead.
3. **Set clean gain** — use Hi-Z, disable DSP/AGC, avoid interface clipping, and run low-level first.
4. **Validate with loopback** — use an attenuated electrical loopback to detect interface compression/asymmetry.
5. **Control the load** — record cable capacitance, pot values, tone network, and input impedance.

---

## Graph pointer tooltips

Attach pointer-move and pointer-leave handlers to every canvas:

- Oscilloscope: time in ms and full-scale amplitude
- Spectrum: logarithmic frequency and relative dB
- Saturation: drive dBFS and output dBFS
- Bode: frequency and dB relative to 500 Hz
- Polarity: time from impulse center and full-scale response

Show a floating theme-aware tooltip next to the pointer and clamp it inside the viewport.

---

## Measurement capture and test coordination

- Only one active measurement test at a time
- Stop the continuous generator before each measurement
- Disable all test buttons during a test
- Shared abort button rejects an active capture and restores buttons
- Capture samples through the input `ScriptProcessorNode`
- Use progress bars and descriptive status messages
- Stopping the analyzer aborts tests and generator

---

## Summary and export

### Collection

Create a snapshot with four sections:

1. Magnetic Saturation Mapper
2. Bode Plot
3. Polarity
4. Analyzer Metrics

Only include displayed values that are not empty, null, undefined, NaN, `—`, or negative infinity.

### On-page layout

At desktop:

- Left column: Magnetic Saturation Mapper, Bode Plot, Polarity stacked vertically
- Right column: Analyzer Metrics spanning the height

At mobile, stack all sections.

### CSV

- UTF-8 BOM
- Header: `Section, Measurement, Value, Unit`
- Quote and escape every cell
- CRLF line endings
- Timestamped filename: `nicks-pickup-lab-summary-<ISO timestamp>.csv`

### PNG

- Render a new 1600 px-wide canvas
- Use currently selected theme colors
- Header: `Nicks Pickup Lab — Measurement Summary`
- Include local creation date/time
- Left column: first three measurement sections
- Right column: Analyzer Metrics
- Dynamically calculate height
- Truncate overlong labels with an ellipsis
- Timestamped PNG filename matching CSV convention

---

## README requirements

Create a polished `README.md` containing:

- Project overview
- Localhost quick start using `python3 -m http.server 8000`
- Permission and browser notes
- Feature/measurement descriptions
- Safety warnings
- Recommended measurement order
- Limitations and privacy statement
- A full section titled **Build a repeatable magnetic driver**

The magnetic-driver section must include:

- Signal-chain diagram
- Suggested air-core coil, non-magnetic former, enamelled wire, current-limiting resistor, cable, and fixture materials
- Conservative starting ranges: roughly 8–15 mm former, 300–600 turns of 0.15–0.25 mm wire, and initially a 1 kΩ / 0.5 W or larger series resistor
- Coil winding documentation: turns, wire, DCR, inductance, face, start/finish leads
- Current and resistor-power formulas
- Warning that dBFS is not volts and actual voltage/current may need measurement
- Fixed non-magnetic mechanical jig with recorded X/Y/Z position, gap, angle, face, and rotation
- Wiring steps and strain relief
- Polarity convention
- Continuity, safe-load, low-level, loopback, repeatability, and reference-pickup checks
- Notes about pickup load, cable capacitance, temperature, fixture drift, and driver-current monitoring

Use strong warnings against direct output-to-pickup connection, shorts, power amplifiers, and mains voltage.

---

## Accessibility and interaction details

- Use semantic headings, articles, labels, buttons, tablist, dialog roles, and `aria-live` for status/summary updates
- Every input must have a visible label
- Native keyboard focus must remain visible
- Buttons must expose disabled state while unavailable
- Canvas elements need descriptive `aria-label` values
- Graph tooltips must not capture pointer events
- Escape device labels and summary content before inserting HTML

---

## Verification checklist

Before handing off:

### Static checks

- The HTML is a single standalone file
- JavaScript passes syntax checking
- No external network resources exist
- Every queried element ID exists
- Dark mode is default
- Theme toggle works both directions

### Permission checks

- Page load does not call `getUserMedia()`
- Not now dismisses without requesting permission
- Allow audio input is the only initial permission trigger

### UI/default checks

- White noise selected by default
- Output level −3.0 dBFS
- Measurement averaging 30.0 s
- Noise threshold −80 dBFS
- Saturation maximum −6 dBFS and 12 steps
- Bode level −6 dBFS and duration 2.5 s
- Polarity pulse −9 dBFS and 8 averages
- Input and Output labels appear above the meter bars
- Meter fills are solid accent colors
- Live Measurements contains exactly 24 cards, Peak frequency first and Tone confidence last

### Plot checks

- Oscilloscope remains 208 px high
- Plot container does not grow while measuring
- Spectrum is normalized and visible
- No-signal box is centered and prominent
- Bode covers only 500 Hz–8 kHz and marks peak dB/kHz
- Polarity graph is centered around impulse
- Hovering every graph shows useful X/Y coordinates

### Routing checks

- All browser-exposed outputs appear after access
- Output device selection uses `setSinkId` where supported
- Output channel list reflects destination channel count
- Stereo routes to outputs 1+2; discrete selection routes only to selected channel

### Result/export checks

- Polarity reports POSITIVE, NEGATIVE, or INCONCLUSIVE
- Summary excludes null/unavailable values
- Summary layout uses measurement sections on the left and Analyzer Metrics on the right
- PNG and CSV exports work and contain all valid values
- PNG reflects selected theme

## Final implementation standard

Do not stop at a mockup. Implement the full Web Audio routing, real-time analysis, measurement capture, algorithms, canvas rendering, interactions, device selection, responsive layout, and exports. Test the file from localhost in a current browser, inspect both themes, and fix console errors and layout overflow before considering the task complete.
