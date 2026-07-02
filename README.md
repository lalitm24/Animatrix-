
# Manim GenAI Assignment

## Project Overview
Used Google Gemini API to automatically generate Manim animation
code for two mathematical concepts and critically evaluated output.

## Setup Instructions
pip install -r requirements.txt

## How to Run

### Task 1 - Pythagorean Theorem
manim -pql task1_pythagorean/pythagoras.py PythagorasScene

### Task 2 - Fourier Series
manim -pql task2_fourier/fourier_series.py FourierSeriesScene

## Key Findings
- Gemini generated mostly working code structure
- Task 1: Missing right angle marker, hardcoded square sizes
- Task 2: Missing pi labels on x-axis, no proper legend box
- Both scenes needed LaTeX installation to render MathTex
