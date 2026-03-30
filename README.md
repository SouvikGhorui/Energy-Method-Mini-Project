# Energy Methods and Uniqueness of IBVPs
 
**Mini Research Project — MAL5030 (Partial Differential Equations)**
**M.Sc. Mathematics | IIT Jodhpur**
**Author: Souvik Ghorui (M25MA2008)**
 
---
 
## Overview
 
This repository contains all materials for a mini research project on **energy methods** as a tool for proving uniqueness of solutions to **Initial Boundary Value Problems (IBVPs)** for classical PDEs. The project covers the theoretical foundations, formal proofs, numerical simulations, and an animated presentation.
 
The central idea is elegant: by defining an appropriate *energy functional* associated with a PDE solution and showing it must be zero (or decay monotonically), one can prove uniqueness without explicitly constructing the solution.
 
---
 
## Repository Structure
 
```
Energy-Method-Mini-Project/
│
├── Energy_method_mini_research.tex        # LaTeX source for the research report
├── Energy_method_mini_research.pdf        # Compiled research report (PDF)
│
├── PDE Presentation/
│   ├── energy_method_slides.py            # Manim Slides source code (animated presentation)
│   ├── generate_slides.bat                # Windows batch script to compile slides
│   ├── present.bat                        # Windows batch script to launch presentation
│   ├── media/                             # Manim-generated media assets
│   └── slides/                            # Compiled slide outputs
│
├── damped-wave.html                       # Interactive simulation: Damped Wave Equation
├── reaction_diffusion.html                # Interactive simulation: Reaction-Diffusion Model
│
├── Partial Differential Equations An Introduction.pdf   # Reference textbook
└── sharp-hadamard.pdf                     # Reference: Sharp/Hadamard well-posedness
```
 
---
 
## Topics Covered
 
### 1. The Energy Method — Core Idea
The method works by defining an energy functional $E(t)$ for the *difference* of two hypothetical solutions. Using integration by parts and boundary conditions, one shows:
 
$$\frac{dE}{dt} \leq 0 \quad \text{and} \quad E(0) = 0 \implies E(t) \equiv 0$$
 
This forces the two solutions to be identical, proving **uniqueness**.
 
### 2. Heat Equation (Dirichlet IBVP)
 
$$u_t = k\, u_{xx}, \quad x \in (0, L),\; t > 0$$
 
with homogeneous Dirichlet boundary conditions. The energy functional used is:
 
$$E(t) = \frac{1}{2} \int_0^L w^2(x, t)\, dx$$
 
where $w = u_1 - u_2$ is the difference of two solutions. We show $E'(t) \leq 0$, so $E(t) = 0$ for all $t \geq 0$.
 
### 3. Wave Equation (Mixed IBVP)
 
$$u_{tt} = c^2 u_{xx}, \quad x \in (0, L),\; t > 0$$
 
The energy functional incorporates both kinetic and potential energy:
 
$$E(t) = \frac{1}{2} \int_0^L \left[ w_t^2 + c^2 w_x^2 \right] dx$$
 
We show $E'(t) = 0$ (energy conservation), hence $E(t) \equiv E(0) = 0$.
 
### 4. Reactive Diffusion Equation
 
Extension of the heat equation with a reaction term:
 
$$u_t = D \cdot u_{xx} + f(u)$$
 
Uniqueness analysis under suitable Lipschitz conditions on $f$, using Gronwall's inequality alongside the energy method.
 
### 5. Damped Wave Equation
 
$$u_{tt} + 2\alpha \cdot u_t = c^2 u_{xx}$$
 
The modified energy functional accounts for damping, and we show strict energy decay: $E'(t) \leq 0$.
 
---
 
## Deliverables
 
| Deliverable | Description | Format |
|---|---|---|
| Research Report | Full proofs, energy functional constructions, uniqueness theorems | `.pdf` / `.tex` |
| Animated Presentation | 14-slide Manim Slides deck with animated diagrams and plots | Manim Slides |
| Interactive Simulations | Browser-based numerical demos for damped wave and reaction-diffusion | `.html` |
 
---
 
## Interactive Simulations
 
Two standalone HTML simulations are included — no installation required, just open in any browser.
 
### `damped-wave.html`
Visualizes the evolution of a **damped wave** over time. Allows interactive control over parameters like damping coefficient $\alpha$, wave speed $c$, and initial conditions. Illustrates how the energy functional decays as $t \to \infty$.
 
### `reaction_diffusion.html`
Simulates a **reaction-diffusion system**, showcasing pattern formation (Turing patterns) arising from the interplay between diffusion and a nonlinear reaction term. Useful for visualizing behavior that motivates uniqueness constraints on $f(u)$.
 
---
 
## Animated Presentation (Manim Slides)
 
The `PDE Presentation/` folder contains a full animated slide deck built with [Manim Slides](https://manim-slides.eertmans.be/).
 
### Prerequisites
 
```bash
pip install manim manim-slides
```
 
### Compile the slides
 
```bash
cd "PDE Presentation"
generate_slides.bat
```
or manually:
```bash
manim-slides render energy_method_slides.py EnergyMethodSlides
```
 
### Present the slides
 
```bash
present.bat
```
or manually:
```bash
manim-slides present EnergyMethodSlides
```
 
---
 
## Research Report
 
The LaTeX source (`Energy_method_mini_research.tex`) can be compiled with any standard LaTeX distribution:
 
```bash
pdflatex Energy_method_mini_research.tex
```
 
Requires standard packages: `amsmath`, `amssymb`, `amsthm`, `tikz`, `geometry`, `hyperref`.
 
The compiled PDF is already included as `Energy_method_mini_research.pdf`.
 
---
 
## Key Mathematical Results
 
> **Theorem (Uniqueness for Heat Equation).** Let $u_1, u_2$ be two smooth solutions to the heat IBVP with identical initial and boundary data. Then $u_1 \equiv u_2$.
>
> *Proof sketch.* Set $w = u_1 - u_2$. Then $E(t) = \frac{1}{2}\int_0^L w^2\,dx$ satisfies $E'(t) = -k\int_0^L w_x^2\,dx \leq 0$. Since $E(0)=0$ and $E \geq 0$, we get $E \equiv 0$. $\square$
 
> **Theorem (Uniqueness for Wave Equation).** The same conclusion holds for the wave IBVP, with $E(t) = \frac{1}{2}\int_0^L (w_t^2 + c^2 w_x^2)\,dx$ satisfying $E'(t) = 0$.
 
---
 
## References
 
- Strauss, W. A. — *Partial Differential Equations: An Introduction* (2nd ed.) — included as `Partial Differential Equations An Introduction.pdf`
- Hadamard's well-posedness framework — see `sharp-hadamard.pdf`
- Evans, L. C. — *Partial Differential Equations*, AMS Graduate Studies in Mathematics
 
---
 
## License
 
This project is submitted as coursework for **MAL5030** at IIT Jodhpur. All original code, proofs, and simulations are authored by Souvik Ghorui. Reference PDFs are included for academic/educational use only.
 