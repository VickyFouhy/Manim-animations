"""TranslocationTwoExamplesAnimatedOnly

Converted from notebooks/mutations-duplication-inversion-translocation.ipynb (code unchanged apart from removing the notebook-only lines).

Render (from the repo folder, in the manim-env environment):
    python -m manim -ql scenes/mutation_translocation.py TranslocationTwoExamplesAnimatedOnly     # quick preview (480p)
    python -m manim -qh scenes/mutation_translocation.py TranslocationTwoExamplesAnimatedOnly     # final video (1080p)
"""
from manim import *

class TranslocationTwoExamplesAnimatedOnly(Scene):
    def construct(self):
        # ==================================================
        # Helpers
        # ==================================================
        def make_chr(color, height):
            body = RoundedRectangle(
                width=0.7,
                height=height,
                corner_radius=0.35
            )
            body.set_fill(color, opacity=0.8)
            body.set_stroke(WHITE, width=1)

            # Centromere (black band)
            centromere = Rectangle(
                width=0.75,
                height=0.12
            )
            centromere.set_fill(BLACK, opacity=1)
            centromere.set_stroke(BLACK, width=0)
            centromere.move_to(body.get_center())

            return VGroup(body, centromere)

        def make_segment(color, label_text, height=1.05):
            seg = RoundedRectangle(width=0.78, height=height, corner_radius=0.18)
            seg.set_fill(color, opacity=0.25)
            seg.set_stroke(color, width=3)
            lab = Text(label_text, font_size=24).move_to(seg.get_center())
            return seg, lab

        def box_around(mobj, color):
            return SurroundingRectangle(mobj, buff=0.12, corner_radius=0.14).set_stroke(color, 3)

        # ==================================================
        # Example 1: Non-reciprocal
        # ==================================================
        header1 = Text("Example 1: Translocation (non-reciprocal)", font_size=34).to_edge(UP)
        self.play(FadeIn(header1))
        self.wait(0.2)

        chr1 = make_chr(BLUE_E, 4.6).move_to(LEFT*2.2)
        chr2 = make_chr(ORANGE, 3.2).move_to(RIGHT*2.2)

        self.play(FadeIn(chr1), FadeIn(chr2), run_time=1.0)
        self.wait(0.3)

        segA, labA = make_segment(RED, "A")
        segA.move_to(chr1.get_center() + DOWN*0.9)
        labA.move_to(segA.get_center())
        boxA = box_around(segA, RED)

        self.play(FadeIn(segA), FadeIn(labA), FadeIn(boxA), run_time=0.8)
        self.wait(0.25)

        destA = chr2.get_center() + DOWN*0.8

        arrowA = CurvedArrow(
            segA.get_center() + RIGHT*0.4,
            destA + LEFT*0.4,
            angle=-PI/3,
            stroke_width=4
        )
        self.play(Create(arrowA))
        self.wait(0.25)

        chr1_short = make_chr(BLUE_E, 3.2).move_to(chr1.get_center())
        chr2_long  = make_chr(ORANGE, 4.6).move_to(chr2.get_center())

        self.play(
            segA.animate.move_to(destA),
            labA.animate.move_to(destA),
            boxA.animate.move_to(destA),
            FadeOut(arrowA),
            ReplacementTransform(chr1, chr1_short),
            ReplacementTransform(chr2, chr2_long),
            run_time=1.8
        )
        chr1, chr2 = chr1_short, chr2_long

        self.play(Flash(destA, flash_radius=0.4, line_length=0.2), run_time=0.5)

        note1 = Text(
            "Non-reciprocal: one chromosome loses DNA, the other gains DNA",
            font_size=24
        ).to_edge(DOWN)
        self.play(FadeIn(note1, shift=UP*0.1))
        self.wait(1.4)
        self.play(FadeOut(note1))

        self.play(
            FadeOut(chr1), FadeOut(chr2),
            FadeOut(segA), FadeOut(labA), FadeOut(boxA),
            FadeOut(header1),
            run_time=0.8
        )

        # ==================================================
        # Example 2: Reciprocal
        # ==================================================
        header2 = Text("Example 2: Translocation (reciprocal)", font_size=34).to_edge(UP)
        self.play(FadeIn(header2))
        self.wait(0.2)

        chr1 = make_chr(BLUE_E, 4.9).move_to(LEFT*2.2)
        chr2 = make_chr(ORANGE, 3.3).move_to(RIGHT*2.2)

        self.play(FadeIn(chr1), FadeIn(chr2), run_time=1.0)
        self.wait(0.3)

        segA, labA = make_segment(RED, "A")
        segB, labB = make_segment(YELLOW, "B")

        segA.move_to(chr1.get_center() + DOWN*1.1)
        labA.move_to(segA.get_center())
        boxA = box_around(segA, RED)

        segB.move_to(chr2.get_center() + UP*0.6)
        labB.move_to(segB.get_center())
        boxB = box_around(segB, YELLOW)

        self.play(
            FadeIn(segA), FadeIn(labA), FadeIn(boxA),
            FadeIn(segB), FadeIn(labB), FadeIn(boxB),
            run_time=1.0
        )
        self.wait(0.3)

        destA = segB.get_center()
        destB = segA.get_center()

        arrowA = CurvedArrow(segA.get_center() + RIGHT*0.4, destA + LEFT*0.4, angle=-PI/2.6, stroke_width=4)
        arrowB = CurvedArrow(segB.get_center() + LEFT*0.4,  destB + RIGHT*0.4, angle=PI/2.6, stroke_width=4)

        self.play(Create(arrowA), Create(arrowB))
        self.wait(0.25)

        self.play(
            segA.animate.move_to(destA),
            labA.animate.move_to(destA),
            boxA.animate.move_to(destA),
            segB.animate.move_to(destB),
            labB.animate.move_to(destB),
            boxB.animate.move_to(destB),
            FadeOut(arrowA),
            FadeOut(arrowB),
            run_time=1.8
        )

        self.play(
            Flash(destA, flash_radius=0.35, line_length=0.2),
            Flash(destB, flash_radius=0.35, line_length=0.2),
            run_time=0.6
        )

        note2 = Text(
            "Reciprocal: segments swap (no net gain or loss of DNA)",
            font_size=24
        ).to_edge(DOWN)
        self.play(FadeIn(note2, shift=UP*0.1))
        self.wait(3.0)
        self.play(FadeOut(note2))

        self.wait(0.3)
