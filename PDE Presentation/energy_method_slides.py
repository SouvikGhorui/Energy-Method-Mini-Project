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


# ── Colour palette ────────────────────────────────────────────────────────────
BG       = "#0F172A"
C_BLUE   = "#60A5FA"
C_GREEN  = "#34D399"
C_RED    = "#F87171"
C_YELLOW = "#FCD34D"
C_ORANGE = "#FB923C"
C_GRAY   = "#94A3B8"
C_WHITE  = "#F1F5F9"


class EnergyMethodPresentation(Slide):
    """15-minute research presentation on the energy method for IBVPs."""

    # ── helpers ───────────────────────────────────────────────────────────────

    def clear(self):
        """Fade out every current mobject."""
        mobs = [m for m in self.mobjects if not isinstance(m, (Camera,))]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.5)

    def slide_header(self, text, color=C_BLUE):
        t = Text(text, font_size=34, weight=BOLD, color=color)
        line = Line(6.5 * LEFT, 6.5 * RIGHT, color=color, stroke_width=1.5)
        line.next_to(t, DOWN, buff=0.12)
        g = VGroup(t, line).to_corner(UL, buff=0.45)
        return g

    def bullet(self, text, color=C_WHITE, size=26):
        return Text(f"• {text}", font_size=size, color=color)

    def boxed(self, mob, color=C_GREEN, buff=0.18):
        return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12)

    # ── construct ─────────────────────────────────────────────────────────────

    def construct(self):
        self.camera.background_color = ManimColor(BG)

        self.slide_01_title()
        self.slide_02_ibvp()
        self.slide_03_wellposedness()
        self.slide_04_math_tools()
        self.slide_05_energy_functional()
        self.slide_06_two_step()
        self.slide_07_uniqueness_flow()
        self.slide_08_heat_equation()
        self.slide_09_energy_decay()
        self.slide_10_wave_equation()
        self.slide_11_comparison()
        self.slide_12_damped_wave()
        self.slide_13_strengths_limits()
        self.slide_14_conclusion()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 1 — Title
    # ══════════════════════════════════════════════════════════════════════════
    def slide_01_title(self):
        title = VGroup(
            Text("Energy Methods", font_size=54, weight=BOLD, color=C_BLUE),
            Text("and Uniqueness of IBVPs", font_size=36, color=C_WHITE),
            Text("─" * 42, font_size=18, color=C_GRAY),
            Text("Souvik Ghorui  ·  M25MA2008", font_size=24, color=C_GRAY),
            Text("Course: Partial Differential Equations", font_size=20, color=C_GRAY),
        ).arrange(DOWN, buff=0.32)

        self.play(Write(title[0]), run_time=1.2)
        self.play(FadeIn(title[1], shift=UP * 0.3))
        self.play(FadeIn(title[2]), FadeIn(title[3]), FadeIn(title[4]))
        self.wait(0.5)
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 2 — What is an IBVP?
    # ══════════════════════════════════════════════════════════════════════════
    def slide_02_ibvp(self):
        hdr = self.slide_header("What is an IBVP?")
        self.play(Write(hdr))

        parts = VGroup(
            VGroup(
                Text("PDE", font_size=24, weight=BOLD, color=C_BLUE),
                MathTex(r"\mathcal{L}[u]=f(x,t),\quad x\in(0,L),\ t>0",
                        font_size=32, color=C_BLUE),
            ).arrange(RIGHT, buff=0.4),
            VGroup(
                Text("IC ", font_size=24, weight=BOLD, color=C_GREEN),
                MathTex(r"u(x,0)=\varphi(x),\quad x\in[0,L]",
                        font_size=32, color=C_GREEN),
            ).arrange(RIGHT, buff=0.4),
            VGroup(
                Text("BC ", font_size=24, weight=BOLD, color=C_YELLOW),
                MathTex(r"u(0,t)=g_1(t),\quad u(L,t)=g_2(t)",
                        font_size=32, color=C_YELLOW),
            ).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT).next_to(hdr, DOWN, buff=0.7)

        # Animated rod diagram
        rod = Rectangle(width=5, height=0.6, color=C_ORANGE, fill_color=C_ORANGE,
                        fill_opacity=0.3).shift(DOWN * 2.4)
        left_tick  = Line(rod.get_left()  + DOWN * 0.4, rod.get_left()  + UP * 0.4, color=C_WHITE)
        right_tick = Line(rod.get_right() + DOWN * 0.4, rod.get_right() + UP * 0.4, color=C_WHITE)
        x0_lbl = MathTex("x=0", font_size=22, color=C_GRAY).next_to(left_tick,  DOWN, buff=0.1)
        xL_lbl = MathTex("x=L", font_size=22, color=C_GRAY).next_to(right_tick, DOWN, buff=0.1)
        u_lbl  = MathTex("u(x,t)", font_size=24, color=C_ORANGE).next_to(rod, UP, buff=0.15)
        diagram = VGroup(rod, left_tick, right_tick, x0_lbl, xL_lbl, u_lbl)

        self.play(Create(diagram))
        for p in parts:
            self.play(FadeIn(p, shift=RIGHT * 0.25))
            self.wait(0.2)

        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 3 — Well-Posedness
    # ══════════════════════════════════════════════════════════════════════════
    def slide_03_wellposedness(self):
        hdr = self.slide_header("Well-Posedness  (Hadamard, 1902)")
        self.play(Write(hdr))

        conds = VGroup(
            self.bullet("Existence  — a solution exists",      color=C_WHITE),
            self.bullet("Uniqueness — solution is unique",      color=C_GREEN),
            self.bullet("Stability  — depends continuously on data", color=C_WHITE),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(hdr, DOWN, buff=0.7)

        for c in conds:
            self.play(FadeIn(c, shift=RIGHT * 0.3))
            self.wait(0.25)

        self.next_slide()

        box = self.boxed(conds[1], color=C_GREEN)
        caption = Text("← Energy method targets this!", font_size=22, color=C_GREEN)
        caption.next_to(box, RIGHT, buff=0.3)
        self.play(Create(box), FadeIn(caption))

        note = Text("(also gives stability estimates)", font_size=20, color=C_GRAY)
        note.next_to(conds[2], RIGHT, buff=0.3)
        self.play(FadeIn(note))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 4 — Mathematical Tools
    # ══════════════════════════════════════════════════════════════════════════
    def slide_04_math_tools(self):
        hdr = self.slide_header("Mathematical Tools")
        self.play(Write(hdr))

        # L2 norm
        t_l2 = Text("L² Norm", font_size=26, weight=BOLD, color=C_BLUE)
        e_l2 = MathTex(r"\|u\|^2 = \int_0^L u^2\,dx", font_size=34)
        row1 = VGroup(t_l2, e_l2).arrange(RIGHT, buff=0.5)

        # IBP key identity
        t_ibp = Text("Integration by Parts  (Dirichlet BCs)", font_size=26, weight=BOLD, color=C_ORANGE)
        e_ibp = MathTex(r"\int_0^L u_{xx}\,u\,dx \;=\; -\|u_x\|^2", font_size=34)
        row2 = VGroup(t_ibp, e_ibp).arrange(RIGHT, buff=0.5)

        # Gronwall
        t_gr = Text("Gronwall's Inequality", font_size=26, weight=BOLD, color=C_GREEN)
        e_gr = MathTex(r"E'(t)\leq C\,E(t) \;\Longrightarrow\; E(t)\leq E(0)\,e^{Ct}",
                       font_size=34)
        row3 = VGroup(t_gr, e_gr).arrange(RIGHT, buff=0.5)

        rows = VGroup(row1, row2, row3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        rows.next_to(hdr, DOWN, buff=0.65)

        dividers = VGroup(
            DashedLine(5 * LEFT, 5 * RIGHT, color=C_GRAY, dash_length=0.15, stroke_width=1)
            .next_to(row1, DOWN, buff=0.25),
            DashedLine(5 * LEFT, 5 * RIGHT, color=C_GRAY, dash_length=0.15, stroke_width=1)
            .next_to(row2, DOWN, buff=0.25),
        )

        self.play(FadeIn(row1))
        self.next_slide()
        self.play(Create(dividers[0]), FadeIn(row2))
        self.next_slide()
        self.play(Create(dividers[1]), FadeIn(row3))
        box_gr = self.boxed(e_gr, color=C_GREEN)
        self.play(Create(box_gr))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 5 — Energy Functional
    # ══════════════════════════════════════════════════════════════════════════
    def slide_05_energy_functional(self):
        hdr = self.slide_header("The Energy Functional  E(t)")
        self.play(Write(hdr))

        heat_lbl = Text("Heat Equation  (1st order in t)", font_size=26,
                        weight=BOLD, color=C_RED)
        heat_eq  = MathTex(r"E(t)=\frac{1}{2}\|u(\cdot,t)\|^2=\frac{1}{2}\int_0^L u^2\,dx",
                           font_size=34, color=C_RED)
        heat     = VGroup(heat_lbl, heat_eq).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        wave_lbl = Text("Wave Equation  (2nd order in t)", font_size=26,
                        weight=BOLD, color=C_BLUE)
        wave_eq  = MathTex(r"E(t)=\frac{1}{2}\int_0^L\!\bigl(u_t^2+c^2u_x^2\bigr)dx",
                           font_size=34, color=C_BLUE)
        wave     = VGroup(wave_lbl, wave_eq).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        key = MathTex(r"E(t)\geq 0,\qquad E(t)=0\;\Longleftrightarrow\;u\equiv 0",
                      font_size=32, color=C_YELLOW)

        group = VGroup(heat, wave, key).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        group.next_to(hdr, DOWN, buff=0.6)

        self.play(FadeIn(heat))
        self.next_slide()
        self.play(FadeIn(wave))
        self.next_slide()
        self.play(Write(key), Create(self.boxed(key, color=C_YELLOW)))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 6 — Two-Step Strategy
    # ══════════════════════════════════════════════════════════════════════════
    def slide_06_two_step(self):
        hdr = self.slide_header("The Two-Step Strategy")
        self.play(Write(hdr))

        def step_card(num, title_str, line1_str, line2_mob, color):
            card = RoundedRectangle(corner_radius=0.2, width=11.5, height=2.0,
                                    color=color, fill_color=color, fill_opacity=0.10,
                                    stroke_width=2)
            header = VGroup(
                Text(f"Step {num}", font_size=24, weight=BOLD, color=color),
                Text(title_str,     font_size=24, weight=BOLD, color=color),
            ).arrange(RIGHT, buff=0.4)
            body_line1 = Text(line1_str, font_size=21, color=C_WHITE)
            content = VGroup(header, body_line1, line2_mob).arrange(
                DOWN, buff=0.18, aligned_edge=LEFT)
            content.move_to(card.get_center()).shift(LEFT * 0.2)
            return VGroup(card, content)

        s1 = step_card(
            1, "Energy Identity",
            "Multiply PDE by u (heat) or u_t (wave). Integrate over [0,L], apply IBP & BCs.",
            MathTex(r"\Rightarrow\;\text{obtain a formula for }E'(t)",
                    font_size=24, color=C_WHITE),
            C_BLUE,
        )
        s2 = step_card(
            2, "Apply Gronwall's Inequality",
            "The energy identity gives an ODE inequality:",
            MathTex(r"E'(t)\leq C\,E(t)\;\Rightarrow\;E(t)\leq E(0)\,e^{Ct}",
                    font_size=26, color=C_WHITE),
            C_GREEN,
        )

        arrow = Arrow(DOWN * 0.05, DOWN * 0.5, color=C_WHITE, buff=0, stroke_width=3)
        group = VGroup(s1, arrow, s2).arrange(DOWN, buff=0.22)
        group.next_to(hdr, DOWN, buff=0.45)

        self.play(Create(s1[0]), FadeIn(s1[1]))
        self.next_slide()
        self.play(GrowArrow(arrow))
        self.play(Create(s2[0]), FadeIn(s2[1]))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 7 — Uniqueness Flowchart
    # ══════════════════════════════════════════════════════════════════════════
    def slide_07_uniqueness_flow(self):
        hdr = self.slide_header("How Uniqueness Follows")
        self.play(Write(hdr))

        def fbox(txt, color, w=9, h=0.75):
            b = RoundedRectangle(corner_radius=0.15, width=w, height=h,
                                 color=color, fill_color=color, fill_opacity=0.15,
                                 stroke_width=2)
            lbl = Text(txt, font_size=22, color=color)
            lbl.move_to(b.get_center())
            return VGroup(b, lbl)

        def fbox_math(tex_str, color, w=9):
            b = RoundedRectangle(corner_radius=0.15, width=w, height=0.85,
                                 color=color, fill_color=color, fill_opacity=0.15,
                                 stroke_width=2)
            lbl = MathTex(tex_str, font_size=24, color=color)
            lbl.move_to(b.get_center())
            return VGroup(b, lbl)

        boxes = VGroup(
            fbox(r"Two solutions  u_1, u_2  satisfy the same IBVP", C_BLUE,   w=9.5),
            fbox(r"Define difference:  w = u_1 - u_2",              C_WHITE,  w=7),
            fbox(r"w satisfies homogeneous IBVP,  w(x,0) = 0",      C_YELLOW, w=9),
            fbox_math(r"E_w(t)\geq 0,\quad E_w'(t)\leq 0,\quad E_w(0)=0", C_ORANGE, w=8),
            fbox_math(r"\therefore\;E_w(t)=0\;\forall t\;\Rightarrow\;w\equiv 0\;\Rightarrow\;u_1=u_2\;\checkmark",
                      C_GREEN, w=10.5),
        ).arrange(DOWN, buff=0.22)

        arrows = VGroup(*[
            Arrow(boxes[i].get_bottom(), boxes[i + 1].get_top(),
                  buff=0.04, color=C_GRAY, stroke_width=2.5)
            for i in range(len(boxes) - 1)
        ])

        group = VGroup(boxes, arrows).next_to(hdr, DOWN, buff=0.45)

        for i in range(len(boxes)):
            self.play(FadeIn(boxes[i], shift=RIGHT * 0.2))
            if i < len(boxes) - 1:
                self.play(GrowArrow(arrows[i]))

        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 8 — Heat Equation (Dirichlet BCs)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_08_heat_equation(self):
        hdr = self.slide_header("Application 1: Heat Equation  (Dirichlet BCs)")
        self.play(Write(hdr))

        setup = VGroup(
            MathTex(r"u_t = k\,u_{xx}+f(x,t)", font_size=34, color=C_RED),
            MathTex(r"u(x,0)=\varphi(x),\quad u(0,t)=u(L,t)=0", font_size=30, color=C_WHITE),
        ).arrange(DOWN, buff=0.3).next_to(hdr, DOWN, buff=0.55)

        self.play(Write(setup))
        self.next_slide()

        deriv = VGroup(
            MathTex(r"E(t)=\tfrac{1}{2}\|u\|^2\quad\Longrightarrow\quad E'(t)=\int_0^L u\,u_t\,dx",
                    font_size=30, color=C_YELLOW),
            MathTex(r"=\int_0^L u\bigl(k\,u_{xx}+f\bigr)dx"
                    r"\;\xrightarrow{\text{IBP}}\;"
                    r"-k\|u_x\|^2+\langle u,f\rangle",
                    font_size=30),
        ).arrange(DOWN, buff=0.4).next_to(setup, DOWN, buff=0.5)

        for eq in deriv:
            self.play(Write(eq))
            self.wait(0.3)

        result = MathTex(r"\boxed{E'(t)=-k\|u_x\|^2+\langle u,f\rangle}",
                         font_size=34, color=C_GREEN)
        result.next_to(deriv, DOWN, buff=0.4)
        self.play(Write(result))

        note = VGroup(
            Text("−k‖uₓ‖²  ≤ 0 :  diffusion always dissipates energy", font_size=22, color=C_GRAY),
            Text("⟨u, f⟩    :  source can add/remove energy",           font_size=22, color=C_GRAY),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(result, DOWN, buff=0.3)
        self.next_slide()
        self.play(FadeIn(note))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 9 — Energy Decay (Heat)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_09_energy_decay(self):
        hdr = self.slide_header("Energy Decay — Heat Equation  (f = 0)")
        self.play(Write(hdr))

        poincare = MathTex(
            r"\text{Poincaré:}\quad \|u_x\|^2\geq\frac{\pi^2}{L^2}\|u\|^2"
            r"=\frac{2\pi^2}{L^2}E(t)",
            font_size=30, color=C_YELLOW,
        ).next_to(hdr, DOWN, buff=0.5)
        self.play(Write(poincare))

        ineq = MathTex(
            r"\Rightarrow\quad E'(t)\leq -\frac{2k\pi^2}{L^2}\,E(t)",
            font_size=34, color=C_RED,
        ).next_to(poincare, DOWN, buff=0.35)
        self.play(Write(ineq))
        self.next_slide()

        gronwall_res = MathTex(
            r"E(t)\leq E(0)\,e^{-2k\pi^2 t/L^2}",
            font_size=40, color=C_GREEN,
        ).next_to(ineq, DOWN, buff=0.4)
        box = self.boxed(gronwall_res, color=C_GREEN)
        self.play(Write(gronwall_res), Create(box))
        self.next_slide()

        # Plot
        ax = Axes(
            x_range=[0, 3, 1], y_range=[0, 1.1, 0.5],
            x_length=5.5, y_length=2.5,
            axis_config={"color": C_GRAY, "include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3],
                           "label_direction": DOWN},
            y_axis_config={"numbers_to_include": [0.5, 1.0]},
        ).next_to(gronwall_res, DOWN, buff=0.4)
        ax_labels = ax.get_axis_labels(
            x_label=MathTex("t", font_size=24),
            y_label=MathTex("E(t)", font_size=24),
        )
        curve = ax.plot(lambda t: np.exp(-1.5 * t), color=C_GREEN, stroke_width=3)
        lbl   = MathTex(r"e^{-2k\pi^2t/L^2}", font_size=20, color=C_GREEN)
        lbl.next_to(curve.point_from_proportion(0.2), UR, buff=0.1)

        self.play(Create(ax), Write(ax_labels))
        self.play(Create(curve), FadeIn(lbl))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 10 — Wave Equation
    # ══════════════════════════════════════════════════════════════════════════
    def slide_10_wave_equation(self):
        hdr = self.slide_header("Application 2: Wave Equation")
        self.play(Write(hdr))

        setup = VGroup(
            MathTex(r"u_{tt}=c^2u_{xx}+f(x,t)", font_size=34, color=C_BLUE),
            MathTex(r"u(x,0)=\varphi(x),\quad u_t(x,0)=\psi(x)", font_size=30),
            MathTex(r"u(0,t)=u(L,t)=0", font_size=30),
        ).arrange(DOWN, buff=0.3).next_to(hdr, DOWN, buff=0.5)
        self.play(Write(setup))
        self.next_slide()

        energy_def = MathTex(
            r"E(t)=\frac{1}{2}\int_0^L\!\bigl(u_t^2+c^2u_x^2\bigr)dx"
            r"\;\;(\text{kinetic}+\text{potential})",
            font_size=30, color=C_YELLOW,
        ).next_to(setup, DOWN, buff=0.45)
        self.play(Write(energy_def))
        self.next_slide()

        identity = MathTex(
            r"E'(t)=\langle u_t,\,f\rangle",
            font_size=36, color=C_GREEN,
        ).next_to(energy_def, DOWN, buff=0.4)
        self.play(Write(identity))

        conservation = MathTex(
            r"f=0\;\Rightarrow\;E'(t)=0\;\Rightarrow\;E(t)=E(0)\quad\text{(energy conserved!)}",
            font_size=30, color=C_BLUE,
        ).next_to(identity, DOWN, buff=0.3)
        box = self.boxed(conservation, color=C_BLUE)
        self.next_slide()
        self.play(Write(conservation), Create(box))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 11 — Comparison Plot
    # ══════════════════════════════════════════════════════════════════════════
    def slide_11_comparison(self):
        hdr = self.slide_header("Energy Behaviour: Comparison")
        self.play(Write(hdr))

        ax = Axes(
            x_range=[0, 4, 1], y_range=[0, 1.25, 0.5],
            x_length=8.5, y_length=4.5,
            axis_config={"color": C_GRAY, "include_tip": False},
            x_axis_config={"numbers_to_include": [1, 2, 3, 4]},
            y_axis_config={"numbers_to_include": [0.5, 1.0]},
        ).next_to(hdr, DOWN, buff=0.5)
        ax_labels = ax.get_axis_labels(
            x_label=MathTex("t", font_size=26),
            y_label=MathTex("E(t)", font_size=26),
        )

        heat_curve   = ax.plot(lambda t: np.exp(-1.5 * t), color=C_RED,    stroke_width=3)
        wave_curve   = ax.plot(lambda t: 1.0,              color=C_BLUE,   stroke_width=3)
        damped_curve = ax.plot(lambda t: np.exp(-0.45 * t),color=C_YELLOW, stroke_width=3)

        def legend_entry(color, text):
            seg = Line(ORIGIN, 0.55 * RIGHT, color=color, stroke_width=3)
            lbl = Text(text, font_size=21, color=color)
            return VGroup(seg, lbl).arrange(RIGHT, buff=0.2)

        legend = VGroup(
            legend_entry(C_RED,    "Heat eq.  (exponential decay)"),
            legend_entry(C_BLUE,   "Wave eq.  (conserved)"),
            legend_entry(C_YELLOW, "Damped wave  (non-increasing)"),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_corner(DR, buff=0.6)

        self.play(Create(ax), Write(ax_labels))
        self.play(Create(heat_curve),   FadeIn(legend[0]))
        self.wait(0.2)
        self.play(Create(wave_curve),   FadeIn(legend[1]))
        self.wait(0.2)
        self.play(Create(damped_curve), FadeIn(legend[2]))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 12 — Damped Wave (Worked Example)
    # ══════════════════════════════════════════════════════════════════════════
    def slide_12_damped_wave(self):
        hdr = self.slide_header("Worked Example: Damped Wave Equation")
        self.play(Write(hdr))

        pde = MathTex(r"u_{tt}+2\gamma u_t=c^2 u_{xx},\quad\gamma>0",
                      font_size=34, color=C_ORANGE)
        pde.next_to(hdr, DOWN, buff=0.55)
        self.play(Write(pde))
        self.next_slide()

        step1 = Text("Multiply PDE by uₜ and integrate:", font_size=24, color=C_GRAY)
        eq1 = MathTex(r"E'(t)=\int_0^L u_t\bigl(u_{tt}-c^2u_{xx}\bigr)dx"
                      r"=\int_0^L u_t(-2\gamma u_t)\,dx",
                      font_size=28)
        eq2 = MathTex(r"E'(t)=-2\gamma\|u_t\|^2\;\leq\;0",
                      font_size=38, color=C_GREEN)

        deriv = VGroup(step1, eq1, eq2).arrange(DOWN, buff=0.4).next_to(pde, DOWN, buff=0.4)
        box = self.boxed(eq2, color=C_GREEN)

        for item in deriv:
            self.play(Write(item))
            self.wait(0.2)
        self.play(Create(box))
        self.next_slide()

        uniqueness = MathTex(
            r"\because\;E_w(0)=0,\;E_w'(t)\leq 0"
            r"\;\Rightarrow\;E_w(t)=0\;\Rightarrow\;w\equiv 0\quad\checkmark\;\text{Uniqueness}",
            font_size=26, color=C_YELLOW,
        ).next_to(deriv, DOWN, buff=0.4)
        self.play(FadeIn(uniqueness, shift=UP * 0.2))
        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 13 — Strengths & Limitations
    # ══════════════════════════════════════════════════════════════════════════
    def slide_13_strengths_limits(self):
        hdr = self.slide_header("Strengths & Limitations")
        self.play(Write(hdr))

        strengths = VGroup(
            Text("Strengths", font_size=28, weight=BOLD, color=C_GREEN),
            self.bullet("No explicit solution needed",             color=C_WHITE),
            self.bullet("Works for linear & many nonlinear PDEs", color=C_WHITE),
            self.bullet("Quantitative stability bounds",           color=C_WHITE),
            self.bullet("Mirrors physical energy - intuitive",    color=C_WHITE),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)

        limits = VGroup(
            Text("Limitations", font_size=28, weight=BOLD, color=C_RED),
            self.bullet("L2 control only - no pointwise info",    color=C_WHITE),
            self.bullet("Nonlinear PDEs are harder to handle",    color=C_WHITE),
            self.bullet("Does not prove existence",               color=C_WHITE),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)

        cols = VGroup(strengths, limits).arrange(RIGHT, buff=1.4, aligned_edge=UP)
        cols.next_to(hdr, DOWN, buff=0.6)

        # Divider
        div = DashedLine(cols.get_top(), cols.get_bottom(), color=C_GRAY,
                         dash_length=0.15, stroke_width=1)
        div.move_to(cols.get_center())

        self.play(FadeIn(strengths[0]))
        for item in strengths[1:]:
            self.play(FadeIn(item, shift=RIGHT * 0.2))

        self.play(Create(div))

        self.play(FadeIn(limits[0]))
        for item in limits[1:]:
            self.play(FadeIn(item, shift=RIGHT * 0.2))

        self.next_slide()
        self.clear()

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 14 — Conclusion
    # ══════════════════════════════════════════════════════════════════════════
    def slide_14_conclusion(self):
        hdr = self.slide_header("Conclusion")
        self.play(Write(hdr))

        points = VGroup(
            MathTex(r"\bullet\;\text{Energy method: assign }E(t)\geq 0,"
                    r"\text{ derive }E'(t)\leq CE(t),\text{ apply Gronwall}",
                    font_size=28),
            MathTex(r"\bullet\;\text{Heat eq.: }E(t)\to 0"
                    r"\quad\text{(diffusion is dissipative)}",
                    font_size=28, color=C_RED),
            MathTex(r"\bullet\;\text{Wave eq.: }E(t)=E(0)"
                    r"\quad\text{(energy is conserved)}",
                    font_size=28, color=C_BLUE),
            MathTex(r"\bullet\;\text{Damped wave: }E'(t)=-2\gamma\|u_t\|^2\leq 0"
                    r"\quad\text{(dissipative)}",
                    font_size=28, color=C_YELLOW),
            MathTex(r"\bullet\;\text{Uniqueness: }E_w(0)=0,\;E_w'(t)\leq 0"
                    r"\;\Rightarrow\;w\equiv 0",
                    font_size=28, color=C_GREEN),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).next_to(hdr, DOWN, buff=0.55)

        for p in points:
            self.play(FadeIn(p, shift=UP * 0.1))
            self.wait(0.1)

        self.next_slide()
        self.clear()

        # ── Thank-you ──
        big = Text("Thank You!", font_size=64, weight=BOLD, color=C_BLUE)
        sub = Text("Questions?", font_size=34, color=C_GRAY)
        VGroup(big, sub).arrange(DOWN, buff=0.4)
        self.play(Write(big))
        self.play(FadeIn(sub))
        self.wait(1)
        self.next_slide()