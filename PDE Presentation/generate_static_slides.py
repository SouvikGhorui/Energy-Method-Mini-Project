"""
Static Slides Generator for Energy Methods Presentation
Outputs PNG images for each slide's final state.
"""

from manim import *
import numpy as np
import os

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


class GenerateStaticSlides(Scene):
    """Outputs static PNG frames of each slide."""

    def save_slide(self, name):
        """Helper to pause for a fraction of a second, save the frame as a PNG, and clear."""
        self.wait(0.1) # Ensure everything is drawn to the camera
        
        # Create output directory if it doesn't exist
        out_dir = "Static_Slides"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            
        # Save the current frame to an image
        self.camera.get_image().save(os.path.join(out_dir, f"{name}.png"))
        self.clear()

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
    # SLIDE 1 — Title Card
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

        self.add(heat_waves, title_group)
        self.save_slide("Slide_01_Title")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 2 — Motivation: Physical Reality → Mathematical Model
    # ══════════════════════════════════════════════════════════════════════════
    def slide_02_motivation(self):
        hdr = self.section_header("Why Energy Methods?")

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

        math_label = Text("Mathematical Model", font_size=26, weight=BOLD, color=C_BLUE)
        pde_eq = MathTex(r"u_t = k\,u_{xx}", font_size=36, color=C_BLUE)
        ic_eq = MathTex(r"u(x,0) = \varphi(x)", font_size=28, color=C_GREEN)
        bc_eq = MathTex(r"u(0,t) = u(L,t) = 0", font_size=28, color=C_YELLOW)
        math_group = VGroup(math_label, pde_eq, ic_eq, bc_eq).arrange(DOWN, buff=0.3)
        math_group.shift(RIGHT * 3 + DOWN * 0.5)

        arrow = Arrow(phys_group.get_right() + RIGHT * 0.2, math_group.get_left() + LEFT * 0.2, color=C_WHITE, buff=0.15, stroke_width=3)
        arrow_label = Text("Model", font_size=18, color=C_GRAY).next_to(arrow, UP, buff=0.08)

        question = Text("Does this PDE have a unique solution?", font_size=28, weight=BOLD, color=C_YELLOW).to_edge(DOWN, buff=0.6)

        self.add(hdr, phys_group, math_group, arrow, arrow_label, question)
        self.save_slide("Slide_02_Motivation")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 3 — Hadamard's Trinity
    # ══════════════════════════════════════════════════════════════════════════
    def slide_03_hadamard(self):
        hdr = self.section_header("Hadamard's Well-Posedness  (1902)")

        def make_orb(label_text, color, pos):
            circle = Circle(radius=0.8, color=color, fill_color=color, fill_opacity=0.15, stroke_width=2.5)
            glow = Circle(radius=1.05, color=color, fill_opacity=0.05, stroke_width=0.5)
            label = Text(label_text, font_size=22, weight=BOLD, color=color)
            label.move_to(circle.get_center())
            return VGroup(glow, circle, label).move_to(pos)

        orb_exist  = make_orb("Existence",  C_GRAY,  LEFT * 4 + DOWN * 0.5)
        orb_unique = make_orb("Uniqueness", C_GREEN, DOWN * 0.3)
        orb_stab   = make_orb("Stability",  C_GRAY,  RIGHT * 4 + DOWN * 0.5)

        # Scale down un-focused orbs, scale up target
        orb_exist.set_opacity(0.25).scale(0.7)
        orb_stab.set_opacity(0.25).scale(0.7)
        orb_unique[1].set(fill_opacity=0.3, stroke_width=4)
        orb_unique.scale(1.8)

        focus_text = Text("Energy method targets this!", font_size=26, color=C_GREEN).next_to(orb_unique, DOWN, buff=0.5)

        self.add(hdr, orb_exist, orb_unique, orb_stab, focus_text)
        self.save_slide("Slide_03_Hadamard")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 4 — The Energy Functional E(t)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_04_energy_functional(self):
        hdr = self.section_header("The Energy Functional  E(t)")
        energy_def = MathTex(r"E(t) = \frac{1}{2} \int_0^L u^2 \, dx", font_size=42, color=C_YELLOW).next_to(hdr, DOWN, buff=0.7)

        ax = Axes(x_range=[0, PI, PI/4], y_range=[-0.2, 1.3, 0.5],
                  x_length=5.5, y_length=3.0,
                  axis_config={"color": C_GRAY, "include_tip": False}).shift(DOWN*1.5 + LEFT*0.5)
        ax_labels = ax.get_axis_labels(x_label=MathTex("x", font_size=22, color=C_GRAY), y_label=MathTex("", font_size=22))

        # We show the u^2(x) final state curve directly
        u2_curve = ax.plot(lambda x: np.sin(x)**2, color=C_GREEN, stroke_width=3)
        u2_label = MathTex(r"u^2(x)", font_size=22, color=C_GREEN).next_to(ax.c2p(PI*0.35, np.sin(PI*0.35)**2), UP, buff=0.1)
        area = ax.get_area(u2_curve, x_range=[0, PI], color=C_GREEN, opacity=0.25)
        
        area_label = MathTex(r"E(t) = \tfrac{1}{2}\int u^2\,dx", font_size=22, color=C_GREEN).next_to(ax, RIGHT, buff=0.5)
        key = MathTex(r"E(t) \geq 0, \qquad E(t)=0 \;\Leftrightarrow\; u \equiv 0", font_size=30, color=C_YELLOW).to_edge(DOWN, buff=0.5)

        self.add(hdr, energy_def, ax, ax_labels, u2_curve, u2_label, area, area_label, key, self.boxed(key, color=C_YELLOW))
        self.save_slide("Slide_04_Energy_Functional")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 5 — The "Difference" Proof
    # ══════════════════════════════════════════════════════════════════════════
    def slide_05_difference_proof(self):
        hdr = self.section_header("The Uniqueness Proof Strategy")

        ax = Axes(x_range=[0, PI, PI/4], y_range=[-0.3, 1.5, 0.5], x_length=6, y_length=3.0,
                  axis_config={"color": C_GRAY, "include_tip": False}).shift(DOWN*0.3)

        w_curve = ax.plot(lambda x: 0.3*np.sin(x), color=C_YELLOW, stroke_width=3, stroke_opacity=0.3)
        w_lbl = MathTex(r"w = u_1 - u_2", font_size=24, color=C_YELLOW).next_to(ax.c2p(PI*0.4, 0.3*np.sin(PI*0.4)), UP, buff=0.2)
        zero_curve = ax.plot(lambda x: 0, color=C_GREEN, stroke_width=2)

        facts = VGroup(
            MathTex(r"w \text{ solves homogeneous IBVP}", font_size=26, color=C_WHITE),
            MathTex(r"w(x,0) = 0 \;\Rightarrow\; E_w(0) = 0", font_size=26, color=C_GREEN),
            MathTex(r"E_w'(t) \leq 0 \;\Rightarrow\; E_w(t) = 0 \;\Rightarrow\; w \equiv 0", font_size=26, color=C_GREEN),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.4)

        conclusion = MathTex(r"\therefore\; u_1 = u_2 \quad \checkmark", font_size=36, color=C_GREEN).next_to(facts, RIGHT, buff=0.5)

        self.add(hdr, ax, w_curve, zero_curve, w_lbl, facts, conclusion, self.boxed(conclusion, color=C_GREEN))
        self.save_slide("Slide_05_Difference_Proof")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 6 — Heat Equation (Split Screen)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_06_heat_equation(self):
        hdr = self.section_header("Application 1: Heat Equation")
        divider = DashedLine(UP*2.8, DOWN*3.5, color=C_GRAY, dash_length=0.15, stroke_width=1.5)

        left_title = Text("The PDE", font_size=24, weight=BOLD, color=C_RED)
        pde = MathTex(r"u_t = k\,u_{xx}", font_size=36, color=C_RED)
        bcs = MathTex(r"u(0,t) = u(L,t) = 0", font_size=26, color=C_WHITE)
        step1 = Text("Multiply by u, integrate:", font_size=20, color=C_GRAY)
        derive1 = MathTex(r"E'(t) = \int_0^L u \cdot u_t\,dx", font_size=26, color=C_WHITE)
        derive2 = MathTex(r"= \int_0^L u \cdot k\,u_{xx}\,dx", font_size=26, color=C_WHITE)
        derive3 = MathTex(r"\xrightarrow{\text{IBP}}\; -k\|u_x\|^2", font_size=26, color=C_WHITE)
        left_group = VGroup(left_title, pde, bcs, step1, derive1, derive2, derive3).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(LEFT*3.5 + DOWN*0.3)

        right_title = Text("Energy Identity", font_size=24, weight=BOLD, color=C_GREEN)
        result = MathTex(r"E'(t) = -k\|u_x\|^2 \leq 0", font_size=34, color=C_GREEN)
        note1 = MathTex(r"-k\|u_x\|^2 \leq 0", font_size=26, color=C_YELLOW)
        note1_text = Text("Diffusion always dissipates", font_size=20, color=C_GRAY)
        implication = MathTex(r"\Rightarrow\; E(t) \leq E(0)", font_size=30, color=C_BLUE)
        uniqueness = MathTex(r"E_w(0) = 0 \;\Rightarrow\; E_w(t) = 0", font_size=28, color=C_GREEN)
        uniqueness_label = Text("⇒ Uniqueness ✓", font_size=22, weight=BOLD, color=C_GREEN)
        right_group = VGroup(right_title, result, note1, note1_text, implication, uniqueness, uniqueness_label).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(RIGHT*2.5 + DOWN*0.3)
        result_box = self.boxed(result, color=C_GREEN)

        self.add(hdr, divider, left_group, right_group, result_box)
        self.save_slide("Slide_06_Heat_Equation")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 7 — Thermal Dissipation Visualization
    # ══════════════════════════════════════════════════════════════════════════
    def slide_07_thermal_dissipation(self):
        hdr = self.section_header("Visualization: Thermal Dissipation")
        
        ax_heat = Axes(x_range=[0, PI, PI/4], y_range=[-0.1, 1.2, 0.5], x_length=5.0, y_length=3.0,
                       axis_config={"color": C_GRAY, "include_tip": False}).shift(LEFT*3 + DOWN*0.8)
        heat_label = Text("Temperature profile u(x,t)", font_size=20, color=C_GRAY).next_to(ax_heat, UP, buff=0.15)

        decay_rate = 1.5
        curves = VGroup()
        for i, (t_val, col) in enumerate(zip([0.0, 0.3, 0.8, 1.5, 3.0],[C_RED, C_ORANGE, C_YELLOW, C_GREEN, C_BLUE])):
            amp = np.exp(-decay_rate * t_val)
            curve = ax_heat.plot(lambda x, a=amp: a*np.sin(x), color=col, stroke_width=2.5)
            lbl = MathTex(f"t={t_val:.1f}", font_size=16, color=col).next_to(ax_heat.c2p(PI*0.5, amp*np.sin(PI*0.5)), RIGHT, buff=0.15)
            curves.add(VGroup(curve, lbl))

        ax_e = Axes(x_range=[0, 4, 1], y_range=[0, 1.15, 0.5], x_length=4.5, y_length=3.0,
                    axis_config={"color": C_GRAY, "include_tip": False},
                    x_axis_config={"numbers_to_include":[1, 2, 3]},
                    y_axis_config={"numbers_to_include":[0.5, 1.0]}).shift(RIGHT*3 + DOWN*0.8)
        ax_e_labels = ax_e.get_axis_labels(x_label=MathTex("t", font_size=22, color=C_GRAY), y_label=MathTex("E(t)", font_size=22, color=C_GRAY))

        decay_curve = ax_e.plot(lambda t: np.exp(-decay_rate*t), color=C_GREEN, stroke_width=3)
        decay_label = MathTex(r"E(0)\,e^{-2k\pi^2 t/L^2}", font_size=20, color=C_GREEN).next_to(ax_e.c2p(4*0.15, np.exp(-decay_rate*4*0.15)), UR, buff=0.1)

        poincare_box = MathTex(r"\text{Poincar\'{e}: } \|u_x\|^2 \geq \frac{\pi^2}{L^2}\|u\|^2", font_size=22, color=C_YELLOW).to_edge(DOWN, buff=0.4)

        self.add(hdr, ax_heat, heat_label, curves, ax_e, ax_e_labels, decay_curve, decay_label, poincare_box)
        self.save_slide("Slide_07_Thermal_Dissipation")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 8 — Wave Equation
    # ══════════════════════════════════════════════════════════════════════════
    def slide_08_wave_equation(self):
        hdr = self.section_header("Application 2: Wave Equation")
        pde = MathTex(r"u_{tt} = c^2 u_{xx}", font_size=36, color=C_BLUE)
        energy = MathTex(r"E(t) = \frac{1}{2}\int_0^L \!\bigl(u_t^2 + c^2 u_x^2\bigr)\,dx", font_size=30, color=C_YELLOW)
        conservation = MathTex(r"E'(t) = 0 \;\Rightarrow\; E(t) = E(0) \quad \text{(conserved!)}", font_size=30, color=C_GREEN)
        eqs = VGroup(pde, energy, conservation).arrange(DOWN, buff=0.3).next_to(hdr, DOWN, buff=0.5)

        ax_w = Axes(x_range=[0, PI, PI/4], y_range=[-1.2, 1.2, 0.5], x_length=5.5, y_length=2.5,
                    axis_config={"color": C_GRAY, "include_tip": False}).shift(LEFT*2.5 + DOWN*2.0)

        # Fixed time for static plot
        wave_time = 1.0 
        string = ax_w.plot(lambda x: np.sin(x) * np.cos(wave_time * 3), color=C_TEAL, stroke_width=3.5)
        
        # Energy Bars layout — match presentation's final swapped state
        bar_base = RIGHT*3.5 + DOWN*2.0
        bar_height, bar_width = 1.8, 0.7
        ke_val, pe_val = 0.3, 0.7

        # Show the swapped bars (final state of the presentation)
        ke_bar = Rectangle(width=bar_width, height=bar_height*pe_val, color=C_RED, fill_color=C_RED, fill_opacity=0.5, stroke_width=2).move_to(bar_base + LEFT*0.6 + UP*bar_height*pe_val/2)
        ke_lbl = Text("KE", font_size=18, weight=BOLD, color=C_RED).next_to(ke_bar, DOWN, buff=0.1)
        pe_bar = Rectangle(width=bar_width, height=bar_height*ke_val, color=C_BLUE, fill_color=C_BLUE, fill_opacity=0.5, stroke_width=2).move_to(bar_base + RIGHT*0.6 + UP*bar_height*ke_val/2)
        pe_lbl = Text("PE", font_size=18, weight=BOLD, color=C_BLUE).next_to(pe_bar, DOWN, buff=0.1)
        total_line = DashedLine(bar_base + LEFT*1.5 + UP*bar_height*(ke_val+pe_val)/2, bar_base + RIGHT*1.5 + UP*bar_height*(ke_val+pe_val)/2, color=C_GREEN, dash_length=0.1, stroke_width=2)
        total_lbl = Text("Total E", font_size=16, color=C_GREEN).next_to(total_line, RIGHT, buff=0.1)

        # Conservation box (shown at the end of the presentation slide)
        conservation_box = self.boxed(conservation, color=C_GREEN)

        self.add(hdr, eqs, conservation_box, ax_w, string, ke_bar, pe_bar, ke_lbl, pe_lbl, total_line, total_lbl)
        self.save_slide("Slide_08_Wave_Equation")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 9 — Reaction-Diffusion (Tipping Point)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_09_reaction_diffusion(self):
        hdr = self.section_header("Reaction-Diffusion: Tipping Point")
        pde = MathTex(r"u_t = k\,u_{xx} + r\,u", font_size=36, color=C_ORANGE).next_to(hdr, DOWN, buff=0.55)
        r_crit_eq = MathTex(r"r_{\text{crit}} = k\left(\frac{\pi}{L}\right)^2", font_size=34, color=C_YELLOW).next_to(pde, DOWN, buff=0.4)

        ax_decay = Axes(x_range=[0, PI, PI/2], y_range=[-0.1, 1.2, 0.5], x_length=4.5, y_length=2.5,
                        axis_config={"color": C_GRAY, "include_tip": False}).shift(LEFT*3.5 + DOWN*1.8)
        decay_title = Text("Decay: Diffusion Wins", font_size=20, weight=BOLD, color=C_BLUE).next_to(ax_decay, UP, buff=0.15)
        decay_sub = MathTex(r"r < r_{\text{crit}}", font_size=22, color=C_BLUE).next_to(decay_title, DOWN, buff=0.08)

        decay_curves = VGroup()
        for i, t_val in enumerate([0.0, 0.5, 1.0, 2.0]):
            amp = np.exp(-0.8*t_val)
            decay_curves.add(ax_decay.plot(lambda x, a=amp: a*np.sin(x), color=C_BLUE, stroke_width=2.5, stroke_opacity=1.0-0.2*i))

        ax_grow = Axes(x_range=[0, PI, PI/2], y_range=[-0.1, 3.5, 1.0], x_length=4.5, y_length=2.5,
                       axis_config={"color": C_GRAY, "include_tip": False}).shift(RIGHT*3.5 + DOWN*1.8)
        grow_title = Text("Growth: Reaction Wins", font_size=20, weight=BOLD, color=C_RED).next_to(ax_grow, UP, buff=0.15)
        grow_sub = MathTex(r"r > r_{\text{crit}}", font_size=22, color=C_RED).next_to(grow_title, DOWN, buff=0.08)

        grow_curves = VGroup()
        for i, t_val in enumerate([0.0, 0.3, 0.6, 0.9]):
            amp = np.exp(1.2*t_val)
            grow_curves.add(ax_grow.plot(lambda x, a=amp: a*np.sin(x), color=C_RED, stroke_width=2.5, stroke_opacity=0.4+0.2*i))

        div_line = DashedLine(r_crit_eq.get_bottom()+DOWN*0.3, DOWN*3.5, color=C_GRAY, dash_length=0.12, stroke_width=1.5)
        energy_note = MathTex(r"E'(t) = (-k\pi^2/L^2 + r)\,E(t)", font_size=24, color=C_WHITE).to_edge(DOWN, buff=0.35)

        self.add(hdr, pde, r_crit_eq, ax_decay, decay_title, decay_sub, decay_curves, ax_grow, grow_title, grow_sub, grow_curves, div_line, energy_note)
        self.save_slide("Slide_09_Reaction_Diffusion")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 09b — Reaction-Diffusion Example 1
    # ══════════════════════════════════════════════════════════════════════════
    def slide_09b_reaction_diffusion_example(self):
        hdr = self.section_header("Example 1: Heat Eq. with Reaction Term")

        pde_group = VGroup(
            MathTex(r"u_t = u_{xx} + u", font_size=34, color=C_BLUE),
            MathTex(r"x \in (0, \pi), \quad t > 0", font_size=26, color=C_WHITE),
            MathTex(r"u(x,0) = \sin x", font_size=28, color=C_GREEN),
            MathTex(r"u(0,t) = 0, \quad u(\pi,t) = 0", font_size=28, color=C_YELLOW)
        ).arrange(DOWN, buff=0.2).next_to(hdr, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        prob_box = self.boxed(pde_group, color=C_GRAY, buff=0.2)
        
        part_a_title = Text("(a) Energy equation", font_size=24, weight=BOLD, color=C_WHITE)
        e_deriv = MathTex(r"E'(t) =", r"-\|u_x\|^2", r"+", r"\|u\|^2", font_size=30, color=C_TEAL)
        e_deriv.set_color_by_tex(r"-\|u_x\|^2", C_RED)
        e_deriv.set_color_by_tex(r"\|u\|^2", C_GREEN)
        part_a = VGroup(part_a_title, e_deriv).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(prob_box, DOWN, buff=0.5).align_to(prob_box, LEFT)

        part_b_title = Text("(b) Growth or decay?", font_size=24, weight=BOLD, color=C_WHITE)
        poincare = MathTex(r"\text{Poincar\'{e} (}L=\pi\text{): } \|u_x\|^2 \geq \frac{\pi^2}{\pi^2}\|u\|^2 = \|u\|^2", font_size=26, color=C_YELLOW)
        e_bound = MathTex(r"\Rightarrow \quad E'(t) \leq -\|u\|^2 + \|u\|^2 = 0", font_size=28, color=C_GREEN)
        e_bound_text = Text("Energy is non-increasing!", font_size=20, color=C_GREEN)
        part_b = VGroup(part_b_title, poincare, e_bound, e_bound_text).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(prob_box, RIGHT, buff=1.0).align_to(prob_box, UP)

        part_c_title = Text("(c) Uniqueness", font_size=24, weight=BOLD, color=C_WHITE)
        w_eq = MathTex(r"\text{Let } w = u_1 - u_2 \Rightarrow E_w'(t) \leq 0", font_size=26, color=C_GRAY)
        w_zero = MathTex(r"E_w(0) = 0 \Rightarrow E_w(t) = 0 \Rightarrow w \equiv 0", font_size=26, color=C_BLUE)
        part_c = VGroup(part_c_title, w_eq, w_zero).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(part_b, DOWN, buff=0.6).align_to(part_b, LEFT)
        
        uniq_check = Text("Uniqueness follows ✓", font_size=24, weight=BOLD, color=C_GREEN).next_to(part_c, DOWN, buff=0.3)

        self.add(hdr, prob_box, pde_group, part_a, part_b, part_c, uniq_check)
        self.save_slide("Slide_09b_Reaction_Example")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 10 — Damped Wave
    # ══════════════════════════════════════════════════════════════════════════
    def slide_10_damped_wave(self):
        hdr = self.section_header("Damped Wave: Dissipation")
        pde = MathTex(r"u_{tt} + 2\gamma\,u_t = c^2\,u_{xx}, \quad \gamma > 0", font_size=34, color=C_ORANGE).next_to(hdr, DOWN, buff=0.5)

        ax_d = Axes(x_range=[0, PI, PI/4], y_range=[-1.3, 1.3, 0.5], x_length=8, y_length=3.5,
                    axis_config={"color": C_GRAY, "include_tip": False}).shift(DOWN*1.2)
        ax_d_labels = ax_d.get_axis_labels(x_label=MathTex("x", font_size=22, color=C_GRAY), y_label=MathTex("u", font_size=22, color=C_GRAY))

        gamma_val = 0.2
        omega = 4.0
        time_t = 3.5  # Static state snapshot mid-decay

        string = ax_d.plot(lambda x: np.exp(-gamma_val * time_t) * np.sin(x) * np.cos(omega * time_t), color=C_TEAL, stroke_width=3.5)
        env_upper = ax_d.plot(lambda x: np.exp(-gamma_val * time_t) * np.sin(x), color=C_ORANGE, stroke_width=2, stroke_opacity=0.6)
        env_lower = ax_d.plot(lambda x: -np.exp(-gamma_val * time_t) * np.sin(x), color=C_ORANGE, stroke_width=2, stroke_opacity=0.6)
        env_label = MathTex(r"Ae^{-\gamma t}\sin(x)", font_size=22, color=C_ORANGE).next_to(ax_d.c2p(PI*0.5, np.exp(-gamma_val * time_t)) + UP*0.3, UP, buff=0.2)

        bar_outline = Rectangle(width=6.0, height=0.4, color=C_WHITE, stroke_width=1.5).to_edge(DOWN, buff=0.7)
        e_width = max(0.01, 5.8 * np.exp(-2 * gamma_val * time_t))
        e_bar = Rectangle(width=e_width, height=0.3, color=C_RED, fill_color=C_RED, fill_opacity=0.7, stroke_width=0).move_to(bar_outline.get_center()).align_to(bar_outline, LEFT).shift(RIGHT*0.1)
        
        energy_lbl = Text("Energy", font_size=18, weight=BOLD, color=C_RED).next_to(bar_outline, LEFT, buff=0.2)
        decay_lbl = MathTex(r"\propto e^{-2\gamma t}", font_size=20, color=C_RED).next_to(bar_outline, RIGHT, buff=0.2)
        e_identity = MathTex(r"E'(t) = -2\gamma\|u_t\|^2 \leq 0", font_size=28, color=C_GREEN).next_to(bar_outline, UP, buff=0.25)

        self.add(hdr, pde, ax_d, ax_d_labels, string, env_upper, env_lower, env_label, bar_outline, e_bar, energy_lbl, decay_lbl, e_identity, self.boxed(e_identity, color=C_GREEN, buff=0.12))
        self.save_slide("Slide_10_Damped_Wave")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 11 — Energy Comparison Plot
    # ══════════════════════════════════════════════════════════════════════════
    def slide_11_comparison_plot(self):
        hdr = self.section_header("Energy Comparison")
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 1.25, 0.25], x_length=9, y_length=4.5,
                  axis_config={"color": C_GRAY, "include_tip": True, "tip_width": 0.15, "tip_height": 0.15},
                  x_axis_config={"numbers_to_include":[1, 2, 3, 4, 5]},
                  y_axis_config={"numbers_to_include":[0.25, 0.5, 0.75, 1.0]}).next_to(hdr, DOWN, buff=0.4)
        ax_labels = ax.get_axis_labels(x_label=MathTex("t", font_size=26, color=C_WHITE), y_label=MathTex("E(t)/E(0)", font_size=24, color=C_WHITE))

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

        heat_note = MathTex(r"e^{-ct}", font_size=18, color=C_RED).next_to(ax.c2p(5*0.3, np.exp(-1.2*5*0.3)), DR, buff=0.1)
        wave_note = MathTex(r"E(0)", font_size=18, color=C_BLUE).next_to(ax.c2p(5*0.5, 1.0), UP, buff=0.1)

        self.add(hdr, ax, ax_labels, heat_curve, wave_curve, damped_curve, legend, heat_note, wave_note)
        self.save_slide("Slide_11_Comparison_Plot")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 12 — Discussion & Limitations
    # ══════════════════════════════════════════════════════════════════════════
    def slide_12_discussion(self):
        hdr = self.section_header("Discussion & Limitations")
        pro_title = Text("Strengths", font_size=30, weight=BOLD, color=C_GREEN)
        def pro_item(text):
            return VGroup(Text("✓", font_size=24, weight=BOLD, color=C_GREEN), Text(text, font_size=22, color=C_WHITE)).arrange(RIGHT, buff=0.2)
        pros = VGroup(pro_title, pro_item("No explicit solution needed"), pro_item("Works for linear & nonlinear PDEs"),
                      pro_item("Quantitative stability bounds"), pro_item("Physical intuition (real energy)")).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        con_title = Text("Limitations", font_size=30, weight=BOLD, color=C_RED)
        def con_item(text):
            return VGroup(Text("✗", font_size=24, weight=BOLD, color=C_RED), Text(text, font_size=22, color=C_WHITE)).arrange(RIGHT, buff=0.2)
        cons = VGroup(con_title, con_item("L² control only — no pointwise"), con_item("Nonlinear PDEs harder to handle"),
                      con_item("Does not prove existence")).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        columns = VGroup(pros, cons).arrange(RIGHT, buff=1.8, aligned_edge=UP).next_to(hdr, DOWN, buff=0.6)
        divider = DashedLine(columns.get_top()+DOWN*0.2, columns.get_bottom()+UP*0.2, color=C_GRAY, dash_length=0.15, stroke_width=1.5).move_to(columns.get_center())

        self.add(hdr, columns, divider)
        self.save_slide("Slide_12_Discussion")

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 13 — Conclusion & Thank You
    # ══════════════════════════════════════════════════════════════════════════
    def slide_13_conclusion(self):
        hdr = self.section_header("Conclusion")
        points = VGroup(
            MathTex(r"\bullet\;\text{Define } E(t) \geq 0 \text{ measuring solution size}", font_size=28, color=C_WHITE),
            MathTex(r"\bullet\;\text{Derive } E'(t) \leq C\,E(t) \text{ via multiply-and-integrate}", font_size=28, color=C_WHITE),
            MathTex(r"\bullet\;\text{Heat: } E(t) \to 0 \text{ (diffusion dissipates)}", font_size=28, color=C_RED),
            MathTex(r"\bullet\;\text{Wave: } E(t) = E(0) \text{ (energy conserved)}", font_size=28, color=C_BLUE),
            MathTex(r"\bullet\;\text{Damped Wave: } E'(t) = -2\gamma\|u_t\|^2 \leq 0", font_size=28, color=C_YELLOW),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(hdr, DOWN, buff=0.55)

        final_msg = Text("The Energy Method:", font_size=38, weight=BOLD, color=C_GREEN)
        final_sub = Text("PDE Analysis through a Physical Lens", font_size=30, color=C_TEAL)
        final_group = VGroup(final_msg, final_sub).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)

        self.add(hdr, points, final_group, self.boxed(final_group, color=C_GREEN, buff=0.2))
        self.save_slide("Slide_13_Conclusion")

        # Thank You (part of slide 13 in the presentation)
        thank = Text("Thank You!", font_size=72, weight=BOLD, color=C_BLUE)
        qs = Text("Questions?", font_size=36, color=C_GRAY)
        name = Text("Souvik Ghorui  ·  IIT Jodhpur", font_size=24, color=C_DGRAY)
        grp = VGroup(thank, qs, name).arrange(DOWN, buff=0.4)
        
        self.add(grp)
        self.save_slide("Slide_13b_Thank_You")