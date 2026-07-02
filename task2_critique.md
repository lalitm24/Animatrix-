# Review of Task 2 – Fourier Series Animation

## 1. Legend Could Be More Informative

**Observation:** The harmonic labels are placed along the right side of the scene without a dedicated legend.

**Effect:** It is difficult to quickly associate each curve with its corresponding harmonic.

**Suggested Improvement:** Introduce a compact legend box containing colored markers and matching harmonic labels for improved readability.

---

## 2. Missing π-Based Axis Labels

**Observation:** The x-axis uses standard numeric values instead of mathematical labels such as ( \pi ), (2\pi), (3\pi), and (4\pi).

**Effect:** The periodic nature of the waveform is less intuitive for the viewer.

**Suggested Improvement:** Replace the default tick labels with `MathTex` expressions representing the appropriate multiples of ( \pi ).

---

## 3. Initial Cumulative Transition Is Unclear

**Observation:** The first cumulative waveform is created using `harmonic_plot.copy()`, making the transition difficult to interpret.

**Effect:** Viewers may struggle to distinguish the individual harmonic from the cumulative approximation.

**Suggested Improvement:** Use a `ReplacementTransform` between clearly separated objects to produce a more understandable animation.

---

## 4. Harmonic Curves Create Visual Clutter

**Observation:** Every harmonic remains visible after it is introduced.

**Effect:** Multiple overlapping curves reduce the clarity of the cumulative Fourier approximation.

**Suggested Improvement:** Gradually fade out each individual harmonic once it has been incorporated into the cumulative sum.

---

## 5. Uniform Animation Timing

**Observation:** Every harmonic is animated with the same `run_time`.

**Effect:** Later harmonics contribute only minor visual changes but occupy the same amount of animation time as the earlier, more significant harmonics.

**Suggested Improvement:** Decrease the animation duration progressively for higher-order harmonics to maintain a smoother viewing experience.
