# ИH Custom Winds V3.0

A single-file browser lab for **comparative** guitar and bass pickup measurement through an audio interface and a repeatable magnetic driver (exciter) fixture. It measures a Bode magnitude response, relative phase, and a white-noise spectrum with 16 metrics. It also keeps a full winding record and compares up to six stored pickups side by side.

Everything runs locally in `index.html`: no framework, no network requests, no uploads, no analytics.

```
index.html               the complete application (HTML, CSS, JavaScript)
logo.png                 header logo
favicon.svg, favicon-32x32.png, favicon.ico, apple-touch-icon.png
scripts/generate-icons.py   rebuilds the raster icons (Pillow); not needed at runtime
README.md, PROMPT.md
```

---

## 1. Starting the app and privacy

Browsers only expose microphone input and output-device selection in a secure context. Serve the folder from **localhost** (or HTTPS):

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Then open <http://localhost:8765/> in a current Chrome or Edge. Add `?footprint=true` to the URL to turn on the Tone Footprint features (see §9).

- A splash screen appears on every load. **Nothing is requested automatically.** Microphone permission is requested only when you press **Allow audio access**. **Explore first** lets you browse, load projects and export without audio. Click the status pill at the top right later to bring the splash back.
- **AUDIO STAYS ON YOUR PC.** All capture, FFTs and fitting happen inside the page. Captured input is never routed to an audible output. The only path from input to the speakers is a zero-gain node that keeps the capture callback running.
- Your system output stays silent until you explicitly start the 440 Hz tone or a measurement.
- Storage: one `localStorage` key, `ih-custom-winds.local-state.v1`, holds the current project, the six comparison slots and UI preferences. No cookies, `sessionStorage` or IndexedDB are used. Live audio, sample buffers and the learned noise/calibration profile are never stored, so after a reload you allow audio again and the route is recalibrated.

## 2. Audio routing

**Input** group (green):

- **Input device** and **Input channel**. The channel list comes from the real channel count of the captured stream. Two channels are requested where possible, with echo cancellation, noise suppression and AGC disabled.
- **Input trim** (−48 to +18 dB), a digital gain before the meter and the capture buffer.
- **Recalibrate** (dark pole-red) repeats the quiet-input calibration for the current route.
- **INPUT meter** in dBFS. After calibration its left edge sits just above the learned quiet-input floor, so background noise leaves the bar empty and the readout shows *quiet*. Only a real signal moves it. A green line marks −70 dBFS (the calibration target) when it is inside the range, and a red line marks −12 dBFS (headroom warning).

**Output** group (blue):

- **Output device** lists *System default output* plus every distinct `audiooutput` the browser exposes.
  - A non-default device is activated with `AudioContext.setSinkId()`.
  - If only `HTMLMediaElement.setSinkId()` exists, a hidden audio element fed by a `MediaStreamAudioDestinationNode` acts as a bridge.
  - If the browser requires permission and supports `selectAudioOutput()`, the device change asks for it.
  - If no selectable-sink route exists, the app keeps the system default and says that another device needs localhost/HTTPS in a current Chrome or Edge.
- **Output channel** (Channel 1 / Left, Channel 2 / Right, Channel N…). The channel count comes from the active destination. The mono test signal passes through a discrete `ChannelMergerNode` and reaches **only** the selected hardware channel.
- **Output level** (−48 to −6 dBFS, default −30 dBFS) sets the test level used by every measurement.
- Active output is always stopped before a route change. Route selectors are locked during calibration and measurements.

### Route calibration

This runs after connecting, after every input-device or input-channel change, and when you press Recalibrate. A blocking overlay shows **Calibrating, please wait.**

1. Input trim is reset to 0 dB, Output level to −30 dBFS, and the previous profile is removed. The output stays silent.
2. After a short settle, exactly one quiet window (32768 samples, about 0.7 s at 48 kHz, never more than 3 s) is read from the same `AnalyserNode` that drives the INPUT meter.
3. The window's raw RMS (including DC), peak, band-limited noise power and persistent 50/60 Hz harmonics are learned.
4. If the baseline is louder than −70 dBFS, Input trim is reduced once by whole dB. Output level is raised by the same amount within its safe range, and any amount it could not compensate is reported. There are no verification passes.
5. The status pill shows the resulting input-noise level.

Measurements reuse this profile. They never recalibrate or move the level controls.

## 3. 440 Hz test tone

**Play 440 Hz test tone** is the only manual generator: a fixed sine with short ramps at the selected output level. Use it to confirm the exciter is wired, the right channel is selected and the input meter responds. The button toggles to **Stop 440 Hz test tone**. **Stop output** works at any time. The tone needs a connected input and is disabled while measurements run.

## 4. Safety

- **Electrical:** never connect an exciter coil directly across a line output that is not designed to drive low impedance. Drive it from a small power amplifier or a headphone amplifier rated for the coil's impedance, and keep levels low. Disconnect the coil before switching amplifiers on or off.
- **Thermal:** a small coil driven continuously can get hot. Check its temperature by touch after long sessions, and never leave it driven unattended.
- **Feedback:** keep the measured pickup's output away from the amplifier that drives the exciter. Never monitor the pickup through speakers while it is on the fixture. The app never routes input to output.
- **Hearing:** test signals can be loud on headphones or monitors. Start at −30 dBFS or lower, with the playback system turned down.
- **Instrument finish:** the fixture, magnets and tape can mark lacquer and nitro finishes. Protect the finish with a soft, non-reactive layer, and do not leave heated parts in contact with an instrument.

## 5. Building an air-core driver (exciter)

- Wind on a **nonmagnetic former** (3D-printed PLA/PETG, acrylic or phenolic), roughly the footprint of the pickup's pole-piece row.
- Use roughly **0.25–0.35 mm** enamelled copper wire and **220–350 turns**. Aim for a measured DCR of commonly **6–12 Ω**.
- Use **twisted, strain-relieved leads**, with the twist running right up to the coil and a clamp at the former.
- An optional **gapped shield** (a copper foil wrap that does not close into a shorted turn) reduces capacitive coupling. Ground it at one point only.
- **Amplifier load caveats:** many amplifiers are not stable into an almost purely resistive 6–12 Ω load with long leads, and some headphone outputs current-limit. Use a series resistor (for example 10 Ω, ≥2 W) if needed, check the datasheet's minimum load, and never short the output. A coil with too little DCR may make an amplifier oscillate or trip its protection.

## 6. Input preparation and repeatable geometry

- Connect the pickup to a **high-impedance** instrument input (Hi-Z, ≥ 1 MΩ). Use the same short cable for every pickup: input and cable capacitance shift the measured resonance.
- Keep the fixture geometry identical: the same distance and position between exciter and pole pieces (a spacer or jig helps), the same orientation and the same output level. Every result is comparative to that setup.
- Keep the room quiet electrically: dim fluorescent lights, keep phones and switch-mode supplies away, and calibrate with the pickup in place.

## 7. Measurements

Tabs: **Summary · Bode response · Phase · Spectrum · Settings**. Each measurement tab has its own description, setup, run button, Stop, progress bar, graphs and result cards. Every result and every graph heading has a `?` button. It opens a large explanation tooltip on hover, keyboard focus or tap, covering what is calculated, what it indicates and the main caveat. An outside press or Escape closes it.

**Measure All** runs Bode → Phase → Spectrum in sequence, opens each tab as its test starts, and stamps today's Wind Date. It shows one *All three measurements complete.* message at the end and then returns to Summary. Stop cancels the remaining stages. A failure stops the sequence and names the stage. Individual run buttons never change Wind Date.

All output-producing tests need a connected, calibrated input. The output bus is muted whenever no tone or measurement is running. After every measurement, whether it completes, fails or is cancelled, the app also shuts the output down hard. It cancels all gain automation, mutes the bus, stops and disconnects every generator, and rebuilds the output route, including re-applying the output device the way a manual device change does. A capture that stops receiving audio fails with an error instead of hanging. If the browser pauses audio, the status pill asks for one click to resume it. No result is ever invented when the signal is missing. A measurement that fails or is cancelled leaves the previous results untouched.

### Bode response (magnitude only)

- One phase-continuous logarithmic chirp from 500 Hz to 8 kHz (7 s plus brief endpoint holds, with 55 ms fades) is played at the unchanged Output level. The full return is captured once.
- The return is located from the audio API latency estimate plus a bounded cross-correlation onset search. Learned hum is removed conservatively, without touching the frequencies the chirp is passing through at that moment. The signal is band-limited.
- **Sweep points** (20/30/40/50/60, default 60) sets analysis density, not separate tones. Points follow an exponential schedule that is denser at high frequencies. Each point is analysed from an overlapping local window of about ±1/20 octave, using the median RMS of five sub-blocks. The learned noise power is subtracted in the power domain. At least 60% of the points must clear the noise floor; otherwise the run fails with routing/gain guidance.
- Rejected gaps are interpolated only to keep the curve continuous. They are excluded from the direct-point count and from peak selection. A local median outlier guard and light 3-point smoothing stop single spikes from being taken as the resonance.
- Nine extra log-spaced **refinement** points around the strongest candidate are analysed from the same capture. The curve is published only after the whole run succeeds.
- The **fit** is a quadratic in log-frequency through the strongest local 7 (or 5) direct points. It reports the fitted resonance and a ± uncertainty that combines half the closest bin spacing with leave-one-out variation. When no concave in-range fit exists, the strongest-bin fallback is stored explicitly.
- **Display:** the curve is normalised so its lowest robust value is exactly 0 dB, with ticks every 6 dB. **Curve smoothing** (0–100%, default 45%) is a display-only Gaussian in log-frequency with a strongly progressive mapping. It never changes the fit, the cards or the raw CSV values.
- Cards: Fitted resonance, Fit uncertainty, Peak above minimum, Direct / total points.

### Phase

Five shaped low-level pulses are played. Each return is searched in a window wide enough for common interface latency. The strongest excursion is located and normalised into a 30 ms view, and its sign is voted. The result is **POSITIVE**, **NEGATIVE**, or **INDETERMINATE** when the response is below about −80 dBFS or fewer than four votes agree. Cards: Relative phase, Vote agreement, Pulse response level.

### Spectrum (white noise)

- Presets are Pickup focus 500–8,000 Hz, Guitar/bass 40–8,000 Hz, Full audio 20–20,000 Hz, and Custom. Editing Low/High switches to Custom, and High is clamped below Nyquist.
- **Duration** is 2.5, 5 or 10 s. Local white noise passes through a high-pass and a low-pass biquad (Q ≈ 0.707) and is played at the test level on the selected output channel.
- Between 4 and 16 Hann-windowed 8192-point FFT power frames are averaged, depending on duration. The plot is downsampled on a log grid to at most 1200 points and normalised to the strongest point (0 dB).
- **Spectral waterfall**: 12–28 evenly spaced 4096-point frames, each compacted to 96 log cells and normalised to the strongest cell. For contrast, a high-contrast colour scale runs from the quietest 5% of cells (never below −90 dB) to 0 dB, and its lower limit is printed on the colour bar. The measured spectrum and the waterfall sit side by side on wide screens. Frequency runs left to right and time top to bottom. The waterfall is saved with the project.

The 16 metrics:

1. Peak frequency
2. Fundamental (harmonic-sum estimate)
3. RMS level (DC removed, dBFS)
4. Sample peak
5. Spectral centroid
6. 85% roll-off
7. Spectral bandwidth
8. Spectral flatness
9. Spectral slope (dB/octave)
10. THD estimate (harmonics 2–8)
11. Even / odd
12. Peak asymmetry
13. Transient index (max/median 20 ms RMS)
14. Low band (< 250 Hz)
15. Mid band (250 Hz–2 kHz)
16. High band (> 2 kHz)

**Caveat:** with broadband excitation, *Fundamental*, *THD* and *Even / odd* are **comparative screening indicators**, not calibrated distortion measurements. The exciter, its amplifier and the input loading shape every spectrum.

## 8. Projects, comparison and exports

**Project panel:** Project Name (default `Demo`) and Project Notes, then three subsections:

- **Customer**: Name, Address, Phone, eMail, Notes, and a Wind Date in `DD.MM.YYYY` that formats itself as you type.
- **Pickup**, in five groups:
  - Info: Pickup ID, Guitar Type, and the Guitar/Bass, Single Coil/Humbucker and Clockwise/Counterclockwise checkboxes
  - Wire: Wire Type, Gauge, # Winds
  - Hardware: Pole Insulator, Protection, Magnet Type
  - Wires: Leads, Start Wire (Ground), End Wire (Hot)
  - Properties: Polarity, Phase, DCR, Inductance, Capacitance
- **Tonewinder** (only with `?footprint=true`).

Every value is tracked for unsaved changes and saved automatically.

**Project comparison** has six persistent slots with stable colours: blue, lime, orange, white, purple and teal. Red is reserved for the selected project's trace, which is drawn thicker.

- Click a card (or use its radio button with the keyboard) to select it. Selecting a stored slot loads it into the workspace.
- **Show** toggles that slot's trace on the shared 500 Hz–8 kHz Bode comparison graph. Each slot's fitted resonance appears next to the graph, and each readout also selects its slot.
- **Store** copies the complete current project into the active slot.
- **Create PDF** freezes the active slot as an immutable snapshot and blocks edits until the file is ready.
- **Load from file** imports a project into the active slot and loads it.
- **Save to file** downloads the active slot.
- **Clear slot** and **Clear All** both ask for confirmation, then start a clean `Demo` project with today's Wind Date and default Pickup and Tonewinder values.

**Project file:** pretty-printed version-2 JSON named `<safe-name>.pickup-lab`. Version-1 projects and legacy `.custom-winds` and `.pickup-health` files load as well. Missing Spectrum data becomes empty, missing customer and pickup records get defaults, legacy impulse results and settings are dropped, and ISO dates are converted to `DD.MM.YYYY`.

**Export CSV** (Summary) contains:

- project, customer, pickup, tonewinder and routing/settings records
- the Summary overview and every displayed measurement
- full Bode rows: noise-subtracted, raw, output, robust-filtered, raw relative, displayed and smoothed values, plus SNR, learned noise, stability and the direct/interpolated/refinement flags
- the fit metadata
- phase votes and all five pulse waveforms
- raw spectrum metrics, spectrum points and every waterfall cell

**Export PNG** is a 2× image in the current theme that mirrors the compact Summary only.

**Create PDF** is a real multi-page A4 document built locally from canvas-rendered pages. It uses a clean print palette, with the tool name at upper left, the logo at upper right and the lab name alone in the footer. Pages:

1. Project Information (two pages)
2. Overview
3. Bode response with Relative phase (data only)
4. Spectrum Data (measured spectrum, waterfall and the 16 metrics)
5. With `?footprint=true`, a final Tonewinder page

The file is named `<safe-name>-complete-record.pdf`.

## 9. Tone Footprint (`?footprint=true`)

This mode is hidden by default. When enabled, Summary, PNG and the PDF Overview add three things:

- A **Character** gauge with five bands — Velvet, Warm, Balanced, Vivid and Bright — on a red-to-blue gradient.
- A four-axis **Tone Footprint** spider diagram:
  - Brightness, Clarity and Attack in blue hues
  - Body in orange
- **Tonal Characteristics** text.

Brightness, Clarity, Attack and Body come from a pickup model. Fitted resonance has the highest weight, then inductance, DCR and winding count, with a small instrument and construction adjustment. Every score is a **comparative normalized descriptor, not a calibrated physical unit**. The Tonewinder subsection and its PDF page also appear only in this mode, but Tonewinder values are always saved and exported to CSV.

## 10. Themes and accessibility

- Themes: **Light**, **Dark orange**, **Dark green**, **Dark blue** and **Dark purple** (first-run default). The theme button cycles through them in that order. The choice is remembered and redraws every graph.
- Semantic headings, labels and fieldsets; native controls; `role="tab"` tabs with arrow-key navigation; live status regions; visible focus rings; and a single global `role="tooltip"`.
- Buttons are at least 38 px tall and single-line inputs and selects 40 px. Graphs keep a fixed height at every width, and the canvas resolution is capped at a device pixel ratio of 2. Hover or drag on any graph to inspect values.
- `prefers-reduced-motion` is respected. The layout stacks below about 1100 px, becomes a single column below about 760 px, and has no horizontal scrolling down to 300 px.

## 11. Quality checklist

1. Serve from localhost and allow audio. Check that the status pill shows the learned input noise.
2. Play the 440 Hz tone and confirm the exciter and the INPUT meter respond on the chosen channel.
3. Set the Output level so the Bode return peaks well below −12 dBFS while staying clearly above the input floor.
4. Run Measure All. Check *Direct / total points* (close to the total), and the phase vote (5/5).
5. Store the project in a slot, then measure the next pickup with an identical geometry.

## 12. Limitations

- Results are **comparative**. Input impedance, cable capacitance, exciter construction, amplifier response and geometry all shape them.
- Bode is magnitude only. Phase is a relative sign, not a phase response.
- Hum removal is conservative and only covers stationary 50/60 Hz harmonics learned during calibration.
- Browser latency estimates vary. The bounded onset search compensates within about ±0.3 s.
- Output-device selection depends on browser support (current Chrome or Edge).

## 13. Troubleshooting

| Symptom | Fix |
|---|---|
| "Only N of M points cleared the input noise floor" | Check the output device and channel (is the exciter actually driven?), raise the Output level, move the exciter closer, or check the input channel. |
| Permission denied | Allow microphone access for the page in the browser's site settings, then press the status pill and **Allow audio access**. |
| Output device change reverts to the system default | Use localhost/HTTPS in a current Chrome or Edge. Some browsers need the device-selection prompt to be accepted. |
| Calibration reports a loud baseline | Silence the room, check grounding and keep the exciter disconnected from noisy sources. Trim is reduced automatically. |
| Phase INDETERMINATE | Raise the Output level, improve coupling, reduce hum. |
| Local state lost | Private windows and cleared site data reset `localStorage`. Save projects to file. |
| Rebuild icons | `python3 scripts/generate-icons.py` (requires Pillow). |
