# Energy Methods and Uniqueness of IBVPs

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Manim](https://img.shields.io/badge/Manim-Slides-2E3440?style=for-the-badge&logo=manim&logoColor=ECEFF4)
![LaTeX](https://img.shields.io/badge/LaTeX-Project-008080?style=for-the-badge&logo=latex&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

**Mini Research Project — MAL6050 (Partial Differential Equations)**
**M.Sc. Mathematics | IIT Jodhpur**
**Author:** [Souvik Ghorui](https://github.com/souvikghorui) (M25MA2008)

---

## 📌 Overview

This repository hosts a comprehensive study of **Energy Methods** as a powerful analytical tool for proving the uniqueness of solutions to **Initial Boundary Value Problems (IBVPs)**. This project bridges classical PDE theory with modern visualization, featuring rigorous proofs, interactive simulations, and a cinematic animated presentation.

The central theme is the construction of an **Energy Functional** $E(t)$ for the difference of two hypothetical solutions. By demonstrating that $E(t) \equiv 0$ through physical conservation laws or dissipation arguments, we establish uniqueness without needing the explicit form of the solution.

---

## 🚀 Key Features

- 📄 **Rigorous Research Report:** A self-contained study covering Heat, Wave, Damped Wave, and Reaction-Diffusion equations.
- 🎬 **Animated Presentation:** A 14-slide interactive deck built with [Manim Slides](https://manim-slides.eertmans.be/), featuring 3Blue1Brown-style animations.
- 🌐 **Interactive Web Simulations:** Standalone HTML/JS simulations for Damped Wave and Reaction-Diffusion dynamics.
- 📐 **Mathematical Depth:** Detailed derivations using $L^2$ norms, integration by parts, and Gronwall's Inequality.

---

## 📂 Repository Structure

```text
.
├── Energy_method_mini_research.tex  # LaTeX source for the research report
├── Energy_method_mini_research.pdf  # Compiled research report (PDF)
├── damped-wave.html                 # Web simulation: Damped Wave Equation
├── reaction_diffusion.html          # Web simulation: Reaction-Diffusion Model
├── PDE Presentation/                # Manim Slides Presentation
│   ├── energy_method_slides.py      # Manim source code
│   ├── generate_slides.bat          # Build script (Windows)
│   ├── present.bat                  # Presentation launcher (Windows)
│   └── Static_Slides/               # PNG exports of the presentation
├── LICENSE                          # MIT License
└── README.md                        # Project documentation
```

---

## 🧠 Mathematical Highlights

### The Energy Method Core
For a difference function $w = u_1 - u_2$, we define a non-negative energy functional $E(t)$. The goal is to show:
$$\frac{dE}{dt} \leq 0 \quad \text{and} \quad E(0) = 0 \implies E(t) = 0 \quad \forall t \geq 0$$

### Equations Covered
| Equation | Type | Energy Functional $E(t)$ |
| :--- | :--- | :--- |
| **Heat Equation** | Parabolic | $\frac{1}{2} \int \omega^2 \, dx$ |
| **Wave Equation** | Hyperbolic | $\frac{1}{2} \int (\omega_t^2 + c^2 \omega_x^2) \, dx$ |
| **Damped Wave** | Hyperbolic | $\frac{1}{2} \int (\omega_t^2 + c^2 \omega_x^2) \, dx$ (with decay) |
| **Reaction-Diffusion**| Non-linear | Modified $L^2$ with Gronwall analysis |

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.8+**
- **FFmpeg** (required for Manim)
- **LaTeX Distribution** (e.g., MiKTeX or TeX Live)

### Environment Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/souvikghorui/Energy-Method-Mini-Project.git
   cd Energy-Method-Mini-Project
   ```
2. Install Python dependencies:
   ```bash
   pip install manim manim-slides
   ```

---

## 💻 Usage

### 1. Run the Presentation
The presentation is interactive. Press `SPACE` to advance animations.
- **Windows:** Run `present.bat` in the `PDE Presentation/` folder.
- **CLI:**
  ```bash
  cd "PDE Presentation"
  manim-slides present EnergyMethodSlides
  ```

### 2. View Interactive Simulations
Simply open the `.html` files in any modern web browser:
- `damped-wave.html`: Visualize thermal-like dissipation in wave motion.
- `reaction_diffusion.html`: Explore Turing pattern formation and stability.

### 3. Compile Research Report
To modify or rebuild the research paper:
```bash
pdflatex Energy_method_mini_research.tex
```

---

## 📚 References
- **Strauss, W. A.** — *Partial Differential Equations: An Introduction*
- **Evans, L. C.** — *Partial Differential Equations* (AMS Graduate Studies)
- **Hadamard, J.** — *Lectures on Cauchy's Problem in Linear Partial Differential Equations*

---

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
<p align="center">
  Developed with ❤️ for MAL6050 @ <b>IIT Jodhpur</b>
</p>
