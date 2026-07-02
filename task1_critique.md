# Task 1 Critique - Pythagorean Theorem

## Issue 1: No Right Angle Marker
- **Problem:** No small square symbol at vertex A to show 90 degrees
- **Impact:** Viewer cannot identify which angle is the right angle
- **Fix:** Add a RightAngle mobject at vertex A

## Issue 2: Hardcoded Square Sizes
- **Problem:** Squares use LEFT*3 and DOWN*4 instead of actual side lengths
- **Impact:** If triangle changes, squares won't match sides correctly
- **Fix:** Calculate size using np.linalg.norm(B-A) for actual distances

## Issue 3: No Color Legend
- **Problem:** No legend explaining RED=a², BLUE=b², GREEN=c²
- **Impact:** Viewer must guess what each color represents
- **Fix:** Add a legend VGroup in corner with colored labels

## Issue 4: Labels May Overlap Squares
- **Problem:** Side labels use fixed offsets regardless of shape size
- **Impact:** Labels can appear inside or on top of colored squares
- **Fix:** Use dynamic positioning based on actual shape boundaries

## Issue 5: Square on Hypotenuse May Be Incorrect
- **Problem:** Perpendicular vector not normalized to correct length
- **Impact:** The c² square may not be a true square visually
- **Fix:** Normalize the perpendicular vector using np.linalg.norm
