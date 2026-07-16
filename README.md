# Nicks Pickup Lab

A single-file browser workbench for measuring guitar and bass pickups through an audio interface. It combines a live analyzer, controlled magnetic excitation, Bode response measurement, saturation mapping, relative polarity detection, and exportable measurement summaries.

Everything runs locally in [`pickup-lab.html`](./pickup-lab.html). No samples or measurements are uploaded.

> [!CAUTION]
> Use an audio interface's **Hi-Z / Instrument input** for the pickup. Drive the magnetic test coil only through a suitable current-limiting resistor. Never connect an interface output directly to a pickup, short an output, use a power amplifier, or work with mains voltage.

## Quick start

1. Connect the pickup to a Hi-Z input on the audio interface.
2. Connect the interface or headphone output to a current-limited magnetic driver coil as described below.
3. Serve the folder from localhost:

   ```sh
   python3 -m http.server 8000
   ```

4. Open <http://localhost:8000/pickup-lab.html> in a current Chromium-based browser.
5. Click **Allow audio input**, select the correct input device and channel, and start the analyzer.
6. Select the desired output device and channel. Begin with low hardware gain even though the application's output-level default is −3 dBFS.

Audio permission is requested only after the **Allow audio input** button is clicked. Output-device enumeration and routing depend on browser and operating-system support.

### Opening splash

The application opens with a branded **Nicks Pickup Lab** splash featuring the `PL` icon and a short overview of its response, resonance, polarity, and magnetic-saturation measurements. A warm orange ambient glow highlights the card and both permission controls.

The visual presentation does not change the privacy flow: loading the page never opens the browser's audio prompt. **Allow audio input** is the only button that requests microphone access; **Not now** simply dismisses the splash. Audio remains local to the page.

## What it measures

### Live Measurements

The live analyzer provides:

- Peak and estimated fundamental frequency
- RMS and sample-peak level
- Crest factor, transient index, DC offset, and waveform asymmetry
- Noise floor, estimated SNR, clipping percentage, and zero-crossing rate
- Spectral centroid, roll-off, bandwidth, flatness, and slope
- THD estimate and even/odd harmonic balance
- Low, mid, and high-band energy
- Nearest note and tone-confidence estimate

Measurement cards can be averaged from real time to 30 seconds. The adjustable noise-floor threshold suppresses input frames and spectrum bins below the selected dBFS level.

### Magnetic Saturation Mapper

Runs stepped sine bursts through the driver coil and compares pickup output against drive level. It estimates:

- Compression onset
- Maximum compression
- Positive/negative peak asymmetry
- Harmonic distortion at maximum drive

The drive value is a repeatable dBFS fixture reference—not a gauss measurement. Interface or headphone-amplifier clipping can look like pickup saturation, so validate the signal chain before interpreting results.

### Bode Plot

Measures the pickup's relative magnitude response from **500 Hz to 8 kHz** using a logarithmic sweep. Excitation falls by **−6 dB per octave** above 500 Hz. The graph is lightly smoothed and marks the highest measured magnitude with its dB and kHz values.

The result includes the complete fixture response: output stage, series resistor, driver coil, magnetic spacing, pickup load, cable, and input stage. Keep all of these fixed when comparing pickups.

### Relative Polarity

Emits repeated positive-leading magnetic pulses, averages the pickup response, and reports **POSITIVE**, **NEGATIVE**, or **INCONCLUSIVE**. The result is relative to the documented coil face, coil wiring, output polarity, pickup magnet face, and pickup lead connected to input hot.

### Summary export

After taking measurements, **Create summary** collects all available non-null results from the saturation mapper, Bode plot, polarity test, and live analyzer. The summary can be exported as PNG or CSV.

---

## Build a repeatable magnetic driver

The driver converts an interface-output signal into a small alternating magnetic field. The pickup senses that field without an electrical connection between the driver and pickup circuits.

```text
Interface/headphone OUT + ── series resistor ── driver coil ── OUT return
                                                )))))
                                           magnetic field
                                                (((((
Pickup hot ───────────────────────────────────────────> Hi-Z input
Pickup return ────────────────────────────────────────> input return
```

### Suggested parts

| Part | Practical starting point |
| --- | --- |
| Coil former | Non-magnetic plastic, acrylic, cardboard, or 3D-printed bobbin |
| Coil | Air-core, approximately 8–15 mm inner diameter and 8–15 mm winding length |
| Wire | 0.15–0.25 mm enamelled copper wire, approximately 300–600 turns |
| Series resistor | Start with **1 kΩ, 0.5 W or greater**; reduce only after verifying the output's safe load and current |
| Cable | Short twisted pair from the output to the driver coil |
| Fixture | Wood, acrylic, or printed frame with nylon/brass fasteners and a repeatable height stop |
| Tools | Multimeter, ruler or caliper, soldering tools, heat-shrink, and a non-magnetic spacer gauge |

These values are deliberately conservative starting points, not a calibrated standard. Coil resistance, inductance, geometry, interface capability, and required field strength vary. Record the final values used for every comparison.

### 1. Wind and document the coil

1. Use an air-core, non-ferromagnetic former. Steel screws or a magnetic core can reshape the field and introduce hysteresis or saturation.
2. Wind all turns in one direction with even tension. Secure the winding with tape, varnish, or heat-shrink that does not move the coil.
3. Mark the two leads **START** and **FINISH**.
4. Mark one physical face **PICKUP SIDE** and draw an arrow showing the winding direction when viewed from that face.
5. Measure and record the coil's DC resistance. If possible, also measure its inductance at a stated test frequency.

A useful fixture record looks like this:

```text
Driver ID:        Coil A
Turns:            420
Wire diameter:    0.20 mm
DC resistance:    18.6 Ω
Inductance:       1.2 mH @ 1 kHz
Pickup-side face: Face A
Output + lead:    START
Series resistor:  1.0 kΩ
```

### 2. Add current limiting

Place a resistor in series with the coil. A large series resistance protects the output and makes coil current less dependent on small resistance changes.

For a conservative low-frequency estimate:

```text
I_rms ≈ V_rms / (R_series + R_coil)
P_resistor ≈ I_rms² × R_series
```

At higher frequencies the coil's inductive reactance also matters:

```text
|Z| ≈ √((R_series + R_coil)² + (2πfL)²)
I_rms ≈ V_rms / |Z|
```

Choose a resistor power rating with generous headroom—at least twice the calculated dissipation. A line output may require a much lighter load than a headphone output, so consult the interface specification before reducing the starting 1 kΩ value.

> [!IMPORTANT]
> Application dBFS is not output voltage. Measure the actual output voltage if current or heating matters. Begin around −40 dBFS with the interface's hardware volume low, then increase gradually while watching the pickup input and checking that the output stage, resistor, and coil remain cool and clean.

### 3. Build a fixed mechanical jig

Repeatability depends more on geometry than absolute output level.

1. Mount the pickup in a cradle that fixes its left/right and front/back position.
2. Mount the driver on a rigid arm above the pickup using non-magnetic hardware.
3. Add a hard height stop or interchangeable spacer. A starting gap of **3–10 mm** is practical; choose one value and keep it unchanged.
4. Add alignment marks for X, Y, Z position, coil face, and rotation.
5. Prevent the coil cable from pulling on the arm or changing the gap.
6. Photograph the completed setup with a ruler in view.

For pickups with multiple pole pieces, define whether the coil is centered over one pole, between two poles, or over the pickup centerline. Do not change this convention between tests.

### 4. Wire the fixture

1. Connect interface/headphone output hot to the series resistor.
2. Connect the resistor to the marked coil **START** lead.
3. Connect coil **FINISH** to the output return.
4. Connect the pickup separately to the Hi-Z input.
5. Add strain relief and insulate every exposed joint.

There should be magnetic coupling between the two circuits, not a deliberate electrical connection from the output signal to the pickup hot lead.

### 5. Establish a polarity convention

Write down all four references before using the polarity result:

- Driver-coil face toward the pickup
- Driver winding direction
- Output lead connected to coil START
- Pickup lead connected to Hi-Z input hot

Swapping either pair of driver leads or pickup leads reverses the reported polarity. With the convention fixed, the application's **POSITIVE** and **NEGATIVE** results become repeatable across pickups.

### 6. Validate before measuring pickups

1. **Continuity:** verify the coil and resistor path with a multimeter.
2. **Safe load:** confirm the total load is allowed for the selected interface output.
3. **Low-level test:** start with low hardware volume and approximately −40 dBFS.
4. **Noise check:** with the generator stopped, set the threshold just above the stable background noise.
5. **Electrical loopback:** through a suitable attenuator, verify that the interface remains linear and symmetrical across the planned drive range. Never feed a hot output directly into a microphone or instrument input.
6. **Repeatability:** remove and reinstall the pickup, then repeat a low-level run. Large changes indicate mechanical-positioning problems.
7. **Reference part:** periodically measure the same known pickup to detect fixture drift.

### Improving measurement repeatability

- Use the same interface, sample rate, output channel, input channel, and hardware gain.
- Record pickup height, coil gap, coil orientation, and temperature.
- Keep pickup loading fixed: pot values, tone capacitor, cable capacitance, and input impedance all affect resonance.
- Use the same series resistor and driver coil for every comparison.
- Allow the coil and resistor to cool between high-drive tests.
- Monitor driver current with a known sense resistor if absolute field consistency is important.
- Treat Bode plots as relative unless the driver's magnetic field versus frequency has been independently characterized.

## Recommended measurement order

1. Start the analyzer and verify the selected input channel.
2. Set the input gain so the strongest expected signal remains below clipping.
3. Set the noise threshold just above the idle noise floor.
4. Run a low-level Bode measurement.
5. Run the polarity test and record the fixture convention.
6. Run the saturation map last, increasing drive gradually.
7. Create and export the measurement summary.

## Limitations

- dBFS values are referenced to the interface, not directly to volts, tesla, or gauss.
- Browser and operating-system audio routing can differ.
- Interface DSP, automatic gain, noise suppression, and sample-rate conversion can invalidate measurements.
- The Bode plot contains the magnetic driver and pickup loading response unless separately calibrated.
- The saturation mapper cannot distinguish pickup nonlinearity from driver, headphone amplifier, preamp, or ADC nonlinearity without control measurements.
- Relative polarity is meaningful only when the physical and electrical fixture convention is documented.

## Project files

```text
pickup-lab.html   Complete application; no build step or external libraries
README.md         Setup, workflow, fixture construction, and safety guidance
```

## Privacy

Audio analysis and exports are produced locally in the browser. The application does not upload audio or measurement data.
