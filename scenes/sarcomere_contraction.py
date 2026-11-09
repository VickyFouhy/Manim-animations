"""Sarcomere_Contraction

Converted from notebooks/sarcomere-contraction.ipynb (code unchanged apart from removing the notebook-only lines).

Render (from the repo folder, in the manim-env environment):
    python -m manim -ql scenes/sarcomere_contraction.py Sarcomere_Contraction     # quick preview (480p)
    python -m manim -qh scenes/sarcomere_contraction.py Sarcomere_Contraction     # final video (1080p)
"""
from manim import *
from pathlib import Path

# Optional arm images live in scenes/assets/ (not included in the repo)
ASSETS = Path(__file__).resolve().parent / "assets"

class Sarcomere_Contraction(Scene):
    def construct(self):
        spacing_y = 0.6
        actin_len = 2.5   # shorter for sliding
        gap = 4.0

        # --- Actin (blue) ---
        base_actin = Rectangle(height=0.15, width=actin_len).set_fill("#00D5FF", 0.8).set_stroke("#00D5FF", 2)
        actin_left = VGroup(base_actin.copy().shift(UP*spacing_y),
                            base_actin.copy(),
                            base_actin.copy().shift(DOWN*spacing_y)).shift(LEFT*gap/2)
        actin_right = VGroup(base_actin.copy().shift(UP*spacing_y),
                             base_actin.copy(),
                             base_actin.copy().shift(DOWN*spacing_y)).shift(RIGHT*gap/2)
        actins = VGroup(actin_left, actin_right)

        # --- Myosin (red, thick) ---
        base_myosin = Rectangle(height=0.25, width=4).set_fill("#8F5AFF", 0.8).set_stroke("#8F5AFF", 2)
        myosin = VGroup(base_myosin.copy().shift(UP*0.3),
                        base_myosin.copy().shift(DOWN*0.3))

        # --- Top labels (left side) ---
        actin_label  = Text("Actin").set_color("#00D5FF").scale(0.6)
        myosin_label = Text("Myosin").set_color("#8F5AFF").scale(0.6)
        labels_left = VGroup(actin_label, myosin_label).arrange(DOWN, buff=0.3)
        labels_left.next_to(VGroup(actins, myosin), LEFT, buff=1.0)

        # Stage labels (relaxed / contracted)
        relaxed_label = Text("Relaxed").set_color(WHITE).scale(0.6)
        contracting_label = Text("Contracting").set_color(WHITE).scale(0.6)
        contracted_label = Text("Contracted").set_color(WHITE).scale(0.6)

        for lbl in (relaxed_label, contracting_label, contracted_label):
            lbl.move_to(labels_left.get_center())

        # --- "Changes" bullet points (start hidden) ---
        changes = VGroup(
            Text("• Z lines move closer").scale(0.4),
            Text("• I band shortens").scale(0.4),
            Text("• H zone shortens").scale(0.4),
            Text("• A band unchanged").scale(0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        changes.next_to(VGroup(actins, myosin), RIGHT, buff=0.6)
        changes.align_to(VGroup(actins, myosin), UP)

        # --- Dynamic height reference ---
        z_height = (actins.get_top()[1] - actins.get_bottom()[1]) + 0.6

        # --- M line (center of sarcomere, vertical, through myosin) ---
        m_line = Line(
            UP * z_height/2,
            DOWN * z_height/2
        ).set_stroke(GREY_B, 4).move_to([myosin.get_center()[0], 0, 0])

        m_line_label = Text("M line").scale(0.4).set_color(GREY_B).next_to(m_line, DOWN, buff=0.8)

        # --- Dynamic Z-lines ---
        z_left = always_redraw(lambda:
            Line(UP*z_height/2, DOWN*z_height/2).set_stroke(GREY_B, 4).move_to([actin_left.get_left()[0], 0, 0])
        )
        z_right = always_redraw(lambda:
            Line(UP*z_height/2, DOWN*z_height/2).set_stroke(GREY_B, 4).move_to([actin_right.get_right()[0], 0, 0])
        )

        z_left_label  = always_redraw(lambda:
            Text("Z line").scale(0.4).set_color(GREY_B).next_to(z_left, DOWN, buff=0.3)
        )
        z_right_label = always_redraw(lambda:
            Text("Z line").scale(0.4).set_color(GREY_B).next_to(z_right, DOWN, buff=0.3)
        )

        # --- I band (myosin edges) ---
        i_left_boundary = always_redraw(lambda:
            Line(UP*z_height/2, DOWN*z_height/2).set_stroke(WHITE, 2).move_to([myosin.get_left()[0], 0, 0])
        )
        i_right_boundary = always_redraw(lambda:
            Line(UP*z_height/2, DOWN*z_height/2).set_stroke(WHITE, 2).move_to([myosin.get_right()[0], 0, 0])
        )

        I_left_arrow = always_redraw(lambda:
            DoubleArrow(start=z_left.get_center(), end=i_left_boundary.get_center(),
                        buff=0, stroke_width=0.8, color=WHITE, tip_length=0.15).shift(UP*1.0)
        )
        I_right_arrow = always_redraw(lambda:
            DoubleArrow(start=i_right_boundary.get_center(), end=z_right.get_center(),
                        buff=0, stroke_width=0.8, color=WHITE, tip_length=0.15).shift(UP*1.0)
        )
        I_left_label = always_redraw(lambda:
            Text("I band").scale(0.4).set_color(WHITE).next_to(I_left_arrow, UP, buff=0.1)
        )
        I_right_label = always_redraw(lambda:
            Text("I band").scale(0.4).set_color(WHITE).next_to(I_right_arrow, UP, buff=0.1)
        )

        # --- A band (span of myosin) ---
        A_arrow = always_redraw(lambda:
            DoubleArrow(start=i_left_boundary.get_center(), end=i_right_boundary.get_center(),
                        buff=0, stroke_width=0.8, color=WHITE, tip_length=0.15).shift(UP*1.3)
        )
        A_label = always_redraw(lambda:
            Text("A band").scale(0.4).set_color(WHITE).next_to(A_arrow, UP, buff=0.1)
        )

        # --- H zone (inner actin tips) ---
        h_left_boundary = always_redraw(lambda:
            Line(UP*z_height/2, DOWN*z_height/2).set_stroke(WHITE, 2).move_to([actin_left[1].get_right()[0], 0, 0])
        )
        h_right_boundary = always_redraw(lambda:
            Line(UP*z_height/2, DOWN*z_height/2).set_stroke(WHITE, 2).move_to([actin_right[1].get_left()[0], 0, 0])
        )

        H_arrow = always_redraw(lambda:
            DoubleArrow(start=h_left_boundary.get_center(), end=h_right_boundary.get_center(),
                        buff=0, stroke_width=0.8, color=WHITE, tip_length=0.15).shift(DOWN*1.0)
        )
        H_label = always_redraw(lambda:
            Text("H zone").scale(0.4).set_color(WHITE).next_to(H_arrow, DOWN, buff=0.1)
        )

        # --- build relaxed state in order ---
        self.play(Create(actins))
        self.play(Write(actin_label))
        self.wait(0.5)

        self.play(Create(myosin))
        self.play(Write(myosin_label))
        self.wait(0.5)

        # show M line after myosin so it clearly sits in the middle
        self.play(Create(m_line), Write(m_line_label))
        self.wait(0.5)
        self.play(FadeOut(m_line_label), FadeOut(m_line))

        self.play(Create(z_left), Create(z_right))
        self.play(Write(z_left_label), Write(z_right_label))
        self.wait(1)

        # I band first (lines → arrows/labels)
        self.play(Create(i_left_boundary), Create(i_right_boundary))
        self.play(Create(I_left_arrow), Create(I_right_arrow))
        self.play(Write(I_left_label), Write(I_right_label))
        self.wait(1)

        # Then A band
        self.play(Create(A_arrow), Write(A_label))
        self.wait(1)

        # Then H zone (lines → arrow/label)
        self.play(Create(h_left_boundary), Create(h_right_boundary))
        self.play(Create(H_arrow), Write(H_label))

        self.wait(2)
        # Remove actin/myosin labels, add "Relaxed"
        self.play(FadeOut(labels_left), FadeIn(relaxed_label))
        self.wait(1.5)  # hold relaxed state

        # =========================
        #   BICEP PNGs (fixed)
        # =========================
        path_relaxed    = ASSETS / "arm_s.png"
        path_contracted = ASSETS / "arm_f.png"
        # If the arm images aren't there, the arm is skipped
        show_arm = path_relaxed.exists() and path_contracted.exists()

        if show_arm:
            bicep_relaxed    = ImageMobject(str(path_relaxed))
            bicep_contracted = ImageMobject(str(path_contracted))

            bicep_relaxed.set_height(2.8)
            bicep_contracted.set_height(2.8)

            anchor = VGroup(actins, myosin)
            bicep_relaxed.next_to(anchor, DOWN, buff=0.3)
            bicep_contracted.move_to(bicep_relaxed)

            bicep_relaxed.set_z_index(10)
            bicep_contracted.set_z_index(10)

            self.play(FadeIn(bicep_relaxed))
            self.wait(0.5)

        # --- Contraction calculation ---
        desired_gap = 0.5  # target gap between inner actin tips
        inner_left_x  = actin_left[1].get_right()[0]
        inner_right_x = actin_right[1].get_left()[0]
        current_gap   = inner_right_x - inner_left_x
        shift = max(0, (current_gap - desired_gap) / 2)

        # Swap stage label to "Contracting"
        self.play(FadeOut(relaxed_label), FadeIn(contracting_label))

        # Animate contraction + swap bicep image
        arm_swap = [ReplacementTransform(bicep_relaxed, bicep_contracted)] if show_arm else []
        self.play(
            actin_left.animate.shift(RIGHT*shift),
            actin_right.animate.shift(LEFT*shift),
            *arm_swap,
            run_time=5, rate_func=linear
        )

        # Swap stage label to "Contracted"
        self.play(FadeOut(contracting_label), FadeIn(contracted_label))
        self.wait(1.0)

        # 1) Z lines move closer
        self.play(
            Write(changes[0]),
            Circumscribe(z_left, color=WHITE, fade_out=True, time_width=5.0),
            Circumscribe(z_right, color=WHITE, fade_out=True, time_width=5.0),
        )
        self.wait(0.8)

        # 2) I band shortens
        self.play(
            Write(changes[1]),
            Circumscribe(I_left_label, color=WHITE, fade_out=True, time_width=5.0),
            Circumscribe(I_right_label, color=WHITE, fade_out=True, time_width=5.0),
        )
        self.wait(0.8)

        # 3) H zone shortens
        self.play(
            Write(changes[2]),
            Circumscribe(H_label, color=WHITE, fade_out=True, time_width=5.0),
        )
        self.wait(0.8)

        # 4) A band unchanged
        self.play(
            Write(changes[3]),
            Circumscribe(A_label, color=WHITE, fade_out=True, time_width=5.0),
        )
        self.wait(1.5)
