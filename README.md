# ИH Custom Winds

ИH Custom Winds is a self-contained browser instrument for comparative guitar and bass pickup testing. It uses a real audio-interface input and a repeatable magnetic driver fixture to measure:

- Band-selectable white-noise response over 2.5, 5, or 10 seconds
- 16 time- and frequency-domain noise-response indicators
- Magnetic saturation, 500 Hz–8 kHz Bode magnitude, and five-pulse relative phase
- A fixed 440 Hz routing/reference tone
- Automatic local-state persistence, JSON project save/load, CSV data export, and theme-aware PNG summary export

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
440 Hz / automated output (Bode, spectrum, saturation, phase)
  → selected audio output device and hardware channel
  → suitable headphone or power amplifier
  → repeatable magnetic driver coil
  → magnetic coupling across a fixed gap
  → pickup under test
  → interface Hi-Z input and selected channel
  → browser analysis
```

Spectrum, saturation, Bode, phase, and the 440 Hz tone use the selected output device and channel. The Output device dropdown lists every `audiooutput` exposed by the browser, with **System default output** as the fallback. Selecting a hardware device prefers Web Audio output-sink routing and falls back to a hidden HTML audio sink fed by the Web Audio graph; the browser may request permission before exposing or activating a non-default device. If neither standards-based sink API is available, non-default selection requires opening the app from localhost or HTTPS in a current Chrome or Edge browser. The Output channel selector routes the mono test signal discretely to the chosen destination channel.

Whenever the input device or input channel changes, the app keeps the output silent, resets **Input trim** to 0 dB and **Output level** to −30 dBFS, discards the previous route correction, and records exactly one quiet window lasting no more than three seconds from the same `AnalyserNode` that drives the visible INPUT meter. A blocking overlay says **Calibrating, please wait.** and asks the operator to keep the input quiet for the complete capture. The automatic decision uses that window's raw meter RMS, including any visible DC component. If it is louder than −70 dBFS, the app lowers **Input trim** once in whole-dB steps and raises **Output level** by the same amount within its safe range. There are no verification passes or further calibration captures. Route selection and measurement buttons are locked during those three seconds, and device/channel selection is locked during every measurement, so calibration cannot run while a measurement is active. Measurements reuse the learned route profile without moving either level control. A green marker on the INPUT meter identifies the −70 dBFS target; the red marker remains at −12 dBFS.

The final session-only profile also detects persistent 50/60 Hz harmonics. It is used for conservative stationary-hum removal throughout the measurements and for local-window noise-power subtraction in the continuous Bode sweep. The active sweep frequency is protected from hum removal. Relearning avoids reusing a noise profile or calibration from a different interface route.

## Safety

Incorrect loading or excessive output can damage an interface, amplifier, driver coil, active pickup, speakers, or hearing.

1. Mute monitors, headphones, instrument amplifiers, and DAW monitoring before enabling an output signal.
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
8. Select the required output device and hardware channel, then set **Output level** low.
9. Use the 440 Hz button briefly to confirm routing. Stop it before changing cables or fixtures.

Digital input trim changes analysis level but cannot repair analog clipping.

## Analysis workflow and results dashboard

The desktop workspace places **01 Audio routing** beside the wider **02 Analyze pickup** panel. Inside Audio routing, the interface input controls and meter sit in a dedicated green-accented **Input** group. **Input device** and **Input channel** share one row; **Input trim** and the accent-colored manual **Recalibrate** button share the next. Recalibrate repeats the same quiet-input route calibration used after an input-device or input-channel change. In the blue-accented **Output** group, **Output device** and **Output channel** share one row above the generator level, meter, and buttons. The full-width **03 Project comparison** panel places its six large slot cards and file actions on the left, with six side-by-side **Fitted Resonance** readouts and the shared Bode graph on the right. The full-width **04 Project** panel follows it, with Customer on the left and Pickup on the right. When `?footprint=true` is active, a separate full-width Tonewinder subsection appears below them. These panels stack vertically on narrow screens.

The **Summary** tab is first and initially active. By default it contains Resonance, Relative phase, DCR, Inductance, Compression, and Measurement record. Add `?footprint=true` to the page URL—for example, `http://127.0.0.1:8766/?footprint=true`—to also show the horizontal-bar **Tone Footprint**, **Tonal Characteristics**, and the Project panel's **Tonewinder** subsection. Each Tone Footprint factor has its own accessible explanation tooltip, and every bar transitions from the current theme accent to reddish orange. The detailed graphs and metrics remain in the four measurement tabs—**Bode response**, **Phase**, **Spectrum**, and **Saturation**. Brightness, Clarity, Attack, and Body use a pickup-specific electrical model: fitted resonance receives the strongest weight when available, while inductance, DCR, wind count, and pickup construction supplement it or provide an estimate before measurement. Compression remains the measured stepped-drive result. These normalized scores are comparative descriptors rather than calibrated physical units. The feature stays off when the parameter is absent or has any value other than `true`.

The glowing **Measure All** button beside **Clear measurements** runs the four tests sequentially in tab order: Bode, Phase, Spectrum, then Saturation. The app opens each tab as its measurement starts, waits for every test to finish, and returns to Summary when the sequence completes, fails, or is stopped. One centered toaster confirms when all four measurements finish successfully; **Stop output** cancels the active test and the remaining sequence.

Every result value has a `?` explanation button describing its role, interpretation, and main caveat. Every graph heading has the same explanation control. The buttons work by hover, keyboard focus, and touch; tap elsewhere or press Escape to dismiss. Explanation boxes use the same large, orange-accented blurred-glass treatment as centered notification messages. Every graph keeps labelled x/y tick values visible, and measured graphs also show exact cursor-position values on hover or touch-drag.

## 440 Hz test tone

**Play 440 Hz test tone** produces a continuous sine wave through the selected output device and channel at the selected output level. It requires an input connection. Press the same button or **Stop output** to ramp it down.

The button is intended only for routing, gain, and phase-chain checks. It replaces the former free-form excitation generator.

## Spectrum

The noise test plays locally generated white noise through the selected output device and channel. Two second-order Butterworth-style biquad filters limit the excitation to the selected span:

- Pickup focus: 500–8,000 Hz
- Guitar / bass: 40–8,000 Hz
- Full audio: 20–20,000 Hz, limited by sample rate
- Custom low and high frequencies

Choose 2.5, 5, or 10 seconds. Longer runs support more stable averaging but heat the driver more and require a quiet, fixed setup. The analyzer averages multiple 8192-point Hann-window FFT frames and plots the response relative to its strongest selected-band bin.

### Spectrum metrics and tooltips

The **Spectrum** tab contains two measured-frequency graphs: an averaged logarithmic spectrum and a time-resolved spectral waterfall. In the waterfall, frequency runs left to right, capture time runs top to bottom, and color represents relative level from −90 dB to 0 dB. Both graphs and the metric cards have synchronized copies in Summary. Every metric card and graph has a `?` button; hover, focus, or tap it to see an explanation.

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

The **Sweep points** dropdown offers 20, 30, 40, 50, or 60 analysis points, with 60 as the default. The app emits one phase-continuous logarithmic chirp from 500 Hz to 8 kHz at the selected test-output level. Short endpoint holds and 55 ms fade-in/fade-out ramps avoid the abrupt transitions and output peaks produced by separate stepped tones.

The selected points are sampled from overlapping local windows of the same captured chirp, using windowed RMS estimates and learned-noise power subtraction. Noise-limited points are excluded from the direct-point count and interpolated only for graph continuity. A local outlier filter and light smoothing prevent isolated noisy bins from becoming the resonance candidate. After the normal sweep analysis, the app adds nine closely spaced analysis frequencies between the candidate's neighboring bins, using the same continuous capture.

The graph remains hidden while the continuous sweep runs, while its normal points are calculated, and during peak refinement. During excitation, the top-right status displays the instantaneous sweep frequency and live input value; during analysis and refinement, it displays the point frequency and measured value. Once complete, the robust response is normalized to a minimum of 0 and presented on the established 1:6 display scale. Its measured robust trace is only slightly dimmed and is drawn above the brighter Gaussian-smoothed curve so the original points remain visible. The **Curve smoothing** slider adjusts the overlay from 0% to 100% in logarithmic-frequency space and defaults to 45%. Its progressive response preserves considerably more local variation through the lower and middle range, reserving strong smoothing for the upper end. It is a display control only and never changes the resonance fit, uncertainty, saved measurements, or CSV raw values. The selected smoothing level is saved with the project and used by the on-screen, Summary, PNG, and PDF Bode graphs.

A quadratic curve in log-frequency is fitted through the strongest local seven direct points (five when only five are available). The app reports and exports the fitted resonance, strongest measured bin, and a conservative uncertainty based on local bin spacing and leave-one-out fit variation. The fitted resonance is marked directly on the graph. Peak magnitude and endpoint tilt use the same display scale, while CSV retains raw relative dB, the displayed value, refinement flags, and fit metadata. The result remains magnitude-only and includes the entire driver/interface chain.

### Relative phase

Five low-level shaped pulses vote on response sign. The result is positive, negative, or indeterminate. It is relative to driver face, winding, leads, input wiring, and interface phase—not absolute magnetic north/south.

## Projects and exports

- The **Customer** record stores name, address, phone, eMail, notes, and wind date in European `DD.MM.YYYY` format.
- The **Pickup** record is grouped into **Info** (Pickup ID, Guitar Type, and the six classification/direction checkboxes), **Wire** (Wire Type, Gauge, and wind count), **Hardware** (Pole Insulator, Protection, and Magnet Type), **Wires** (Leads, Start Wire/Ground, and End Wire/Hot), and **Properties** (Polarity, Phase, DCR, Inductance, and Capacitance). Pickup ID defaults to `NH 7k42 #1`. Wire Type offers Plain Enamel, Heavy Formvar, and Poly; Gauge offers AWG41 through AWG44; Polarity offers North or South; and Phase offers Negative or Positive. New projects default to Plain Enamel, AWG42, 7000 winds, Kapton Tape, Tissue, Waxed Pushback, Black ground/start, Yellow hot/end, South polarity, and Negative phase. Guitar Type, Magnet Type, Inductance, DCR, and Capacitance start blank. Calculated **Tonal Characteristics** uses type-neutral wording without a pickup-type prefix and is exposed in Summary, PNG, and PDF only when `?footprint=true` is active.
- With `?footprint=true`, the separate full-width **Tonewinder** subsection stores a named profile plus **Global** values (Turns, Start, Direction, Wire Gauge, ATC Wire tension initial → final, and Winding Speed) and **Scatter Parameters** (Turns Pre-Scatter, Turns Post-Scatter, Filling factor Pre/Post, Min/Max Filling factor, and Turns Scatter Change). It is hidden by default. Tonewinder **Start** is restricted to Left or Right, and **Direction** to CW or CCW; new records default to Left and CW while the remaining Tonewinder values start blank. Hidden Tonewinder data remains part of project persistence and CSV exports.
- **Project comparison** keeps six independent project snapshots. The entire large slot card and its matching fitted-resonance readout are mouse- and keyboard-selectable, while the **Show** checkbox independently controls the colored Bode trace. The active card and resonance readout are strongly highlighted, and all six fitted-resonance values remain visible together above the graph. Slot colors are blue, lime, orange, white, purple, and teal; the selected project's graph changes to an emphasized red line. **Store** copies the current project and measurements into the active slot. **Clear slot** removes the selected snapshot after confirmation, while **Clear All** confirms before removing every stored slot. **Save to file**, **Load from file**, and **Create PDF** operate on the active slot; loading accepts version 2, migrates compatible version-1 data, and remains compatible with legacy `.pickup-health` files. The former Project-panel Save, Load, and PDF buttons are intentionally omitted. The six slots and visibility choices persist locally.
- **Export CSV** contains Created and Updated in European `DD.MM.YYYY` format, the customer, pickup, and Tonewinder records, four Summary overview cards, every displayed measurement, all Spectrum metrics, averaged spectrum points, time/frequency/level waterfall cells, saturation harmonic/transfer data, and Bode measured level, generated output level, robust level, raw relative dB, displayed relative value, SNR, learned floor, interpolation/refinement flags, and fitted-resonance metadata, plus phase votes and every phase waveform sample.
- **Create PDF** in Project comparison freezes the currently selected slot into a snapshot and creates that project's polished multi-page A4 record locally, so switching or editing controls cannot mix another project's data into the export. The record includes a branded header and logo, project/customer information, pickup properties grouped as **Info**, **Wire**, **Hardware**, **Wires**, and **Properties**, test settings, a dedicated **Overview** page, two measurement pages, and a multi-page annex glossary copied directly from every measurement tooltip. By default the Overview contains fitted resonance, Relative Phase, DCR, Inductance, Capacitance, and Compression. When the app URL contains `?footprint=true`, it additionally contains the accent-to-orange horizontal-bar Tone Footprint and Tonal Characteristics, and the PDF gains a separate final **Tonewinder** page. Tonal Characteristics remains omitted from the Project Information pickup section. Its Audio Routing section places **Input Device** beside **Input Channel** on one row and **Output Device** beside **Output Channel** on the next. PDF Measurement Settings contains only **Input Trim** and **Output Level**. The first measurement page places Bode response above Relative phase, and the second places Saturation above Spectrum. The **Spectrum Data** section includes the measured spectral waterfall; Relative phase remains data-only. The Bode, Saturation, and spectral-waterfall graphs appear with their data, and the fitted Bode resonance is marked while the fitted frequency, strongest measured bin, and uncertainty are listed. Pickup selections render as checked or empty boxes in three vertical pairs: Guitar above Bass, Single Coil above Humbucker, and Clockwise above Counterclockwise. Project ID is omitted; Created and Updated use European `DD.MM.YYYY` formatting. The footer contains only the configured lab name, with no separator, page number, or timestamp. Its PDF-only logo is embedded to keep canvas export secure when the app is opened directly from disk.
- **Export PNG** uses the current theme and mirrors the visible Summary tab. Tone Footprint and Tonal Characteristics are included only when `?footprint=true` is active. The **Export PNG** and **Export CSV** buttons stay together in a spaced toolbar at the top of Summary.

The **Settings** analysis tab lets you change the tool name (default **ИH Custom Winds**) and lab name (default **Nicks Pickup Lab**). Press **Apply** to update the header, hero, browser title, and export branding. These names are stored with saved projects and restored when a project is loaded.

The complete serializable application state is saved automatically under the browser-local key `ih-custom-winds.local-state.v1`. Reloading restores project/customer/pickup fields, all measurement data and graphs, settings, branding, theme, active tab, preferred input/output devices and channels, and the six comparison slots with their active/visible states. Imported project files immediately replace and update the local state. Corrupt or incompatible stored data is discarded safely without blocking startup, and a one-time warning appears if browser storage is unavailable or full.

Live microphone streams, Web Audio nodes, active measurements, and learned route-noise/calibration buffers are intentionally session-only. After reload, audio remains disconnected until permission is granted; reconnecting relearns the route noise floor according to the normal three-second calibration rule.

## Themes, responsive behavior, and accessibility

The header theme button cycles through **Light**, **Dark orange**, **Dark green**, and **Dark blue**, displaying the active theme name. Dark green is the first-run default and uses acid-green `#d5fe42` accents; Dark blue remains available with vibrant blue accents, and Light uses neutral surfaces with dark blue. Theme selection is restored from local storage and redraws every source and Summary canvas; PNG and CSV exports identify and use the selected palette.

Controls are native, labelled, and keyboard accessible. Every single-line text/number field and dropdown uses the same 40 px height; multiline notes remain resizable. Measurement and graph tooltips work with pointer hover, keyboard focus, and touch. Plots remain fixed in height while data accumulates, resize horizontally, cap backing-store scale at `2×` device pixel ratio, and stack on mobile. Summary sections and their metric grids collapse cleanly to one column on narrow phones.

## Quality checklist

- Keep driver geometry and all analog gains fixed.
- Warm up active electronics and the driver amplifier.
- Use the same sample rate for a comparison series.
- Record battery condition and instrument-control positions.
- Repeat a reference pickup periodically to quantify fixture drift.
- Reject clipped captures and investigate high transient index during noise tests.
- Allow the driver to cool between long or high-level noise runs.
- Compare complete curves and confidence indicators, not one headline value.
- Save the project immediately after a clean series.

## Limitations

- Browser and interface timing are not laboratory-instrument synchronized.
- The response is not de-embedded from DAC, amplifier, driver coil, fixture, pickup loading, cable, or ADC.
- Bode and noise results are magnitude-only.
- White-noise harmonic metrics cannot separate excitation energy from distortion as cleanly as a single-tone analyzer.
- The app cannot sense driver-coil temperature or external amplifier clipping.
- Comparative results can be excellent; certification-grade absolute results require calibrated hardware and a controlled fixture.

## Troubleshooting

**No input prompt** — Reload the page, press **Allow audio access** on the splash, use localhost/HTTPS, and check site permissions. The app automatically retries with simpler, browser-compatible constraints when Chrome or Safari rejects an advanced audio request.

**White-noise response is missing** — Confirm the selected output device/channel, driver amplifier, coil continuity, and selected input. Use the 440 Hz tone at low level first.

**Fundamental seems wrong** — Broadband excitation can make the harmonic-score estimate ambiguous. Treat it as a comparative hint and use the dedicated saturation test for more defensible harmonic measurements.

**Output comes from the wrong interface or channel** — Select the required device and hardware channel in the Output group. If the browser refuses a non-default device, grant the output-selection prompt or use a browser that supports Web Audio output-sink selection.
