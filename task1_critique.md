# Review of Task 1 – Pythagorean Theorem Animation

## 1. Right-Angle Indicator Missing

**Observation:** The generated animation does not display the conventional right-angle marker at vertex **A**.

**Effect:** It is not immediately obvious which angle of the triangle is (90^\circ).

**Suggested Improvement:** Insert a `RightAngle` mobject at vertex **A** to clearly highlight the right angle.

---

## 2. Fixed Square Dimensions

**Observation:** The attached squares are created using fixed displacement values such as `LEFT*3` and `DOWN*4`.

**Effect:** Any modification to the triangle's dimensions causes the squares to lose their geometric correctness.

**Suggested Improvement:** Compute each side length dynamically using `np.linalg.norm(B - A)` (and similarly for the other sides) before constructing the corresponding squares.

---

## 3. Missing Visual Legend

**Observation:** The animation lacks a legend describing the meaning of the colored regions.

**Effect:** Users must infer which colored square represents (a^2), (b^2), or (c^2).

**Suggested Improvement:** Create a small `VGroup` legend containing color-coded labels and position it in a corner of the scene.

---

## 4. Static Label Placement

**Observation:** Text labels are positioned using constant offsets rather than the actual geometry of the figure.

**Effect:** Labels may overlap the colored squares or appear too close to other objects when the figure changes.

**Suggested Improvement:** Position labels relative to the surrounding objects or their bounding boxes to ensure consistent spacing.

---

## 5. Hypotenuse Square Construction

**Observation:** The perpendicular direction used to build the square on the hypotenuse is not normalized.

**Effect:** As a result, the generated figure may not form a geometrically accurate square.

**Suggested Improvement:** Normalize the perpendicular vector with `np.linalg.norm` before scaling it to the required side length.
