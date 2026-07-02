# Manim Animation Generation using Generative AI

## Overview

This project explores the use of the Google Gemini API to generate Manim Community Edition animations for mathematical concepts. Two different prompts were tested, and the generated code was analyzed to identify its strengths and limitations.

## Installation

Install all required dependencies using:

```bash
pip install -r requirements.txt
```

## Running the Project

### Pythagorean Theorem Animation

```bash
manim -pql task1_pythagorean/pythagoras.py PythagorasScene
```

### Fourier Series Animation

```bash
manim -pql task2_fourier/fourier_series.py FourierSeriesScene
```

## Evaluation

### Pythagorean Theorem

* Generated code was largely functional.
* Right-angle indicator was not included.
* Square dimensions were manually hardcoded instead of being computed dynamically.

### Fourier Series

* X-axis labels for π were absent.
* A proper legend explaining the plotted curves was not generated.

## Observations

* Gemini produced a solid initial implementation for both animations.
* Minor manual corrections were required to improve visual quality and mathematical completeness.
* Rendering scenes containing `MathTex` requires a working LaTeX installation.
