# ИH Custom Winds

ИH Custom Winds is a self-contained browser instrument for comparative guitar and bass pickup testing. It uses a real audio-interface input and a repeatable magnetic driver or tap fixture to measure:

- Manual-tap and three-pulse automatic impulse response with adaptive noise rejection, hum cancellation, and robust aligned stacking
- Captured impulse waveform, logarithmic decay envelope, and resonant-ring FFT
- Ring frequency, estimated T60, damping ratio ζ, Q, and rise time
- Band-selectable white-noise response over 2.5, 5, or 10 seconds
- 16 time- and frequency-domain noise-response indicators
- Magnetic saturation, 500 Hz–8 kHz Bode magnitude, and five-pulse relative phase
- A fixed 440 Hz routing/reference tone
- JSON project save/load, CSV data export, and theme-aware PNG summary export

The application logic is entirely contained in [index.html](./index.html), with the local [logo.png](./logo.png) displayed in the upper-right header and local favicon/iPhone artwork used for browser tabs and Add to Home Screen. Audio stays in the browser tab. There are no runtime dependencies, remote assets, uploads, network requests, telemetry services, or automatic recordings.

## Files

```text
index.html             Complete application, styling, audio engine, and plots
logo.png               Header logo
favicon.svg            Scalable browser-tab icon
favicon-32x32.png       Raster browser-tab icon
favicon.ico             Multi-size legacy browser favicon
apple-touch-icon.png    180×180 iPhone Add to Home Screen icon
scripts/generate-icons.py  Reproducible raster-icon generator
README.md              User guide, safety guidance, and driver construction
PROMPT.md              Full reconstruction specification
```

## Start locally

Audio permission requires a secure browser context. `localhost` qualifies:

```bash
cd /path/to/MY_CUSTOM_WINDS
python3 -m http.server 4173
```

Open `http://127.0.0.1:4173` in a current browser. The opening splash follows the active theme and describes audio access but does not request permission automatically. Press **Allow audio access** to connect. **Explore first** closes the splash without requesting access; reload the page when you are ready to connect an input.

## Signal path

```text
440 Hz / automated test output (Bode, noise, saturation, phase, Capture Auto)
  → operating-system default audio output
  → suitable headphone or power amplifier
  → repeatable magnetic driver coil
  → magnetic coupling across a fixed gap
  → pickup under test
  → interface Hi-Z input and selected channel
  → browser analysis
```

**Manual Capture** is input-only: it waits for a real physical or magnetic impulse and never starts the output. **Capture Auto** emits exactly three short, zero-DC bipolar impulses at the selected test-output level, captures the pickup response to each one, rejects unusable responses, and stacks the accepted captures. White noise, saturation, Bode, phase, Capture Auto, and the 440 Hz tone use the fixed operating-system output. There is intentionally no output-device or output-channel selector.

## Safety

Incorrect loading or excessive output can damage an interface, amplifier, driver coil, active pickup, speakers, or hearing.

1. Mute monitors, headphones, instrument amplifiers, and DAW monitoring before enabling a test output.
2. Never assume an interface line output can drive a low-resistance coil. Use an appropriate enclosed, current-limited headphone or power amplifier.
3. Measure the finished coil's DC resistance. Follow the amplifier manufacturer's minimum-load requirement; DC resistance is not the same as AC impedance.
4. Begin at `−48 dBFS` and with the external amplifier low. Increase cautiously.
5. Stop if the coil or amplifier warms, clips, smells unusual, or behaves erratically.
6. Input is never routed to output by this application, but an interface mixer, operating-system mixer, or DAW can still create a feedback path.
7. Do not work on exposed mains wiring.
8. Use clean nonmagnetic spacers so the fixture cannot scratch the instrument or strike the pickup.
9. For active pickups, use a healthy battery and keep onboard control positions fixed.

## Repeatable magnetic driver

Repeatability matters more than field strength. A useful starting design is:

- Nonmagnetic plastic, fibreboard, acrylic, or 3D-printed former
- Winding window roughly 35–50 mm long and 8–15 mm wide
- Enamelled copper wire around 0.25–0.35 mm diameter (AWG 30–27)
- Approximately 220–350 turns
- Common finished DC resistance around 6–12 Ω, verified with a meter
- Twisted, strain-relieved flexible leads
- Optional electrostatic foil shield with a full-width gap so it cannot form a shorted turn

These are starting values, not a guaranteed load. Wire diameter, winding length, inductance, frequency, and amplifier design all affect the real load.

### Construction

1. Build a rigid former with two flanges and no steel, magnets, or ferrite.
2. Smooth sharp edges and provide holes or clamps for strain relief.
3. Wind 220–350 turns in a consistent direction and count them.
4. Secure layers with thin insulating tape or winding varnish.
5. Strip enamel only at the two joints, solder flexible leads, and insulate them.
6. Measure DC resistance and check that neither lead connects to the former or shield.
7. If shielding, leave a deliberate full-width gap in the foil.
8. Permanently mark the driver face, winding direction, and lead phase.
9. Mount it in a nonmagnetic fixture with hard stops for height, lateral position, and angle.

Record the driver-to-pickup gap, pickup position, instrument-control positions, input gain, output-amplifier setting, sample rate, and fixture orientation in project notes.

## Preparing a measurement

1. Fix the instrument and driver so neither can move.
2. Mechanically mute the strings for magnetic-driver measurements.
3. Select only the pickup under test.
4. Put passive volume/tone or active EQ controls at documented positions.
5. Connect to a high-impedance interface input and disable input effects, auto gain, echo cancellation, noise suppression, and monitoring.
6. Grant input permission and select the device and channel.
7. Adjust analog input gain so the strongest event stays below clipping.
8. Set **Test output level** low and verify the default operating-system output.
9. Use the 440 Hz button briefly to confirm routing. Stop it before changing cables or fixtures.

Digital input trim changes analysis level but cannot repair analog clipping.

## Analysis workflow and results dashboard

The first five analysis tabs—**Bode response**, **Noise spectrum**, **Saturation**, **Phase**, and **Impulse / tap**—contain their setup, start button, progress, graphs, and measurements. Bode response is the initial tab. Each primary measurement-action row has clear vertical breathing room above and below. The **Summary** tab contains a synchronized second copy of every graph and measurement in the same order.

The glowing **Measure All** button beside **Clear measurements** runs the five tests sequentially in tab order: Bode, Noise, Saturation, Phase, then Impulse / tap. The app opens each tab as its measurement starts, waits for every test to finish, and returns to Bode when the sequence completes, fails, or is stopped. The final stage uses Capture Auto and emits exactly three impulses, so the batch does not pause for physical taps. One centered toaster confirms when all five measurements finish successfully; **Stop output** cancels the active test and the remaining sequence.

Every result value has a `?` explanation button describing its role, interpretation, and main caveat. Every graph heading has the same explanation control. The buttons work by hover, keyboard focus, and touch; tap elsewhere or press Escape to dismiss. Explanation boxes use the same large, orange-accented blurred-glass treatment as centered notification messages. Every graph keeps labelled x/y tick values visible, and measured graphs also show exact cursor-position values on hover or touch-drag.

## 440 Hz test tone

**Play 440 Hz test tone** produces a continuous sine wave through the operating system's default output at the selected test-output level. It requires an input connection. Press the same button or **Stop output** to ramp it down.

The button is intended only for routing, gain, and phase-chain checks. It replaces the former free-form excitation generator.

## Impulse-response / tap test

Choose 3, 5, or 7 impulses (3 by default) and press **Manual Capture**. For each tap, the app:

1. Learns about 700 ms of quiet input using robust RMS, variation, and upper-percentile peak statistics.
2. High-pass conditions only the detector path so steady mains hum and slow handling movement are less likely to trigger it.
3. Arms only after five stable frames, then displays **TAP NOW**.
4. Requires a fresh, steep transient that clears adaptive RMS, peak, crest-factor, novelty, peak-rise, and roughness thresholds.
5. Captures approximately 1.35 seconds aligned to the trigger for analysis, while storing and displaying only the aligned 20 ms onset waveform.
6. Rejects and retries weak, noise-like, non-decaying, or clipped captures, up to three attempts per tap.
7. Scores valid responses by raw and transient signal-to-noise ratio plus decay quality.

Wait for **TAP NOW**, make one firm tap, then allow the ring to decay before the next tap. After the series, the app uses the highest-scoring capture as the reference and combines all sufficiently correlated taps. Use the same impact device, direction, force, contact point, input gain, and pickup loading for comparable results.

### Automatic capture

Press **Capture Auto** to automate the impulse stage. The app emits exactly three separate 4.5 ms zero-DC bipolar impulses through the operating system's default output at the selected test-output level. Before each impulse it learns the current noise floor; after the pulse it captures the decay, locates the returned transient within a bounded latency window, and applies the same SNR, decay, clipping, hum-cancellation, alignment, and robust-stacking checks used by Manual Capture. Weak responses are rejected without emitting replacement pulses, so a run always contains exactly three excitation events. If all three are rejected, the app reports routing/gain guidance instead of creating a result.

**Measure All** uses Capture Auto for its final stage, allowing the full sequence to finish without asking for manual taps. Keep the amplifier, driver coil, pickup, and interface connected exactly as they are for the other output-driven measurements.

### Noise cancellation

Each accepted capture is cleaned using the quiet reference measured immediately before its tap. The app detects coherent 50 or 60 Hz mains hum and harmonics through 1.2 kHz, then removes only components that remain stable in the late capture. This avoids a hard gate that would artificially shorten the decay.

The cleaned taps are peak-aligned and compared over their early ring. Only positively correlated captures are retained, scaled within conservative limits, and combined with a sample-wise median. This suppresses uncorrelated background noise and inconsistent handling sounds while anchoring alignment and phase to the highest-scoring tap. The detector status reports how many taps were stacked and the measured late-tail noise reduction. More consistent taps produce more effective cancellation.

### Impulse plots

- **Captured waveform** is the aligned, noise-reduced tap stack, normalized and limited to a 20 ms onset window.
- **Decay envelope** uses 5 ms RMS blocks across the captured decay on a logarithmic dB scale and overlays the fitted T60 line.
- **FFT of resonant ring** uses the early aligned response and identifies its strongest 60 Hz–10 kHz component.

These plots appear in the **Impulse / tap** tab and as synchronized copies in Summary. Every plot has a fixed height and a cursor tooltip with the value nearest the pointer.

### Impulse values

- **Ring frequency** — strongest early-decay spectral component.
- **Decay time / T60 estimate** — time for the fitted amplitude envelope to fall 60 dB. It is extrapolated when the captured signal reaches the noise floor earlier.
- **Damping ratio ζ** — estimated as `1 / (2Q)`. Smaller values mean a more lightly damped ring.
- **Q from ring** — derived from frequency and decay: `Q = π × f × T60 / 6.9078`.
- **Rise time** — interval from 10% to 90% of the first peak.

T60, Q, and ζ are model-based estimates. Multiple modes, noisy envelopes, driver motion, active electronics, mechanical vibration, and short capture windows can make the fit unresolved or misleading.

## White-noise spectrum

The noise test plays locally generated white noise through the system-default output. Two second-order Butterworth-style biquad filters limit the excitation to the selected span:

- Pickup focus: 500–8,000 Hz
- Guitar / bass: 40–8,000 Hz
- Full audio: 20–20,000 Hz, limited by sample rate
- Custom low and high frequencies

Choose 2.5, 5, or 10 seconds. Longer runs support more stable averaging but heat the driver more and require a quiet, fixed setup. The analyzer averages multiple 8192-point Hann-window FFT frames and plots the response relative to its strongest selected-band bin.

### Spectrum metrics and tooltips

The spectrum graph and metrics appear in the **Noise spectrum** tab and as synchronized copies in Summary. Every metric card has a `?` button. Hover, focus, or tap it to see an explanation.

| Measurement | Meaning |
| --- | --- |
| Peak frequency | Strongest averaged spectral component in the selected span. |
| Fundamental | Harmonic-score estimate of the lowest periodic component; may be uncertain for broadband noise. |
| RMS level | Average captured signal energy in dBFS. |
| Sample peak | Largest absolute digital sample; values near 0 dBFS indicate clipping risk. |
| Spectral centroid | Power-weighted spectral center, often perceived as brightness. |
| 85% roll-off | Frequency below which 85% of selected-band power lies. |
| Spectral bandwidth | Power-weighted spread around the centroid. |
| Spectral flatness | Geometric/arithmetic mean power ratio; high is flat/noise-like. |
| Spectral slope | Fitted level trend in dB per octave. |
| THD estimate | Harmonics 2–8 relative to estimated fundamental; screening-only under noise excitation. |
| Even / odd | Even-harmonic to odd-harmonic energy ratio in dB. |
| Peak asymmetry | Positive/negative waveform peak ratio in dB. |
| Transient index | Strongest 20 ms RMS block divided by median block RMS. |
| Low band | Integrated selected-span spectral energy below 250 Hz. |
| Mid band | Integrated selected-span spectral energy from 250 Hz to 2 kHz. |
| High band | Integrated selected-span spectral energy above 2 kHz. |

Fundamental, THD, and even/odd remain comparative screening indicators under broadband excitation. For more defensible distortion results, use the dedicated stepped-tone saturation test.

## Existing guided measurements

### Magnetic saturation

Eight 1 kHz steps measure pickup RMS output, fundamental, combined even harmonics, combined odd harmonics, half-cycle asymmetry, and transfer compression. Even harmonics growing faster than odd while the transfer curve bends asymmetrically can suggest magnetic saturation, but driver-amplifier or interface distortion can mimic it.

### Bode magnitude

Thirty logarithmically spaced tones cover 500 Hz–8 kHz. Results normalize to the strongest point and report peak resonance, peak level, and endpoint tilt. The peak-resonance point is marked directly on the Bode graph. It is magnitude-only and includes the entire driver/interface chain.

### Relative phase

Five low-level shaped pulses vote on response sign. The result is positive, negative, or indeterminate. It is relative to driver face, winding, leads, input wiring, and interface phase—not absolute magnetic north/south.

## Projects and exports

- The **Customer** record stores name, address, phone, eMail, notes, and wind date in Swiss `DD.MM.YYYY` format.
- The **Pickup** record starts with Pickup ID, which defaults to `NH 7k42 #1`, followed by guitar/bass, single-coil/humbucker, clockwise/counterclockwise selections plus wire type, gauge, wind count, polarity, phase, pole insulator, protection, leads, start wire (hot), and end wire (ground). New projects start with the requested NH winding defaults: Plain Enamel, AWG42, 7000 winds, South polarity, Negative phase, Kapton Tape, Tissue, Waxed Pushback, Yellow hot/start, and Black ground/end.
- **Save project** downloads version-2 JSON data using the single `.custom-winds` filename extension. It contains customer and pickup records, settings, the impulse capture mode and automatic-excitation metadata where applicable, full impulse results, per-capture and noise-cancellation metadata, envelope, impulse FFT, all noise metrics and spectrum points, saturation, Bode, phase, notes, and timestamps.
- **Load project** accepts version 2, migrates compatible version-1 files, and remains compatible with legacy `.pickup-health` files.
- **Export CSV** contains the customer and pickup records, four Summary overview cards, every displayed measurement, raw impulse waveform/envelope/fit/FFT data, capture-mode and automatic-excitation metadata, impulse noise-cancellation metadata, all noise metrics and spectrum points, saturation harmonic/transfer data, Bode points, phase votes, and every phase waveform sample.
- **Export PDF**, located immediately to the right of **Load project**, creates a polished multi-page A4 record locally: branded header and logo, project/customer information, pickup properties and test settings, three measurement pages, and a multi-page annex glossary copied directly from every measurement tooltip. The first measurement page places Bode response above Relative phase, the second places Saturation above Noise spectrum, and the third contains Impulse / tap. Noise spectrum and Relative phase remain data-only; the Bode, Saturation, and Impulse graphs appear before their data, and Bode peak resonance is marked. Pickup selections render as checked or empty boxes in three vertical pairs: Guitar above Bass, Single Coil above Humbucker, and Clockwise above Counterclockwise. Project ID is omitted; Created and Updated use date-only Swiss formatting. The footer contains only the configured lab name, with no separator, page number, or timestamp. Its PDF-only logo is embedded to keep canvas export secure when the app is opened directly from disk.
- **Export PNG** uses the current theme and renders the customer and pickup records plus the complete Summary dashboard: all overview information, notes, 33 detailed measurements, and all eight graphs. The three export buttons stay together in a spaced toolbar at the top of Summary.

The **Settings** analysis tab lets you change the tool name (default **ИH Custom Winds**) and lab name (default **Nicks Pickup Lab**). Press **Apply** to update the header, hero, browser title, and export branding. These names are stored with saved projects and restored when a project is loaded.

No project data or theme is persisted automatically. Reloading always starts in **Dark green**.

## Themes, responsive behavior, and accessibility

The header theme button cycles through **Light**, **Dark orange**, **Dark green**, and **Dark blue**, displaying the active theme name. Dark green is the default and uses acid-green `#d5fe42` accents; Dark blue uses vibrant blue accents, and Light uses neutral surfaces with dark blue. Theme selection is session-only and redraws every source and Summary canvas; PNG and CSV exports identify and use the selected palette.

Controls are native, labelled, and keyboard accessible. Every single-line text/number field and dropdown uses the same 40 px height; multiline notes remain resizable. Measurement and graph tooltips work with pointer hover, keyboard focus, and touch. Plots remain fixed in height while data accumulates, resize horizontally, cap backing-store scale at `2×` device pixel ratio, and stack on mobile. Summary sections and their metric grids collapse cleanly to one column on narrow phones.

## Quality checklist

- Keep driver geometry and all analog gains fixed.
- Warm up active electronics and the driver amplifier.
- Use the same sample rate for a comparison series.
- Record battery condition and instrument-control positions.
- Repeat a reference pickup periodically to quantify fixture drift.
- Use the same tap device, direction, force, contact point, and fixture support for every impulse series.
- Reject clipped captures and investigate high transient index during noise tests.
- Allow the driver to cool between long or high-level noise runs.
- Compare complete curves and confidence indicators, not one headline value.
- Save the project immediately after a clean series.

## Limitations

- Browser and interface timing are not laboratory-instrument synchronized.
- The response is not de-embedded from DAC, amplifier, driver coil, fixture, pickup loading, cable, or ADC.
- Bode and noise results are magnitude-only.
- Impulse T60 assumes a primarily exponential decay; multiple resonances violate that simple model.
- White-noise harmonic metrics cannot separate excitation energy from distortion as cleanly as a single-tone analyzer.
- The app cannot sense driver-coil temperature or external amplifier clipping.
- Comparative results can be excellent; certification-grade absolute results require calibrated hardware and a controlled fixture.

## Troubleshooting

**No input prompt** — Reload the page, press **Allow audio access** on the splash, use localhost/HTTPS, and check site permissions.

**Tap never triggers** — Wait for **TAP NOW**, then make one firm, clean tap. If the input meter barely moves, raise the interface's analog gain slightly or improve mechanical/magnetic coupling without clipping.

**Tap triggers before contact** — Reduce background noise and handling movement, keep the fixture still during calibration, and wait for the detector to arm before approaching it.

**T60 or Q is unresolved** — Increase signal-to-noise ratio, stabilize the driver fixture, and keep strings or loose hardware from vibrating during the decay.

**White-noise response is missing** — Confirm the operating-system default output, driver amplifier, coil continuity, and selected input. Use the 440 Hz tone at low level first.

**Fundamental seems wrong** — Broadband excitation can make the harmonic-score estimate ambiguous. Treat it as a comparative hint and use the dedicated saturation test for more defensible harmonic measurements.

**Output comes from the wrong interface** — Change the operating system's default output. The app intentionally has no output selector.
