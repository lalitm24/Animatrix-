# Task 2 Critique - Fourier Series

## Issue 1: No Legend Box
- **Problem:** Labels on right side are small and hard to read
- **Impact:** Viewer cannot easily match colors to harmonic numbers
- **Fix:** Add a proper legend box with colored squares and labels

## Issue 2: X-axis Missing Pi Labels
- **Problem:** X-axis shows plain numbers instead of π, 2π, 3π, 4π
- **Impact:** Viewer cannot relate x-axis values to wave period
- **Fix:** Use custom x_axis_labels with MathTex pi symbols

## Issue 3: Confusing First Cumulative Transform
- **Problem:** Transform from harmonic_plot.copy() is visually unclear
- **Impact:** Viewer confused about difference between harmonic and sum
- **Fix:** Use ReplacementTransform with clearly separate objects

## Issue 4: All Harmonics Stay Visible and Overlap
- **Problem:** All 5 harmonic curves shown simultaneously
- **Impact:** Screen becomes cluttered making cumulative sum hard to see
- **Fix:** Fade out individual harmonics after adding to cumulative sum

## Issue 5: Equal Animation Speed for All Harmonics
- **Problem:** Each harmonic takes same run_time regardless of visual change
- **Impact:** Later harmonics show tiny changes but take same time as first
- **Fix:** Reduce run_time progressively for later harmonics
