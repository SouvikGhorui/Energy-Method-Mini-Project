"""
Energy Methods and Uniqueness of IBVPs
Manim Slides Presentation — Souvik Ghorui (M25MA2008)

Run with:
    generate_slides.bat (to build the slides)
    present.bat         (to show the presentation)
"""

from manim import *
from manim import ManimColor
from manim_slides import Slide
import numpy as np


# ── Colour palette (3Blue1Brown-inspired pastels on dark) ─────────────────────
BG       = "#1B1B2F"
C_BLUE   = "#58C4DD"
C_GREEN  = "#83C167"
C_RED    = "#FF6B6B"
C_YELLOW = "#FFFF00"
C_ORANGE = "#FF8C00"
C_TEAL   = "#5CE1E6"
C_PINK   = "#E07CDA"
C_GRAY   = "#888888"
C_WHITE  = "#ECF0F1"
C_DGRAY  = "#444444"


class EnergyMethodPresentation(Slide):
    """Cinematic research presentation on the energy method for IBVPs."""

    def clear(self):
        mobs = [m for m in self.mobjects if not isinstance(m, (Camera,))]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.6)

    def section_header(self, text, color=C_BLUE):
        t = Text(text, font_size=36, weight=BOLD, color=color)
        line = Line(6.5 * LEFT, 6.5 * RIGHT, color=color, stroke_width=1.5)
        line.next_to(t, DOWN, buff=0.1)
        g = VGroup(t, line).to_corner(UL, buff=0.45)
        return g

    def boxed(self, mob, color=C_GREEN, buff=0.18):
        return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12)

    def construct(self):
        self.camera.background_color = ManimColor(BG)
        self.slide_01_title()
        self.slide_02_motivation()
        self.slide_03_hadamard()
        self.slide_04_energy_functional()
        self.slide_05_difference_proof()
        self.slide_06_heat_equation()
        self.slide_07_thermal_dissipation()
        self.slide_08_wave_equation()
        self.slide_09_reaction_diffusion()
        self.slide_09b_reaction_diffusion_example()
        self.slide_10_damped_wave()
        self.slide_11_comparison_plot()
        self.slide_12_discussion()
        self.slide_13_conclusion()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 1 — Title Card (everything appears at once)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_01_title(self):
        heat_waves = VGroup()
        for i in range(6):
            freq = 0.5 + i * 0.3
            phase = i * 0.7
            wave = FunctionGraph(
                lambda x, f=freq, p=phase: 0.15 * np.sin(f * x + p),
                x_range=[-7.5, 7.5, 0.05],
                color=C_ORANGE, stroke_width=1.0,
                stroke_opacity=0.08 + i * 0.02,
            ).shift(UP * (2.5 - i * 1.0))
            heat_waves.add(wave)

        title_main = Text("Energy Method and its Application", font_size=42, weight=BOLD, color=C_BLUE)
        title_sub = Text("in Uniqueness of the Solution of Initial Boundary Value Problems", font_size=24, color=C_TEAL)
        divider = Line(5.0 * LEFT, 5.0 * RIGHT, color=C_GRAY, stroke_width=1.5)
        author = Text("Souvik Ghorui  |  IIT Jodhpur", font_size=26, color=C_GRAY)
        course = Text("Partial Differential Equations  ·  M.Sc.–M.Tech", font_size=20, color=C_DGRAY)
        title_group = VGroup(title_main, title_sub, divider, author, course).arrange(DOWN, buff=0.3)

        # Everything appears together
        self.play(
            *[Create(w) for w in heat_waves],
            Write(title_main), FadeIn(title_sub),
            Create(divider), FadeIn(author), FadeIn(course),
            run_time=2.0,
        )
        self.next_slide()  # PAUSE — presenter introduces themselves
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 2 — Motivation: Physical Reality → Mathematical Model
    # ══════════════════════════════════════════════════════════════════════════
    def slide_02_motivation(self):
        hdr = self.section_header("Why Energy Methods?")
        self.play(Write(hdr))

        # --- Physical Reality: a rod with heat gradient ---
        phys_label = Text("Physical Reality", font_size=26, weight=BOLD, color=C_ORANGE)
        rod = RoundedRectangle(width=5.0, height=0.7, corner_radius=0.15,
                               color=C_ORANGE, fill_opacity=0.0, stroke_width=2.5)
        grad_rects = VGroup()
        n_segs = 20
        seg_w = 4.8 / n_segs
        for i in range(n_segs):
            t = i / (n_segs - 1)
            r_val = int(255 * (1 - t))
            b_val = int(100 + 155 * t)
            col = f"#{r_val:02x}4040" if t < 0.5 else f"#4040{b_val:02x}"
            rect = Rectangle(width=seg_w, height=0.5, fill_color=col, fill_opacity=0.6, stroke_width=0)
            rect.move_to(rod.get_left() + RIGHT * (0.1 + seg_w / 2 + i * seg_w))
            grad_rects.add(rect)
        hot_lbl = Text("Hot", font_size=18, color=C_RED).next_to(rod, LEFT, buff=0.15)
        cold_lbl = Text("Cold", font_size=18, color=C_BLUE).next_to(rod, RIGHT, buff=0.15)
        temp_label = MathTex(r"u(x,t)", font_size=24, color=C_WHITE).next_to(rod, UP, buff=0.15)
        phys_group = VGroup(phys_label, rod, grad_rects, hot_lbl, cold_lbl, temp_label)
        phys_label.next_to(rod, UP, buff=0.6)
        temp_label.next_to(rod, UP, buff=0.1)
        phys_group.shift(LEFT * 3 + DOWN * 0.5)

        self.play(Create(rod), FadeIn(grad_rects), run_time=1.0)
        self.play(FadeIn(hot_lbl), FadeIn(cold_lbl), FadeIn(phys_label), FadeIn(temp_label))
        self.next_slide()  # PAUSE — explain the physical rod

        # --- Arrow + Mathematical Model ---
        math_label = Text("Mathematical Model", font_size=26, weight=BOLD, color=C_BLUE)
        pde_eq = MathTex(r"u_t = k\,u_{xx}", font_size=36, color=C_BLUE)
        ic_eq = MathTex(r"u(x,0) = \varphi(x)", font_size=28, color=C_GREEN)
        bc_eq = MathTex(r"u(0,t) = u(L,t) = 0", font_size=28, color=C_YELLOW)
        math_group = VGroup(math_label, pde_eq, ic_eq, bc_eq).arrange(DOWN, buff=0.3)
        math_group.shift(RIGHT * 3 + DOWN * 0.5)

        arrow = Arrow(phys_group.get_right() + RIGHT * 0.2,
                       math_group.get_left() + LEFT * 0.2,
                       color=C_WHITE, buff=0.15, stroke_width=3)
        arrow_label = Text("Model", font_size=18, color=C_GRAY).next_to(arrow, UP, buff=0.08)

        self.play(GrowArrow(arrow), FadeIn(arrow_label))
        self.play(Write(math_label))
        self.play(Write(pde_eq), run_time=0.8)
        self.play(FadeIn(ic_eq, shift=RIGHT * 0.2), FadeIn(bc_eq, shift=RIGHT * 0.2))
        self.next_slide()  # PAUSE — explain the PDE model

        # --- Question ---
        question = Text("Does this PDE have a unique solution?",
                        font_size=28, weight=BOLD, color=C_YELLOW).to_edge(DOWN, buff=0.6)
        self.play(Write(question))
        self.next_slide()  # PAUSE — let the question sink in
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 3 — Hadamard's Trinity
    # ══════════════════════════════════════════════════════════════════════════
    def slide_03_hadamard(self):
        hdr = self.section_header("Hadamard's Well-Posedness  (1902)")
        self.play(Write(hdr))

        def make_orb(label_text, color, pos):
            circle = Circle(radius=0.8, color=color, fill_color=color, fill_opacity=0.15, stroke_width=2.5)
            glow = Circle(radius=1.05, color=color, fill_opacity=0.05, stroke_width=0.5)
            label = Text(label_text, font_size=22, weight=BOLD, color=color)
            label.move_to(circle.get_center())
            return VGroup(glow, circle, label).move_to(pos)

        orb_exist  = make_orb("Existence",  C_GRAY,  LEFT * 4 + DOWN * 0.5)
        orb_unique = make_orb("Uniqueness", C_GREEN, ORIGIN + DOWN * 0.5)
        orb_stab   = make_orb("Stability",  C_GRAY,  RIGHT * 4 + DOWN * 0.5)

        for orb in [orb_exist, orb_unique, orb_stab]:
            self.play(FadeIn(orb, scale=0.5), run_time=0.7)
        self.next_slide()  # PAUSE — explain three conditions

        # Uniqueness orb grows
        self.play(
            orb_exist.animate.set_opacity(0.25).scale(0.7),
            orb_stab.animate.set_opacity(0.25).scale(0.7),
            orb_unique[1].animate.set(fill_opacity=0.3, stroke_width=4),
            orb_unique.animate.scale(1.8).move_to(DOWN * 0.3),
            run_time=1.2,
        )
        focus_text = Text("Energy method targets this!", font_size=26, color=C_GREEN)
        focus_text.next_to(orb_unique, DOWN, buff=0.5)
        self.play(Write(focus_text))
        self.next_slide()  # PAUSE — explain why uniqueness matters
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 4 — The Energy Functional E(t)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_04_energy_functional(self):
        hdr = self.section_header("The Energy Functional  E(t)")
        self.play(Write(hdr))

        energy_def = MathTex(r"E(t) = \frac{1}{2} \int_0^L u^2 \, dx",
                             font_size=42, color=C_YELLOW).next_to(hdr, DOWN, buff=0.7)
        self.play(Write(energy_def), run_time=1.0)
        self.next_slide()  # PAUSE — explain the definition

        # Axes + u(x) curve
        ax = Axes(x_range=[0, PI, PI/4], y_range=[-0.2, 1.3, 0.5],
                  x_length=5.5, y_length=3.0,
                  axis_config={"color": C_GRAY, "include_tip": False}).shift(DOWN*1.5 + LEFT*0.5)
        ax_labels = ax.get_axis_labels(
            x_label=MathTex("x", font_size=22, color=C_GRAY),
            y_label=MathTex("", font_size=22))

        u_curve = ax.plot(lambda x: np.sin(x), color=C_BLUE, stroke_width=3)
        u_label = MathTex(r"u(x)", font_size=22, color=C_BLUE).next_to(
            ax.c2p(PI*0.35, np.sin(PI*0.35)), UP, buff=0.1)

        self.play(Create(ax), Write(ax_labels))
        self.play(Create(u_curve), FadeIn(u_label))
        self.next_slide()  # PAUSE — explain the wave u(x)

        # Transform to u^2(x) with shaded area
        u2_curve = ax.plot(lambda x: np.sin(x)**2, color=C_GREEN, stroke_width=3)
        u2_label = MathTex(r"u^2(x)", font_size=22, color=C_GREEN).next_to(
            ax.c2p(PI*0.35, np.sin(PI*0.35)**2), UP, buff=0.1)
        area = ax.get_area(u2_curve, x_range=[0, PI], color=C_GREEN, opacity=0.25)

        self.play(ReplacementTransform(u_curve, u2_curve),
                  ReplacementTransform(u_label, u2_label), run_time=1.0)
        self.play(FadeIn(area), run_time=0.7)
        area_label = MathTex(r"E(t) = \tfrac{1}{2}\int u^2\,dx",
                             font_size=22, color=C_GREEN).next_to(ax, RIGHT, buff=0.5)
        self.play(Write(area_label))
        self.next_slide()  # PAUSE — explain squaring and area

        # Key property
        key = MathTex(r"E(t) \geq 0, \qquad E(t)=0 \;\Leftrightarrow\; u \equiv 0",
                      font_size=30, color=C_YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(key), Create(self.boxed(key, color=C_YELLOW)))
        self.next_slide()  # PAUSE — explain the key property
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 5 — The "Difference" Proof
    # ══════════════════════════════════════════════════════════════════════════
    def slide_05_difference_proof(self):
        hdr = self.section_header("The Uniqueness Proof Strategy")
        self.play(Write(hdr))

        ax = Axes(x_range=[0, PI, PI/4], y_range=[-0.3, 1.5, 0.5],
                  x_length=6, y_length=3.0,
                  axis_config={"color": C_GRAY, "include_tip": False}).shift(DOWN*0.3)
        self.play(Create(ax), run_time=0.6)

        # Two solutions
        u1_curve = ax.plot(lambda x: np.sin(x) + 0.15, color=C_BLUE, stroke_width=3)
        u1_lbl = MathTex(r"u_1", font_size=24, color=C_BLUE).next_to(
            ax.c2p(PI*0.3, np.sin(PI*0.3)+0.15), UP, buff=0.15)
        u2_curve = ax.plot(lambda x: np.sin(x) - 0.15, color=C_PINK, stroke_width=3)
        u2_lbl = MathTex(r"u_2", font_size=24, color=C_PINK).next_to(
            ax.c2p(PI*0.3, np.sin(PI*0.3)-0.15), DOWN, buff=0.15)

        self.play(Create(u1_curve), FadeIn(u1_lbl), run_time=0.7)
        self.play(Create(u2_curve), FadeIn(u2_lbl), run_time=0.7)
        self.next_slide()  # PAUSE — explain two solutions u1, u2

        # Merge into w
        w_curve = ax.plot(lambda x: 0.3*np.sin(x), color=C_YELLOW, stroke_width=3)
        w_lbl = MathTex(r"w = u_1 - u_2", font_size=24, color=C_YELLOW).next_to(
            ax.c2p(PI*0.4, 0.3*np.sin(PI*0.4)), UP, buff=0.2)
        self.play(ReplacementTransform(u1_curve, w_curve), FadeOut(u2_curve),
                  ReplacementTransform(u1_lbl, w_lbl), FadeOut(u2_lbl), run_time=1.2)
        self.next_slide()  # PAUSE — explain the difference w

        # Facts
        facts = VGroup(
            MathTex(r"w \text{ solves homogeneous IBVP}", font_size=26, color=C_WHITE),
            MathTex(r"w(x,0) = 0 \;\Rightarrow\; E_w(0) = 0", font_size=26, color=C_GREEN),
            MathTex(r"E_w'(t) \leq 0 \;\Rightarrow\; E_w(t) = 0 \;\Rightarrow\; w \equiv 0",
                    font_size=26, color=C_GREEN),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.4)
        for f in facts:
            self.play(FadeIn(f, shift=RIGHT*0.2), run_time=0.6)
        self.next_slide()  # PAUSE — explain the logic chain

        # Collapse to zero
        zero_curve = ax.plot(lambda x: 0, color=C_GREEN, stroke_width=2)
        self.play(ReplacementTransform(w_curve, zero_curve), run_time=1.0)
        conclusion = MathTex(r"\therefore\; u_1 = u_2 \quad \checkmark",
                             font_size=36, color=C_GREEN).next_to(facts, RIGHT, buff=0.5)
        self.play(Write(conclusion), Create(self.boxed(conclusion, color=C_GREEN)))
        self.next_slide()  # PAUSE — celebrate uniqueness result
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 6 — Heat Equation (Split Screen)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_06_heat_equation(self):
        hdr = self.section_header("Application 1: Heat Equation")
        self.play(Write(hdr))

        divider = DashedLine(UP*2.8, DOWN*3.5, color=C_GRAY, dash_length=0.15, stroke_width=1.5)

        # LEFT: PDE setup
        left_title = Text("The PDE", font_size=24, weight=BOLD, color=C_RED)
        pde = MathTex(r"u_t = k\,u_{xx}", font_size=36, color=C_RED)
        bcs = MathTex(r"u(0,t) = u(L,t) = 0", font_size=26, color=C_WHITE)
        step1 = Text("Multiply by u, integrate:", font_size=20, color=C_GRAY)
        derive1 = MathTex(r"E'(t) = \int_0^L u \cdot u_t\,dx", font_size=26, color=C_WHITE)
        derive2 = MathTex(r"= \int_0^L u \cdot k\,u_{xx}\,dx", font_size=26, color=C_WHITE)
        derive3 = MathTex(r"\xrightarrow{\text{IBP}}\; -k\|u_x\|^2", font_size=26, color=C_WHITE)
        left_group = VGroup(left_title, pde, bcs, step1, derive1, derive2, derive3).arrange(
            DOWN, buff=0.25, aligned_edge=LEFT).shift(LEFT*3.5 + DOWN*0.3)

        # RIGHT: Energy identity
        right_title = Text("Energy Identity", font_size=24, weight=BOLD, color=C_GREEN)
        result = MathTex(r"E'(t) = -k\|u_x\|^2 \leq 0", font_size=34, color=C_GREEN)
        note1 = MathTex(r"-k\|u_x\|^2 \leq 0", font_size=26, color=C_YELLOW)
        note1_text = Text("Diffusion always dissipates", font_size=20, color=C_GRAY)
        implication = MathTex(r"\Rightarrow\; E(t) \leq E(0)", font_size=30, color=C_BLUE)
        uniqueness = MathTex(r"E_w(0) = 0 \;\Rightarrow\; E_w(t) = 0", font_size=28, color=C_GREEN)
        uniqueness_label = Text("⇒ Uniqueness ✓", font_size=22, weight=BOLD, color=C_GREEN)
        right_group = VGroup(right_title, result, note1, note1_text, implication,
                             uniqueness, uniqueness_label).arrange(
            DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT*2.5 + DOWN*0.3)

        self.play(Create(divider))
        self.play(FadeIn(left_title), Write(pde), run_time=0.8)
        self.play(FadeIn(bcs))
        self.next_slide()  # PAUSE — explain the PDE setup

        self.play(FadeIn(step1))
        for eq in [derive1, derive2, derive3]:
            self.play(Write(eq), run_time=0.6)
        self.next_slide()  # PAUSE — explain the derivation steps

        self.play(FadeIn(right_title))
        self.play(Write(result), Create(self.boxed(result, color=C_GREEN)))
        self.next_slide()  # PAUSE — explain the energy identity

        self.play(FadeIn(note1), FadeIn(note1_text))
        self.play(Write(implication))
        self.play(FadeIn(uniqueness), FadeIn(uniqueness_label))
        self.next_slide()  # PAUSE — explain uniqueness conclusion
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 7 — Thermal Dissipation Visualization
    # ══════════════════════════════════════════════════════════════════════════
    def slide_07_thermal_dissipation(self):
        hdr = self.section_header("Visualization: Thermal Dissipation")
        self.play(Write(hdr))

        ax_heat = Axes(x_range=[0, PI, PI/4], y_range=[-0.1, 1.2, 0.5],
                       x_length=5.0, y_length=3.0,
                       axis_config={"color": C_GRAY, "include_tip": False}).shift(LEFT*3 + DOWN*0.8)
        heat_label = Text("Temperature profile u(x,t)", font_size=20, color=C_GRAY).next_to(ax_heat, UP, buff=0.15)

        self.play(Create(ax_heat), FadeIn(heat_label))

        times_data = [0.0, 0.3, 0.8, 1.5, 3.0]
        colors_heat = [C_RED, C_ORANGE, C_YELLOW, C_GREEN, C_BLUE]
        decay_rate = 1.5

        curves = VGroup()
        for i, (t_val, col) in enumerate(zip(times_data, colors_heat)):
            amp = np.exp(-decay_rate * t_val)
            curve = ax_heat.plot(lambda x, a=amp: a*np.sin(x), color=col, stroke_width=2.5)
            lbl = MathTex(f"t={t_val:.1f}", font_size=16, color=col).next_to(
                ax_heat.c2p(PI*0.5, amp*np.sin(PI*0.5)), RIGHT, buff=0.15)
            curves.add(VGroup(curve, lbl))

        for c in curves:
            self.play(Create(c[0]), FadeIn(c[1]), run_time=0.5)
        self.next_slide()  # PAUSE — explain the cooling snapshots

        # Decay curve
        ax_e = Axes(x_range=[0, 4, 1], y_range=[0, 1.15, 0.5],
                    x_length=4.5, y_length=3.0,
                    axis_config={"color": C_GRAY, "include_tip": False},
                    x_axis_config={"numbers_to_include": [1, 2, 3]},
                    y_axis_config={"numbers_to_include": [0.5, 1.0]}).shift(RIGHT*3 + DOWN*0.8)
        ax_e_labels = ax_e.get_axis_labels(
            x_label=MathTex("t", font_size=22, color=C_GRAY),
            y_label=MathTex("E(t)", font_size=22, color=C_GRAY))

        decay_curve = ax_e.plot(lambda t: np.exp(-decay_rate*t), color=C_GREEN, stroke_width=3)
        decay_label = MathTex(r"E(0)\,e^{-2k\pi^2 t/L^2}", font_size=20, color=C_GREEN).next_to(
            ax_e.c2p(4*0.15, np.exp(-decay_rate*4*0.15)), UR, buff=0.1)

        self.play(Create(ax_e), Write(ax_e_labels))
        self.play(Create(decay_curve), FadeIn(decay_label), run_time=1.0)
        self.next_slide()  # PAUSE — explain exponential decay curve

        poincare_box = MathTex(r"\text{Poincar\'{e}: } \|u_x\|^2 \geq \frac{\pi^2}{L^2}\|u\|^2",
                               font_size=22, color=C_YELLOW).to_edge(DOWN, buff=0.4)
        self.play(Write(poincare_box))
        self.next_slide()  # PAUSE — explain Poincaré inequality
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 8 — Wave Equation
    # ══════════════════════════════════════════════════════════════════════════
    def slide_08_wave_equation(self):
        hdr = self.section_header("Application 2: Wave Equation")
        self.play(Write(hdr))

        pde = MathTex(r"u_{tt} = c^2 u_{xx}", font_size=36, color=C_BLUE)
        energy = MathTex(r"E(t) = \frac{1}{2}\int_0^L \!\bigl(u_t^2 + c^2 u_x^2\bigr)\,dx",
                         font_size=30, color=C_YELLOW)
        conservation = MathTex(r"E'(t) = 0 \;\Rightarrow\; E(t) = E(0) \quad \text{(conserved!)}",
                               font_size=30, color=C_GREEN)
        eqs = VGroup(pde, energy, conservation).arrange(DOWN, buff=0.3).next_to(hdr, DOWN, buff=0.5)

        self.play(Write(pde))
        self.next_slide()  # PAUSE — intro wave PDE

        self.play(Write(energy))
        self.next_slide()  # PAUSE — explain KE + PE energy

        # Vibrating string
        ax_w = Axes(x_range=[0, PI, PI/4], y_range=[-1.2, 1.2, 0.5],
                    x_length=5.5, y_length=2.5,
                    axis_config={"color": C_GRAY, "include_tip": False}).shift(LEFT*2.5 + DOWN*2.0)
        self.play(Create(ax_w), run_time=0.5)

        # Animate vibrating string smoothly
        wave_time = ValueTracker(0)
        
        string = ax_w.plot(lambda x: np.sin(x) * np.cos(wave_time.get_value() * 3), 
                           color=C_TEAL, stroke_width=3.5)
        
        string.add_updater(
            lambda m: m.become(
                ax_w.plot(lambda x: np.sin(x) * np.cos(wave_time.get_value() * 3), 
                          color=C_TEAL, stroke_width=3.5)
            )
        )
        
        self.add(string)
        self.play(wave_time.animate.set_value(2 * PI), run_time=3.5, rate_func=linear)
        string.suspend_updating()

        self.next_slide()  # PAUSE — explain vibrating string

        # KE/PE bar chart
        bar_base = RIGHT*3.5 + DOWN*2.0
        bar_height = 1.8
        bar_width = 0.7
        ke_val, pe_val = 0.3, 0.7

        ke_bar = Rectangle(width=bar_width, height=bar_height*ke_val, color=C_RED,
                           fill_color=C_RED, fill_opacity=0.5, stroke_width=2
                           ).move_to(bar_base + LEFT*0.6 + UP*bar_height*ke_val/2)
        ke_lbl = Text("KE", font_size=18, weight=BOLD, color=C_RED).next_to(ke_bar, DOWN, buff=0.1)
        pe_bar = Rectangle(width=bar_width, height=bar_height*pe_val, color=C_BLUE,
                           fill_color=C_BLUE, fill_opacity=0.5, stroke_width=2
                           ).move_to(bar_base + RIGHT*0.6 + UP*bar_height*pe_val/2)
        pe_lbl = Text("PE", font_size=18, weight=BOLD, color=C_BLUE).next_to(pe_bar, DOWN, buff=0.1)
        total_line = DashedLine(bar_base + LEFT*1.5 + UP*bar_height*(ke_val+pe_val)/2,
                                bar_base + RIGHT*1.5 + UP*bar_height*(ke_val+pe_val)/2,
                                color=C_GREEN, dash_length=0.1, stroke_width=2)
        total_lbl = Text("Total E", font_size=16, color=C_GREEN).next_to(total_line, RIGHT, buff=0.1)

        self.play(Create(ke_bar), Create(pe_bar), FadeIn(ke_lbl), FadeIn(pe_lbl))
        self.play(Create(total_line), FadeIn(total_lbl))
        self.next_slide()  # PAUSE — explain KE/PE bars

        # Swap bars
        ke_bar2 = Rectangle(width=bar_width, height=bar_height*pe_val, color=C_RED,
                            fill_color=C_RED, fill_opacity=0.5, stroke_width=2
                            ).move_to(bar_base + LEFT*0.6 + UP*bar_height*pe_val/2)
        pe_bar2 = Rectangle(width=bar_width, height=bar_height*ke_val, color=C_BLUE,
                            fill_color=C_BLUE, fill_opacity=0.5, stroke_width=2
                            ).move_to(bar_base + RIGHT*0.6 + UP*bar_height*ke_val/2)
        self.play(ReplacementTransform(ke_bar, ke_bar2),
                  ReplacementTransform(pe_bar, pe_bar2), run_time=1.0)
        self.play(Write(conservation), Create(self.boxed(conservation, color=C_GREEN)))
        self.next_slide()  # PAUSE — explain conservation
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 9 — Reaction-Diffusion (Tipping Point)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_09_reaction_diffusion(self):
        hdr = self.section_header("Reaction-Diffusion: Tipping Point")
        self.play(Write(hdr))

        pde = MathTex(r"u_t = k\,u_{xx} + r\,u", font_size=36, color=C_ORANGE).next_to(hdr, DOWN, buff=0.55)
        self.play(Write(pde))
        self.next_slide()  # PAUSE — introduce the PDE

        r_crit_eq = MathTex(r"r_{\text{crit}} = k\left(\frac{\pi}{L}\right)^2",
                            font_size=34, color=C_YELLOW).next_to(pde, DOWN, buff=0.4)
        self.play(Write(r_crit_eq))
        self.next_slide()  # PAUSE — explain critical threshold

        # LEFT: Decay
        ax_decay = Axes(x_range=[0, PI, PI/2], y_range=[-0.1, 1.2, 0.5],
                        x_length=4.5, y_length=2.5,
                        axis_config={"color": C_GRAY, "include_tip": False}).shift(LEFT*3.5 + DOWN*1.8)
        decay_title = Text("Decay: Diffusion Wins", font_size=20, weight=BOLD, color=C_BLUE).next_to(ax_decay, UP, buff=0.15)
        decay_sub = MathTex(r"r < r_{\text{crit}}", font_size=22, color=C_BLUE).next_to(decay_title, DOWN, buff=0.08)

        decay_curves = VGroup()
        for i, t_val in enumerate([0.0, 0.5, 1.0, 2.0]):
            amp = np.exp(-0.8*t_val)
            c = ax_decay.plot(lambda x, a=amp: a*np.sin(x), color=C_BLUE,
                              stroke_width=2.5, stroke_opacity=1.0-0.2*i)
            decay_curves.add(c)

        self.play(Create(ax_decay), FadeIn(decay_title), FadeIn(decay_sub))
        for c in decay_curves:
            self.play(Create(c), run_time=0.35)
        self.next_slide()  # PAUSE — explain decay scenario

        # RIGHT: Growth
        ax_grow = Axes(x_range=[0, PI, PI/2], y_range=[-0.1, 3.5, 1.0],
                       x_length=4.5, y_length=2.5,
                       axis_config={"color": C_GRAY, "include_tip": False}).shift(RIGHT*3.5 + DOWN*1.8)
        grow_title = Text("Growth: Reaction Wins", font_size=20, weight=BOLD, color=C_RED).next_to(ax_grow, UP, buff=0.15)
        grow_sub = MathTex(r"r > r_{\text{crit}}", font_size=22, color=C_RED).next_to(grow_title, DOWN, buff=0.08)

        grow_curves = VGroup()
        for i, t_val in enumerate([0.0, 0.3, 0.6, 0.9]):
            amp = np.exp(1.2*t_val)
            c = ax_grow.plot(lambda x, a=amp: a*np.sin(x), color=C_RED,
                             stroke_width=2.5, stroke_opacity=0.4+0.2*i)
            grow_curves.add(c)

        self.play(Create(ax_grow), FadeIn(grow_title), FadeIn(grow_sub))
        for c in grow_curves:
            self.play(Create(c), run_time=0.35)
        self.next_slide()  # PAUSE — explain growth scenario

        div_line = DashedLine(r_crit_eq.get_bottom()+DOWN*0.3, DOWN*3.5,
                              color=C_GRAY, dash_length=0.12, stroke_width=1.5)
        self.play(Create(div_line))
        energy_note = MathTex(r"E'(t) = (-k\pi^2/L^2 + r)\,E(t)",
                              font_size=24, color=C_WHITE).to_edge(DOWN, buff=0.35)
        self.play(Write(energy_note))
        self.next_slide()  # PAUSE — explain the energy formula
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 09b — Reaction-Diffusion Example 1 
    # ══════════════════════════════════════════════════════════════════════════
    def slide_09b_reaction_diffusion_example(self):
        hdr = self.section_header("Example 1: Heat Eq. with Reaction Term")
        self.play(Write(hdr))

        # Problem statement box
        pde_group = VGroup(
            MathTex(r"u_t = u_{xx} + u", font_size=34, color=C_BLUE),
            MathTex(r"x \in (0, \pi), \quad t > 0", font_size=26, color=C_WHITE),
            MathTex(r"u(x,0) = \sin x", font_size=28, color=C_GREEN),
            MathTex(r"u(0,t) = 0, \quad u(\pi,t) = 0", font_size=28, color=C_YELLOW)
        ).arrange(DOWN, buff=0.2).next_to(hdr, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        
        prob_box = self.boxed(pde_group, color=C_GRAY, buff=0.2)
        
        self.play(Create(prob_box), Write(pde_group))
        self.next_slide()

        # Part (a): Energy Equation
        part_a_title = Text("(a) Energy equation", font_size=24, weight=BOLD, color=C_WHITE)
        e_deriv = MathTex(r"E'(t) =", r"-\|u_x\|^2", r"+", r"\|u\|^2", font_size=30, color=C_TEAL)
        e_deriv.set_color_by_tex(r"-\|u_x\|^2", C_RED)
        e_deriv.set_color_by_tex(r"\|u\|^2", C_GREEN)
        
        part_a = VGroup(part_a_title, e_deriv).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        part_a.next_to(prob_box, DOWN, buff=0.5).align_to(prob_box, LEFT)

        self.play(FadeIn(part_a_title))
        self.play(Write(e_deriv))
        self.next_slide()

        # Part (b): Growth or Decay
        part_b_title = Text("(b) Growth or decay?", font_size=24, weight=BOLD, color=C_WHITE)
        poincare = MathTex(r"\text{Poincar\'{e} (}L=\pi\text{): } \|u_x\|^2 \geq \frac{\pi^2}{\pi^2}\|u\|^2 = \|u\|^2", font_size=26, color=C_YELLOW)
        e_bound = MathTex(r"\Rightarrow \quad E'(t) \leq -\|u\|^2 + \|u\|^2 = 0", font_size=28, color=C_GREEN)
        e_bound_text = Text("Energy is non-increasing!", font_size=20, color=C_GREEN)
        part_b = VGroup(part_b_title, poincare, e_bound, e_bound_text).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        part_b.next_to(prob_box, RIGHT, buff=1.0).align_to(prob_box, UP)

        self.play(FadeIn(part_b_title))
        self.play(Write(poincare))
        self.play(Write(e_bound), FadeIn(e_bound_text))
        self.next_slide()

        # Part (c): Uniqueness
        part_c_title = Text("(c) Uniqueness", font_size=24, weight=BOLD, color=C_WHITE)
        w_eq = MathTex(r"\text{Let } w = u_1 - u_2 \Rightarrow E_w'(t) \leq 0", font_size=26, color=C_GRAY)
        w_zero = MathTex(r"E_w(0) = 0 \Rightarrow E_w(t) = 0 \Rightarrow w \equiv 0", font_size=26, color=C_BLUE)
        part_c = VGroup(part_c_title, w_eq, w_zero).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        part_c.next_to(part_b, DOWN, buff=0.6).align_to(part_b, LEFT)

        self.play(FadeIn(part_c_title))
        self.play(Write(w_eq))
        self.play(Write(w_zero))
        
        uniq_check = Text("Uniqueness follows ✓", font_size=24, weight=BOLD, color=C_GREEN).next_to(part_c, DOWN, buff=0.3)
        self.play(FadeIn(uniq_check))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 10 — Damped Wave
    # ══════════════════════════════════════════════════════════════════════════
    def slide_10_damped_wave(self):
        hdr = self.section_header("Damped Wave: Dissipation")
        self.play(Write(hdr))

        pde = MathTex(r"u_{tt} + 2\gamma\,u_t = c^2\,u_{xx}, \quad \gamma > 0",
                      font_size=34, color=C_ORANGE).next_to(hdr, DOWN, buff=0.5)
        self.play(Write(pde))
        self.next_slide()  # PAUSE — introduce damped wave PDE

        ax_d = Axes(x_range=[0, PI, PI/4], y_range=[-1.3, 1.3, 0.5],
                    x_length=8, y_length=3.5,
                    axis_config={"color": C_GRAY, "include_tip": False}).shift(DOWN*1.2)
        ax_d_labels = ax_d.get_axis_labels(
            x_label=MathTex("x", font_size=22, color=C_GRAY),
            y_label=MathTex("u", font_size=22, color=C_GRAY))

        gamma_val = 0.2
        omega = 4.0
        
        time_t = ValueTracker(0)

        string = ax_d.plot(lambda x: np.sin(x), color=C_TEAL, stroke_width=3.5)
        env_upper = ax_d.plot(lambda x: np.sin(x), color=C_ORANGE, stroke_width=2, stroke_opacity=0.6)
        env_lower = ax_d.plot(lambda x: -np.sin(x), color=C_ORANGE, stroke_width=2, stroke_opacity=0.6)

        env_label = MathTex(r"Ae^{-\gamma t}\sin(x)", font_size=22, color=C_ORANGE).next_to(
            ax_d.c2p(PI*0.5, 1.0), UP, buff=0.2)

        string.add_updater(lambda m: m.become(ax_d.plot(
            lambda x: np.exp(-gamma_val * time_t.get_value()) * np.sin(x) * np.cos(omega * time_t.get_value()),
            color=C_TEAL, stroke_width=3.5
        )))
        env_upper.add_updater(lambda m: m.become(ax_d.plot(
            lambda x: np.exp(-gamma_val * time_t.get_value()) * np.sin(x),
            color=C_ORANGE, stroke_width=2, stroke_opacity=0.6
        )))
        env_lower.add_updater(lambda m: m.become(ax_d.plot(
            lambda x: -np.exp(-gamma_val * time_t.get_value()) * np.sin(x),
            color=C_ORANGE, stroke_width=2, stroke_opacity=0.6
        )))
        env_label.add_updater(lambda m: m.move_to(
            ax_d.c2p(PI*0.5, np.exp(-gamma_val * time_t.get_value())) + UP*0.3
        ))

        self.play(Create(ax_d), Write(ax_d_labels), run_time=0.7)
        self.play(Create(env_upper), Create(env_lower), FadeIn(env_label), run_time=0.8)
        self.play(Create(string), run_time=1.0)
        self.next_slide()  # PAUSE — explain the string and envelope

        # Energy bar setup
        bar_outline = Rectangle(width=6.0, height=0.4, color=C_WHITE, stroke_width=1.5).to_edge(DOWN, buff=0.7)
        e_bar = Rectangle(width=5.8, height=0.3, color=C_RED, fill_color=C_RED, fill_opacity=0.7, stroke_width=0)
        e_bar.move_to(bar_outline.get_center()).align_to(bar_outline, LEFT).shift(RIGHT*0.1)
        
        e_bar.add_updater(lambda m: m.become(
            Rectangle(
                width=max(0.01, 5.8 * np.exp(-2 * gamma_val * time_t.get_value())), height=0.3,
                color=C_RED, fill_color=C_RED, fill_opacity=0.7, stroke_width=0
            ).move_to(bar_outline.get_center()).align_to(bar_outline, LEFT).shift(RIGHT*0.1)
        ))

        energy_lbl = Text("Energy", font_size=18, weight=BOLD, color=C_RED).next_to(bar_outline, LEFT, buff=0.2)
        decay_lbl = MathTex(r"\propto e^{-2\gamma t}", font_size=20, color=C_RED).next_to(bar_outline, RIGHT, buff=0.2)

        self.play(Create(bar_outline), FadeIn(e_bar), FadeIn(energy_lbl), FadeIn(decay_lbl))
        self.next_slide()  # PAUSE — introduce energy bar
        
        self.add(string, env_upper, env_lower, env_label, e_bar)
        
        # Now Animate both time evolving AND bar shrinking!
        self.play(time_t.animate.set_value(6.0), run_time=6.0, rate_func=linear)
        
        # Suspend updaters
        string.suspend_updating()
        env_upper.suspend_updating()
        env_lower.suspend_updating()
        env_label.suspend_updating()
        e_bar.suspend_updating()

        e_identity = MathTex(r"E'(t) = -2\gamma\|u_t\|^2 \leq 0",
                             font_size=28, color=C_GREEN).next_to(bar_outline, UP, buff=0.25)
        self.play(Write(e_identity), Create(self.boxed(e_identity, color=C_GREEN, buff=0.12)))
        self.next_slide()  # PAUSE — explain the energy identity
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 11 — Energy Comparison Plot
    # ══════════════════════════════════════════════════════════════════════════
    def slide_11_comparison_plot(self):
        hdr = self.section_header("Energy Comparison")
        self.play(Write(hdr))

        ax = Axes(x_range=[0, 5, 1], y_range=[0, 1.25, 0.25],
                  x_length=9, y_length=4.5,
                  axis_config={"color": C_GRAY, "include_tip": True, "tip_width": 0.15, "tip_height": 0.15},
                  x_axis_config={"numbers_to_include": [1, 2, 3, 4, 5]},
                  y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0]}).next_to(hdr, DOWN, buff=0.4)
        ax_labels = ax.get_axis_labels(
            x_label=MathTex("t", font_size=26, color=C_WHITE),
            y_label=MathTex("E(t)/E(0)", font_size=24, color=C_WHITE))

        heat_curve = ax.plot(lambda t: np.exp(-1.2*t), color=C_RED, stroke_width=3.5)
        wave_curve = ax.plot(lambda t: 1.0, color=C_BLUE, stroke_width=3.5)
        damped_curve = ax.plot(lambda t: np.exp(-0.35*t), color=C_YELLOW, stroke_width=3.5)

        def legend_item(color, text):
            seg = Line(ORIGIN, 0.6*RIGHT, color=color, stroke_width=4)
            lbl = Text(text, font_size=20, color=color)
            return VGroup(seg, lbl).arrange(RIGHT, buff=0.15)

        legend = VGroup(
            legend_item(C_RED, "Heat: exponential decay"),
            legend_item(C_BLUE, "Wave: conserved"),
            legend_item(C_YELLOW, "Damped wave: gradual decline"),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_corner(DR, buff=0.5)

        self.play(Create(ax), Write(ax_labels), run_time=0.8)
        self.next_slide()  # PAUSE — explain axes

        self.play(Create(heat_curve, run_time=1.2), FadeIn(legend[0]))
        self.next_slide()  # PAUSE — explain heat curve

        self.play(Create(wave_curve, run_time=1.0), FadeIn(legend[1]))
        self.next_slide()  # PAUSE — explain wave curve

        self.play(Create(damped_curve, run_time=1.2), FadeIn(legend[2]))

        heat_note = MathTex(r"e^{-ct}", font_size=18, color=C_RED).next_to(
            ax.c2p(5*0.3, np.exp(-1.2*5*0.3)), DR, buff=0.1)
        wave_note = MathTex(r"E(0)", font_size=18, color=C_BLUE).next_to(
            ax.c2p(5*0.5, 1.0), UP, buff=0.1)
        self.play(FadeIn(heat_note), FadeIn(wave_note))
        self.next_slide()  # PAUSE — compare all three
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 12 — Discussion & Limitations
    # ══════════════════════════════════════════════════════════════════════════
    def slide_12_discussion(self):
        hdr = self.section_header("Discussion & Limitations")
        self.play(Write(hdr))

        pro_title = Text("Strengths", font_size=30, weight=BOLD, color=C_GREEN)
        def pro_item(text):
            return VGroup(Text("✓", font_size=24, weight=BOLD, color=C_GREEN),
                          Text(text, font_size=22, color=C_WHITE)).arrange(RIGHT, buff=0.2)

        pros = VGroup(pro_title, pro_item("No explicit solution needed"),
                      pro_item("Works for linear & nonlinear PDEs"),
                      pro_item("Quantitative stability bounds"),
                      pro_item("Physical intuition (real energy)")).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        con_title = Text("Limitations", font_size=30, weight=BOLD, color=C_RED)
        def con_item(text):
            return VGroup(Text("✗", font_size=24, weight=BOLD, color=C_RED),
                          Text(text, font_size=22, color=C_WHITE)).arrange(RIGHT, buff=0.2)

        cons = VGroup(con_title, con_item("L² control only — no pointwise"),
                      con_item("Nonlinear PDEs harder to handle"),
                      con_item("Does not prove existence")).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        columns = VGroup(pros, cons).arrange(RIGHT, buff=1.8, aligned_edge=UP)
        columns.next_to(hdr, DOWN, buff=0.6)
        divider = DashedLine(columns.get_top()+DOWN*0.2, columns.get_bottom()+UP*0.2,
                             color=C_GRAY, dash_length=0.15, stroke_width=1.5).move_to(columns.get_center())

        self.play(FadeIn(pro_title, shift=DOWN*0.2))
        self.next_slide()  # PAUSE — Intro to strengths
        
        for item in pros[1:]:
            self.play(FadeIn(item, shift=RIGHT*0.2), run_time=0.4)
            self.next_slide()  # PAUSE — after each strength

        self.play(Create(divider))
        self.play(FadeIn(con_title, shift=DOWN*0.2))
        self.next_slide()  # PAUSE — Intro to limitations
        
        for item in cons[1:]:
            self.play(FadeIn(item, shift=RIGHT*0.2), run_time=0.4)
            self.next_slide()  # PAUSE — after each limitation
            
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 13 — Conclusion & Thank You
    # ══════════════════════════════════════════════════════════════════════════
    def slide_13_conclusion(self):
        hdr = self.section_header("Conclusion")
        self.play(Write(hdr))

        points = VGroup(
            MathTex(r"\bullet\;\text{Define } E(t) \geq 0 \text{ measuring solution size}",
                    font_size=28, color=C_WHITE),
            MathTex(r"\bullet\;\text{Derive } E'(t) \leq C\,E(t) \text{ via multiply-and-integrate}",
                    font_size=28, color=C_WHITE),
            MathTex(r"\bullet\;\text{Heat: } E(t) \to 0 \text{ (diffusion dissipates)}",
                    font_size=28, color=C_RED),
            MathTex(r"\bullet\;\text{Wave: } E(t) = E(0) \text{ (energy conserved)}",
                    font_size=28, color=C_BLUE),
            MathTex(r"\bullet\;\text{Damped Wave: } E'(t) = -2\gamma\|u_t\|^2 \leq 0",
                    font_size=28, color=C_YELLOW),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(hdr, DOWN, buff=0.55)

        for p in points:
            self.play(FadeIn(p, shift=UP*0.1), run_time=0.5)
        self.next_slide()  # PAUSE — summarize all results

        final_msg = Text("The Energy Method:", font_size=38, weight=BOLD, color=C_GREEN)
        final_sub = Text("PDE Analysis through a Physical Lens", font_size=30, color=C_TEAL)
        final_group = VGroup(final_msg, final_sub).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        self.play(Write(final_msg), FadeIn(final_sub),
                  Create(self.boxed(final_group, color=C_GREEN, buff=0.2)), run_time=1.0)
        self.next_slide()  # PAUSE — final message
        self.clear()

        # Thank You
        thank = Text("Thank You!", font_size=72, weight=BOLD, color=C_BLUE)
        qs = Text("Questions?", font_size=36, color=C_GRAY)
        name = Text("Souvik Ghorui  ·  IIT Jodhpur", font_size=24, color=C_DGRAY)
        VGroup(thank, qs, name).arrange(DOWN, buff=0.4)
        self.play(Write(thank), run_time=1.0)
        self.play(FadeIn(qs, shift=UP*0.2))
        self.play(FadeIn(name))
        self.wait(1)
        self.next_slide()