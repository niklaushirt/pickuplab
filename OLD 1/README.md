# Nicks Pickup Lab

Nicks Pickup Lab is a self-contained browser instrument for comparative guitar and bass pickup testing. It uses a real audio-interface input and a repeatable magnetic driver or tap fixture to measure:

- Multi-tap impulse response, retaining the cleanest capture
- Captured impulse waveform, logarithmic decay envelope, and resonant-ring FFT
- Ring frequency, estimated T60, damping ratio ζ, Q, first-swing polarity, and rise time
- Band-selectable white-noise response over 2.5, 5, or 10 seconds
- 24 time- and frequency-domain noise-response indicators
- Magnetic saturation, 500 Hz–8 kHz Bode magnitude, and five-pulse relative polarity
- A fixed 440 Hz routing/reference tone
- JSON project save/load, CSV data export, and theme-aware PNG summary export

The app is entirely contained in [index.html](./index.html). Audio stays in the browser tab. There are no dependencies, external assets, uploads, network requests, telemetry services, or automatic recordings.

## Files

```text
index.html   Complete application, styling, audio engine, plots, and embedded icons
README.md    User guide, safety guidance, and driver construction
PROMPT.md    Full reconstruction specification
```

## Start locally

Audio permission requires a secure browser context. `localhost` qualifies:

```bash
cd /path/to/PICKUP_HEALTH
python3 -m http.server 4173
```

Open `http://127.0.0.1:4173` in a current browser. The opening splash follows the active theme and describes audio access but does not request permission automatically. Press **Allow audio access** to connect. **Explore first** closes the splash without requesting access; reload the page when you are ready to connect an input.

## Signal path

```text
440 Hz / automated test output
  → operating-system default audio output
  → suitable headphone or power amplifier
  → repeatable magnetic driver coil
  → magnetic coupling across a fixed gap
  → pickup under test
  → interface Hi-Z input and selected channel
  → browser analysis
```

The impulse/tap test is input-only: it waits for repeated physical or magnetic impulses and never starts output. White noise, saturation, Bode, pulse-polarity, and the 440 Hz tone use the operating system's default output. There is intentionally no output-device or output-channel selector.

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

The safety checkbox is a deliberate reminder, not an electrical protection circuit.

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
8. Permanently mark the driver face, winding direction, and lead polarity.
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

The first five analysis tabs—**Bode response**, **Noise spectrum**, **Saturation**, **Polarity**, and **Impulse / tap**—contain their setup, start button, progress, graphs, and measurements. Bode response is the initial tab. Each primary measurement-action row has clear vertical breathing room above and below. The **Summary** tab contains a synchronized second copy of every graph and measurement in the same order.

The glowing **Measure All** button beside **Clear measurements** runs the five tests sequentially in tab order: Bode, Noise, Saturation, Polarity, then Impulse. The app opens each tab as its measurement starts, waits for every test to finish, and returns to Bode when the sequence completes, fails, or is stopped. The final impulse step still requires the selected number of physical taps. One centered toaster confirms when all five measurements finish successfully; **Stop output** cancels the active test and the remaining sequence.

Every result value has a `?` explanation button describing its role, interpretation, and main caveat. Every graph heading has the same explanation control. The buttons work by hover, keyboard focus, and touch; tap elsewhere or press Escape to dismiss. Explanation boxes use the same large, orange-accented blurred-glass treatment as centered notification messages. The graphs themselves also show exact cursor-position values on hover or touch-drag.

## 440 Hz test tone

**Play 440 Hz test tone** produces a continuous sine wave through the operating system's default output at the selected test-output level. It requires an input connection and the safety confirmation. Press the same button or **Stop output** to ramp it down.

The button is intended only for routing, gain, and polarity-chain checks. It replaces the former free-form excitation generator.

## Impulse response / tap test

Choose 3, 5, or 7 impulses and press **Capture tap series**. For every tap, the detector:

1. Measures a short quiet baseline.
2. Sets a threshold from the measured noise, with a conservative minimum.
3. Shows `TAP NOW` and waits up to 15 seconds.
4. Captures approximately 1.5 seconds around the event.
5. Scores peak-to-noise ratio and penalizes clipping and strong secondary impacts.

After the series, the app keeps the highest-scoring capture. Use the same nonmagnetic plectrum, repeatable solenoid, small steel target, or other safe fixture for each impulse. A hand tap is useful diagnostically but is less repeatable.

### Impulse plots

- **Captured waveform** is the cleanest aligned, normalized response.
- **Decay envelope** uses 5 ms RMS blocks on a logarithmic dB scale. A least-squares decay line is fitted primarily from −5 to −40 dB.
- **FFT of resonant ring** uses the early aligned response and identifies its strongest 60 Hz–10 kHz component.

These plots appear in the **Impulse / tap** tab and as synchronized copies in Summary. Every plot has a fixed height and a cursor tooltip with the value nearest the pointer.

### Impulse values

- **Ring frequency** — strongest early-decay spectral component.
- **Decay time / T60 estimate** — time for the fitted amplitude envelope to fall 60 dB. It is extrapolated when the captured signal reaches the noise floor earlier.
- **Damping ratio ζ** — estimated as `1 / (2Q)`. Smaller values mean a more lightly damped ring.
- **Q from ring** — derived from frequency and decay: `Q = π × f × T60 / 6.9078`.
- **First-swing polarity** — sign of the strongest initial excursion after onset. It is relative to the unchanged input wiring and tap direction.
- **Rise time** — interval from 10% to 90% of the first peak.

T60, Q, and ζ are model-based estimates. Multiple modes, noisy envelopes, irregular tapping, active electronics, mechanical vibration, and short capture windows can make the fit unresolved or misleading.

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
| Crest factor | Peak-to-RMS ratio; low values can indicate compression or clipping. |
| DC offset | Mean sample value as percent of full scale. |
| Noise floor | Median spectral-bin level in the selected span. |
| SNR estimate | Difference between spectral peak and median spectral floor. |
| Spectral centroid | Power-weighted spectral center, often perceived as brightness. |
| 85% roll-off | Frequency below which 85% of selected-band power lies. |
| Spectral bandwidth | Power-weighted spread around the centroid. |
| Spectral flatness | Geometric/arithmetic mean power ratio; high is flat/noise-like. |
| Spectral slope | Fitted level trend in dB per octave. |
| THD estimate | Harmonics 2–8 relative to estimated fundamental; screening-only under noise excitation. |
| Even / odd | Even-harmonic to odd-harmonic energy ratio in dB. |
| Peak asymmetry | Positive/negative waveform peak ratio in dB. |
| Zero crossings | DC-removed sign changes per second. |
| Clipped samples | Count at or beyond ±0.999 full scale; any nonzero value invalidates critical conclusions. |
| Transient index | Strongest 20 ms RMS block divided by median block RMS. |
| Nearest note | Equal-tempered note nearest the estimated fundamental, A4 = 440 Hz. |
| Low band | Integrated selected-span spectral energy below 250 Hz. |
| Mid band | Integrated selected-span spectral energy from 250 Hz to 2 kHz. |
| High band | Integrated selected-span spectral energy above 2 kHz. |
| Tone confidence | Confidence that the harmonic-score fundamental is periodic rather than broadband. |

Low tone confidence is normal for a relatively flat white-noise response. THD, even/odd, nearest note, and “fundamental” should then be treated as diagnostic hints, not authoritative measurements. For more defensible distortion results, use the dedicated stepped-tone saturation test.

## Existing guided measurements

### Magnetic saturation

Eight 1 kHz steps measure pickup RMS output, fundamental, combined even harmonics, combined odd harmonics, half-cycle asymmetry, and transfer compression. Even harmonics growing faster than odd while the transfer curve bends asymmetrically can suggest magnetic saturation, but driver-amplifier or interface distortion can mimic it.

### Bode magnitude

Thirty logarithmically spaced tones cover 500 Hz–8 kHz. Results normalize to the strongest point and report peak resonance, peak level, and endpoint tilt. It is magnitude-only and includes the entire driver/interface chain.

### Relative polarity

Five low-level shaped pulses vote on response sign. The result is positive, negative, or indeterminate. It is relative to driver face, winding, leads, input wiring, and interface polarity—not absolute magnetic north/south.

## Projects and exports

- **Save project** downloads version-2 JSON data using the single `.pickup-health` filename extension. It contains settings, full impulse results, cleanest-capture metadata, envelope, impulse FFT, all noise metrics and spectrum points, saturation, Bode, polarity, notes, and timestamps.
- **Load project** accepts version 2 and migrates compatible version-1 files.
- **Export CSV** contains the four Summary overview cards, every displayed measurement, raw impulse waveform/envelope/fit/FFT data, all noise metrics and spectrum points, saturation harmonic/transfer data, Bode points, polarity votes, and every polarity waveform sample.
- **Export PNG** uses the current theme and renders the complete Summary dashboard: all overview information, notes, 42 detailed measurements, and all eight graphs. The two export buttons stay together in a spaced toolbar at the top of Summary.

No project data or theme is persisted automatically. Reloading always starts in **Dark blue**.

## Themes, responsive behavior, and accessibility

The header theme button cycles through **Light**, **Dark orange**, **Dark green**, and **Dark blue**, displaying the active theme name. Dark blue is the default and uses vibrant blue accents; Dark green uses acid-green `#d5fe42` accents, and Light uses neutral surfaces with dark blue. Theme selection is session-only and redraws every source and Summary canvas; PNG and CSV exports identify and use the selected palette.

The document embeds a text-free blue/cyan single-coil favicon as scalable SVG with a 32×32 PNG fallback. It also embeds an opaque 180×180 PNG Apple touch icon and the Apple standalone-title/status-bar metadata used when the page is added to an iPhone home screen. No external icon files are required.

Controls are native, labelled, and keyboard accessible. Every single-line text/number field and dropdown uses the same 40 px height; multiline notes remain resizable. Measurement and graph tooltips work with pointer hover, keyboard focus, and touch. Plots remain fixed in height while data accumulates, resize horizontally, cap backing-store scale at `2×` device pixel ratio, and stack on mobile. Summary sections and their metric grids collapse cleanly to one column on narrow phones.

## Quality checklist

- Keep driver geometry and all analog gains fixed.
- Warm up active electronics and the driver amplifier.
- Use the same sample rate for a comparison series.
- Record battery condition and instrument-control positions.
- Repeat a reference pickup periodically to quantify fixture drift.
- For taps, use the same impact device, direction, force range, and point.
- Reject clipped captures and investigate high transient index during noise tests.
- Allow the driver to cool between long or high-level noise runs.
- Compare complete curves and confidence indicators, not one headline value.
- Save the project immediately after a clean series.

## Limitations

- Browser and interface timing are not laboratory-instrument synchronized.
- The response is not de-embedded from DAC, amplifier, driver coil, fixture, pickup loading, cable, or ADC.
- Bode and noise results are magnitude-only.
- Tap T60 assumes a primarily exponential decay; multiple resonances violate that simple model.
- White-noise harmonic metrics cannot separate excitation energy from distortion as cleanly as a single-tone analyzer.
- The app cannot sense driver-coil temperature or external amplifier clipping.
- Comparative results can be excellent; certification-grade absolute results require calibrated hardware and a controlled fixture.

## Troubleshooting

**No input prompt** — Reload the page, press **Allow audio access** on the splash, use localhost/HTTPS, and check site permissions.

**Tap never triggers** — Tap more firmly, reduce background noise, increase analog input gain without clipping, and confirm the selected input channel.

**Tap triggers before contact** — Stop vibration, mute strings, move cables carefully, and reduce environmental noise before arming.

**T60 or Q is unresolved** — Increase signal-to-noise ratio, use a cleaner single impact, capture more taps, and avoid a second impact during decay.

**White-noise response is missing** — Confirm the operating-system default output, driver amplifier, coil continuity, selected input, and safety checkbox. Use the 440 Hz tone at low level first.

**Clipped samples are nonzero** — Lower the interface's analog input gain, then lower test-output or external-amplifier level and repeat.

**Fundamental or nearest note seems wrong** — Check tone confidence. These values are intentionally low-authority under broadband excitation.

**Output comes from the wrong interface** — Change the operating system's default output. The app intentionally has no output selector.
