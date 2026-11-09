"""Synapse_Receptors_DownAP_SR_Sized_WithSarcomereRight_Anim

Converted from notebooks/synapse-neuromuscular-junction.ipynb. Since then, an acetylcholinesterase step
has been added (ACh hydrolysed, clearing the receptors), and the pre-synaptic cell redrawn as an axon
ending in a synaptic knob, with Ca²⁺ channels on the lower sides of the knob.

Render (from the repo folder, in the manim-env environment):
    python -m manim -ql scenes/synapse_neuromuscular_junction.py Synapse_Receptors_DownAP_SR_Sized_WithSarcomereRight_Anim     # quick preview (480p)
    python -m manim -qh scenes/synapse_neuromuscular_junction.py Synapse_Receptors_DownAP_SR_Sized_WithSarcomereRight_Anim     # final video (1080p)
"""
from manim import *
import numpy as np
import textwrap
from manim.utils.space_ops import normalize

Text.set_default(font="Helvetica Neue")

# =========================
# PALETTE (colors)
# =========================
PRE_FILL, PRE_STROKE     = "#5EB7B4", "#5EB7B4"
POST_FILL, POST_STROKE   = "#0000FF", "#0000FF"
REC_COLOR                = "#00BFFF"
VES_COLOR, NT_COLOR      = "##4297A0", "#FFFF00"
BOLT_COLOR               = "#FFFFFF"
AP_ARROW_COLOR           = "#FFFFFF"
SR_FILL, SR_STROKE       = "#7ED957", "#FFFFFF"
CA_COLOR                 = "#FF00FF"
TEXT_COLOR               = WHITE   # labels, captions and pointers outside the cells
CHANNEL_COLOR            = WHITE
STEP_HOLD                = 1.0     # seconds each caption shows before its step animates

# Inset SARCOMERE colors
SM_ACTIN_COLOR           = "#00D5FF"
SM_MYOSIN_COLOR          = "#8F5AFF"

# =========================
# SIZES / KNOBS
# =========================
#STEP_PAUSE = 1.0  # seconds to pause before each new step label
DIAGRAM_SCALE     = 0.80
DIAGRAM_SHIFT_X   = -1.4
DIAGRAM_SHIFT_Y   = +0.60
CLEFT_SIZE        = 1.15

POST_WIDTH        = 12.0
POST_HEIGHT       = 3.4

RECEPTOR_WIDTH    = 0.5
RECEPTOR_BASE_H   = 0.06

VESICLE_RADIUS    = 0.5
NT_DOT_R          = 0.09
NT_PER_VESICLE    = 5

SARCO_FONT        = 24
AP_FONT           = 25

PRE_AP_LEN        = 0.80
PRE_AP_TIP        = 0.18
PRE_AP_STROKE     = 3

# SR size
SR_WIDTH, SR_HEIGHT = 2.4, 0.45
CA_SR_R, CA_SR_COUNT= 0.06, 1   # single Ca2+ dot

# Sarcomere
SM_SCALE          = 1.30
SM_ACTIN_LEN      = 1.20
SM_ACTIN_THICK    = 0.10
SM_MYOSIN_LEN     = 1.60
SM_MYOSIN_THICK   = 0.18
SM_ROWS_SPACING   = 0.25
SM_GAP            = 1.80
SM_CONTRACT_TO    = 0.22
SM_CONTRACT_TIME  = 1.2
SM_LABEL_FONT     = 24
SM_LABEL_COLOR    = "#FFFFFF"
CA_PULSE_SCALE    = 1.35
TO_SM_TIP, TO_SM_STROKE = 0.22, 3

CHANNEL_BAR_W, CHANNEL_BAR_H = 0.10, 0.40

# Synaptic knob outline: (x, height above the knob's bottom), with the axon running off the top
KNOB_OUTLINE = [
    (-1.0, 4.8), (-1.0, 3.4), (-2.3, 2.3), (-3.8, 1.3), (-3.9, 0.4), (-3.0, 0.05), (0, 0),
    (3.0, 0.05), (3.9, 0.4), (3.8, 1.3), (2.3, 2.3), (1.0, 3.4), (1.0, 4.8),
]
CA_CHANNEL_HEIGHTS = (0.55, 1.05)   # two Ca2+ channels on each side of the knob
VESICLE_HEIGHT     = 1.0

# =========================
# Helpers
# =========================
def filled_receptor_on_top(x, top_y, width=RECEPTOR_WIDTH, base_h=RECEPTOR_BASE_H, color=REC_COLOR):
    base = Rectangle(width=width, height=base_h, color=color, fill_color=color, fill_opacity=1.0)
    base.move_to([x, top_y - base_h/2, 0])
    r = width/2
    cap = AnnularSector(
        arc_center=[x, top_y, 0],
        inner_radius=0.0, outer_radius=r,
        start_angle=PI, angle=PI,
        color=color, fill_color=color, fill_opacity=1.0, stroke_width=4
    )
    return VGroup(base, cap).set_z_index(15)

def make_mini_sarcomere():
    base_actin = Rectangle(height=SM_ACTIN_THICK, width=SM_ACTIN_LEN)\
                    .set_fill(SM_ACTIN_COLOR, 0.85).set_stroke(SM_ACTIN_COLOR, 1.5)
    actin_left = VGroup(base_actin.copy().shift(UP*SM_ROWS_SPACING),
                        base_actin.copy(),
                        base_actin.copy().shift(DOWN*SM_ROWS_SPACING)).shift(LEFT*SM_GAP/2)
    actin_right= VGroup(base_actin.copy().shift(UP*SM_ROWS_SPACING),
                        base_actin.copy(),
                        base_actin.copy().shift(DOWN*SM_ROWS_SPACING)).shift(RIGHT*SM_GAP/2)
    base_myosin= Rectangle(height=SM_MYOSIN_THICK, width=SM_MYOSIN_LEN)\
                    .set_fill(SM_MYOSIN_COLOR, 0.85).set_stroke(SM_MYOSIN_COLOR, 1.5)
    myosin = VGroup(base_myosin.copy().shift(UP*0.22),
                    base_myosin.copy().shift(DOWN*0.22))
    g = VGroup(actin_left, actin_right, myosin).scale(SM_SCALE)
    return g, actin_left, actin_right

def make_knob(bottom):
    knob = VMobject(fill_color=PRE_FILL, fill_opacity=1.0, stroke_color=PRE_STROKE, stroke_width=5)
    knob.set_points_smoothly([bottom + np.array([x, y, 0]) for x, y in KNOB_OUTLINE])
    return knob

def point_on_knob(knob, side, y, samples=600):
    """Point on the knob's outline at height y on one side (-1 left, +1 right), and the outline's direction there."""
    pts = [knob.point_from_proportion(a) for a in np.linspace(0, 1, samples)]
    mid_x = knob.get_center()[0]
    i = min((k for k in range(samples) if np.sign(pts[k][0] - mid_x) == side), key=lambda k: abs(pts[k][1] - y))
    return pts[i], pts[min(i + 1, samples - 1)] - pts[max(i - 1, 0)]

def make_ca_channel(point, direction, color=None):
    color = color or CHANNEL_COLOR
    bars = VGroup(*[Rectangle(width=CHANNEL_BAR_W, height=CHANNEL_BAR_H, color=color, fill_color=color,
                              fill_opacity=1.0, stroke_width=0).shift(RIGHT*dx) for dx in (-0.09, 0.09)])
    return bars.rotate(np.arctan2(direction[1], direction[0])).move_to(point).set_z_index(20)

def drift(A, B, curve_down=0.40, jitter_x=0.26):
    A = np.array(A); B = np.array(B)
    mid = 0.5*(A+B) + DOWN*curve_down + RIGHT*np.random.uniform(-jitter_x, jitter_x)
    return VMobject().set_points_smoothly([A, mid, B])

def label_with_pointer(self, text, target_mobj, run_time=0.7, buff=0.28, offset=ORIGIN):
    lab = Text(text, font_size=26).set_color(TEXT_COLOR).set_z_index(85)
    lab.next_to(target_mobj, RIGHT, buff=buff).shift(offset)
    start = lab.get_left(); end = target_mobj.get_right()
    pointer = Arrow(start, end, buff=0.0, tip_length=0.16, color=TEXT_COLOR).set_stroke(width=3).set_z_index(86)
    self.play(FadeIn(lab), GrowArrow(pointer), run_time=run_time*0.7)
    self.wait(0.15)
    self.end_step()
    self.play(FadeOut(lab), FadeOut(pointer), run_time=0.3)

def step_label(self, text, rt_in=0.2, hold=None, y_shift=2.6, width=26):
    hold = STEP_HOLD if hold is None else hold
    wrapped = textwrap.fill(text, width=width)
    lab = Text(wrapped, font_size=26, line_spacing=0.8).set_color(TEXT_COLOR).set_z_index(80)

    frame_width  = config.frame_width
    frame_height = config.frame_height

    COLUMN_LEFT_X =  frame_width/2 - 4.5
    TOP_Y         =  frame_height/2 - 0.9

    max_width = frame_width/2 - 0.4 - COLUMN_LEFT_X   # keep long captions on screen
    if lab.width > max_width:
        lab.scale_to_fit_width(max_width)

    dx = COLUMN_LEFT_X - lab.get_left()[0]
    dy = TOP_Y         - lab.get_top()[1]
    lab.shift(RIGHT*dx + UP*dy)

    # Fade the text in
    self.play(FadeIn(lab), run_time=rt_in)

    # Keep it on screen for a bit
    self.wait(hold)

    return lab

# Scene
# =========================
class Synapse_Receptors_DownAP_SR_Sized_WithSarcomereRight_Anim(Scene):
    def end_step(self):
        """End of a step, before its caption fades. Does nothing here; the slides version pauses for a click."""

    def construct(self):
        rng = np.random.default_rng(7)

        # Base shapes: synaptic knob (end of the motor neurone's axon) above the muscle cell.
        # knob_box is the knob's footprint (never shown), used to lay things out.
        knob_box = Rectangle(width=7.8, height=3.2).to_edge(UP, buff=1.0)
        pre = make_knob(knob_box.get_bottom()).set_z_index(5)
        post = RoundedRectangle(width=POST_WIDTH, height=POST_HEIGHT, corner_radius=1.0,
                                fill_color=POST_FILL, fill_opacity=1.0,
                                color=POST_STROKE).set_stroke(width=5).set_z_index(5)
        post.to_edge(DOWN, buff=0.8)
        post.shift(DOWN * (post.get_top()[1] - (knob_box.get_bottom()[1] - CLEFT_SIZE)))

        # Receptors
        top_y = post.get_top()[1]
        rec_xs = np.linspace(post.get_left()[0] + 1.0, post.get_right()[0] - 1.0, 6)
        receptors = VGroup(*[filled_receptor_on_top(x, top_y) for x in rec_xs])

        # Calcium channels (2 on each lower side of the knob, across the membrane)
        knob_bottom = knob_box.get_bottom()
        channels = VGroup(*[make_ca_channel(*point_on_knob(pre, side, knob_bottom[1] + h))
                            for side in (-1, 1) for h in CA_CHANNEL_HEIGHTS])

        # Vesicles + NT dots
        fuse_xs = [-1.6, -0.3, 1.0, 2.2]
        vesicles, ves_contents = VGroup(), []
        for x in fuse_xs:
            v = Circle(radius=VESICLE_RADIUS, color=VES_COLOR, fill_color=VES_COLOR, fill_opacity=0.25)
            v.move_to([knob_bottom[0] + x, knob_bottom[1] + VESICLE_HEIGHT, 0]).set_z_index(12)
            vesicles.add(v)
            dots = VGroup(*[
                Dot(radius=NT_DOT_R, color=NT_COLOR).move_to(
                    v.get_center()
                    + RIGHT*rng.uniform(-VESICLE_RADIUS*0.45, VESICLE_RADIUS*0.45)
                    + UP   *rng.uniform(-VESICLE_RADIUS*0.45, VESICLE_RADIUS*0.45)
                ).set_z_index(11)
                for _ in range(NT_PER_VESICLE)
            ])
            ves_contents.append(dots)

        # Layout & shift (scale about the knob + muscle cell, so the axon running off the top doesn't move things)
        diagram = VGroup(pre, post, receptors, channels, vesicles, *ves_contents)
        about = VGroup(knob_box, post).get_center()
        for m in (diagram, knob_box):
            m.scale(DIAGRAM_SCALE, about_point=about).shift(RIGHT*DIAGRAM_SHIFT_X + UP*DIAGRAM_SHIFT_Y)
        knob_mid = knob_box.get_center()
        self.play(FadeIn(diagram))

        # ===== NEW INTRO CELL LABELS (in front) =====
        pre_cell_label = Text("Pre-synaptic cell\n(motor neurone)", font_size=26).set_color(TEXT_COLOR).set_z_index(85)
        pre_cell_label.next_to(knob_box, RIGHT, buff=0.9).align_to(knob_box, UP)
        pre_cell_target = point_on_knob(pre, 1, pre_cell_label.get_center()[1])[0]
        pre_cell_pointer = Arrow(pre_cell_label.get_left(), pre_cell_target, buff=0.06,
                                 tip_length=0.14, color=TEXT_COLOR).set_stroke(width=3).set_z_index(86)
        self.play(FadeIn(pre_cell_label), GrowArrow(pre_cell_pointer), run_time=0.5)
        self.wait(0.8)
        self.end_step()
        self.play(FadeOut(pre_cell_label), FadeOut(pre_cell_pointer), run_time=0.3)

        post_cell_label = Text("Post-synaptic cell\n(muscle cell)", font_size=26).set_color(TEXT_COLOR).set_z_index(85)
        post_cell_label.next_to(post, RIGHT, buff=0.5).align_to(post, DOWN)
        post_cell_pointer = Arrow(post_cell_label.get_left(), post.get_right(), buff=0.06,
                                  tip_length=0.14, color=TEXT_COLOR).set_stroke(width=3).set_z_index(86)
        self.play(FadeIn(post_cell_label), GrowArrow(post_cell_pointer), run_time=0.5)
        self.wait(0.8)
        self.end_step()
        self.play(FadeOut(post_cell_label), FadeOut(post_cell_pointer), run_time=0.3)

        # ===== INTRO LABELS (in front) =====
        sarco_label = Text("Sarcolemma", font_size=26).set_color(TEXT_COLOR).set_z_index(85)
        sarco_label.next_to(post, RIGHT, buff=0.9).align_to(post, UP)
        sarco_pointer = Arrow(sarco_label.get_left(), post.get_top(), buff=0.06,
                              tip_length=0.14, color=TEXT_COLOR).set_stroke(width=3).set_z_index(86)
        self.play(FadeIn(sarco_label), GrowArrow(sarco_pointer), run_time=0.5)
        self.wait(0.8)
        self.end_step()
        self.play(FadeOut(sarco_label), FadeOut(sarco_pointer), run_time=0.3)

        achr_label = Text("Acetylcholine\nreceptors", font_size=26).set_color(TEXT_COLOR).set_z_index(85)
        achr_label.next_to(post, RIGHT, buff=0.9).align_to(receptors, UP)
        achr_pointer = Arrow(achr_label.get_left(), receptors.get_right(),
                             buff=0.06, tip_length=0.14, color=TEXT_COLOR)\
                             .set_stroke(width=3).set_z_index(86)
        self.play(FadeIn(achr_label), GrowArrow(achr_pointer), run_time=0.5)
        self.wait(0.8)
        self.end_step()
        self.play(FadeOut(achr_label), FadeOut(achr_pointer), run_time=0.3)

        cleft_anchor = Dot(point=[post.get_center()[0],
                                  0.5*(pre.get_bottom()[1] + post.get_top()[1]), 0], radius=0.0)
        label_with_pointer(self, "Synaptic cleft", cleft_anchor)

        # ===== MAIN SEQUENCE =====

        # 1) Action potential arrives
        step1 = step_label(self, "Action potential arrives")
        start_pt = np.array([knob_mid[0], config.frame_height/2 - 0.15, 0])   # down the axon
        end_pt   = start_pt + DOWN*PRE_AP_LEN
        pre_ap_arrow = Arrow(start_pt, end_pt, buff=0, tip_length=PRE_AP_TIP, color=BOLT_COLOR)\
                        .set_stroke(width=PRE_AP_STROKE).set_z_index(60)
        self.play(GrowArrow(pre_ap_arrow), run_time=0.4)
        self.end_step()
        self.play(FadeOut(pre_ap_arrow), FadeOut(step1), run_time=0.2)

        # 2) Opening of Ca2+ channels — Ca dots enter above vesicles
        step2 = step_label(self, "Opening of Ca²⁺ channels")
        ca_targets = [v.get_center() + UP*0.18 for v in vesicles]
        # Ca2+ starts just outside each channel and enters through it
        ca_sources = [ch.get_center() + normalize(ch.get_center() - knob_mid)*0.3 for ch in channels]
        CA_DOT_R, CA_PER_CHANNEL = 0.06, 3
        def bez(A, B, bend): return VMobject().set_points_smoothly([A, (A+B)/2 + bend, B])
        ca_dots, ca_moves = VGroup(), []
        for src in ca_sources:
            nearest = sorted(ca_targets, key=lambda p: abs(p[0]-src[0]))[:2]
            for j in range(CA_PER_CHANNEL):
                d = Dot(radius=CA_DOT_R, color=CA_COLOR).move_to(src).set_z_index(25)
                ca_dots.add(d)
                tgt = nearest[j % len(nearest)]
                bend = DOWN*0.10 + (RIGHT if src[0] < knob_mid[0] else LEFT)*0.20
                ca_moves.append(MoveAlongPath(d, bez(src, tgt, bend)))
        self.add(ca_dots)
        self.play(*ca_moves, run_time=0.8, rate_func=smooth)
        self.end_step()
        self.play(FadeOut(ca_dots, scale=0.85), FadeOut(step2), run_time=0.2)

        # 3) ACh vesicles bind to membrane — docking
        step3 = step_label(self, "ACh vesicles bind\n to membrane", width=28)
        dock_y = pre.get_bottom()[1] + 0.05
        dock_targets = [np.array([knob_mid[0] + fx*DIAGRAM_SCALE, dock_y, 0]) for fx in fuse_xs]
        self.play(*[
            anim for (v, content), tgt in zip(zip(vesicles, ves_contents), dock_targets)
            for anim in (v.animate.move_to(tgt), content.animate.move_to(tgt))
        ], run_time=0.45)
        self.end_step()
        self.play(FadeOut(step3), run_time=0.2)

        # Fusion cue
        flashes = [SurroundingRectangle(v, color=VES_COLOR, buff=0.05).set_stroke(width=3, opacity=0.7).set_z_index(22)
                   for v in vesicles]
        self.play(*[Create(f) for f in flashes],
                  *[v.animate.scale(1.06).set_fill(opacity=0.35) for v in vesicles], run_time=0.18)

        # 4) Release ACh into the synaptic cleft — vesicles disappear (dots remain)
        step4 = step_label(self, "Release ACh into the synaptic cleft", width=28)
        self.play(*[FadeOut(v) for v in vesicles], *[FadeOut(f) for f in flashes], run_time=0.18)
        self.end_step()
        self.play(FadeOut(step4), run_time=0.2)

        # 5) ACh diffuses — dots bind on receptor caps
        step5 = step_label(self, "ACh diffuses across the synaptic cleft", width=28)
        moves, settles, bound = [], [], set()   # bound: receptors that ACh binds to
        for content in ves_contents:
            for dot in content:
                rec_i = min(range(len(receptors)), key=lambda i: abs(receptors[i].get_center()[0] - dot.get_center()[0]))
                bound.add(rec_i)
                cap = receptors[rec_i][1]
                cap_center = cap.get_center()
                r_world = cap.get_width()/2
                epsilon = 0.01
                bind_point = cap_center + UP*(r_world - epsilon)
                moves.append(MoveAlongPath(dot, drift(dot.get_center(), bind_point)))
                settles.append(dot.animate.move_to(bind_point).set_opacity(1.0).set_z_index(26))
        self.play(*moves, run_time=1.2, rate_func=smooth)
        self.end_step()
        self.play(*settles, FadeOut(step5))

        # 6) ACh binds (beat only)
        step6 = step_label(self, "ACh binds to AChR\n on sarcolemma", width=28)
        self.wait(0.2)
        self.end_step()
        self.play(FadeOut(step6), run_time=0.2)

        # 6a) Local Na+ influx — through the receptors ACh has bound to (they are the Na+ channels)
        step6a = step_label(self, "Local Na⁺ influx\n & depolarisation of sarcolemma", width=28)
        na_depth = 0.40; na_tip = 0.12; na_font = 22
        na_arrows, na_texts = VGroup(), VGroup()
        for idx in sorted(bound):
            cap = receptors[idx][1]
            start = cap.get_center()
            end   = start + DOWN * na_depth
            arrow = Arrow(start, end, buff=0, tip_length=na_tip, color=WHITE).set_stroke(width=3).set_z_index(28)
            na_arrows.add(arrow)
            na_texts.add(Text("Na⁺", font_size=na_font, color=WHITE).next_to(arrow, RIGHT, buff=0.06).set_z_index(28))
        self.play(*[GrowArrow(a) for a in na_arrows], FadeIn(na_texts, scale=0.95), run_time=0.4)
        self.end_step()
        self.play(FadeOut(step6a), FadeOut(na_arrows), FadeOut(na_texts), run_time=0.20)

        # 6b) AChE hydrolyses ACh — ACh fades from the receptors
        step6b = step_label(self, "Acetylcholinesterase hydrolyses ACh", width=28)
        ach_dots = VGroup(*[dot for content in ves_contents for dot in content])
        self.play(FadeOut(ach_dots, scale=0.5), run_time=0.6)
        self.end_step()
        self.play(FadeOut(step6b), run_time=0.2)

        # 7) Depolarisation through t-tubules — spans across cell, connected to SR
        step7 = step_label(self, "Action potential travels through T-tubules", width=28)

        sr = RoundedRectangle(width=SR_WIDTH, height=SR_HEIGHT, corner_radius=0.12,
                              color=SR_STROKE, fill_color=SR_FILL, fill_opacity=1.0)\
                              .set_stroke(width=3).set_z_index(30)
        sr_y = post.get_center()[1] - 0.35
        right_margin = 0.40
        sr_center_x_candidate = receptors.get_right()[0] + 2.6
        sr_center_x_max = post.get_right()[0] - right_margin - SR_WIDTH/2
        sr_x = min(sr_center_x_candidate, sr_center_x_max)
        sr.move_to([sr_x, sr_y, 0])

        sarco_top = post.get_top()[1]
        tub_y     = np.interp(0.40, [0,1], [sarco_top-0.40, sr.get_center()[1]+0.05])
        tub_start_x = post.get_left()[0] + 0.60
        tub_end_x   = sr.get_left()[0] - 0.02
        segments    = 7
        xs          = np.linspace(tub_start_x, tub_end_x, segments+1)

        t_arrows = VGroup()
        for i in range(segments):
            A = np.array([xs[i],   tub_y, 0.0]); B = np.array([xs[i+1], tub_y, 0.0])
            t_arrows.add(Arrow(A, B, buff=0, tip_length=0.16, color=WHITE).set_stroke(width=4).set_z_index(40))
        tube_path = Line([tub_start_x, tub_y, 0], [tub_end_x, tub_y, 0]).set_stroke(GREEN, width=8, opacity=1.0).set_z_index(39)
        junction_target = sr.get_left() + RIGHT*0.02
        connector = Arrow([tub_end_x, tub_y, 0], junction_target, buff=0, tip_length=0.16, color=WHITE)\
                    .set_stroke(width=4).set_z_index(41)

        tt_label = Text("T-tubule", font_size=20, color=WHITE).set_z_index(50)
        tt_label.next_to(tube_path, UP, buff=0.12).align_to(tube_path, RIGHT)

        # below the SR, clear of the T-tubule arrow coming in from above
        sr_label = Text("Sarcoplasmic\nreticulum", font_size=20, line_spacing=0.8, color=SR_STROKE).set_z_index(50)
        sr_label.next_to(sr, DOWN, buff=0.10)

        self.play(*[GrowArrow(a) for a in t_arrows], FadeIn(tt_label), run_time=0.35)
        self.play(Create(connector), run_time=0.20)
        self.play(ShowPassingFlash(tube_path, time_width=0.35), run_time=0.45)
        pulse = Dot(radius=0.07, color=WHITE).move_to(tube_path.get_start()).set_z_index(55)
        self.add(pulse)
        self.play(MoveAlongPath(pulse, tube_path), run_time=0.7, rate_func=linear)
        self.play(pulse.animate.move_to(junction_target), run_time=0.20)
        self.play(FadeIn(sr), FadeIn(sr_label), run_time=0.35)

        self.play(Indicate(sr, scale_factor=1.04, color=SR_STROKE), run_time=0.35)
        self.play(Circumscribe(sr, color=SR_STROKE, fade_out=True, time_width=0.6), run_time=0.35)
        self.end_step()
        self.play(FadeOut(step7), run_time=0.2)

        # =========================
        # 8) SR releases Ca²⁺ — Ca triggers sarcomere contraction
        # =========================
        step8 = step_label(self, "Sarcoplasmic reticulum releases Ca²⁺", width=30, y_shift=2.6)

        sm_group, sm_left, sm_right = make_mini_sarcomere()
        sm_group.set_z_index(60)
        for m in sm_group.submobjects: m.set_z_index(60)
        post.set_z_index(5)

        # ---- Placement slot & scaling (FIXED order so sm_h exists before use) ----
        top_clear    = sr.get_bottom()[1] - 0.00   # more headroom under SR
        bottom_clear = post.get_bottom()[1] + 0.20
        slot_height  = max(0.1, top_clear - bottom_clear)

        left_margin  = post.get_left()[0] + 0.32
        right_limit  = sr.get_left()[0] - 0.22
        max_width    = max(0.5, right_limit - left_margin)

        sm_w, sm_h = sm_group.get_width(), sm_group.get_height()
        s_h = (slot_height * 1.05) / sm_h
        s_w = (max_width   * 1.00) / sm_w
        s   = min(s_h, s_w)
        s   = min(s * 1.25, 2.5)
        sm_group.scale(s)

        # update after scaling
        sm_w, sm_h = sm_group.get_width(), sm_group.get_height()

        
        sm_x = (left_margin + right_limit) / 2.0
        # lift more, but keep inside the post-synaptic cell with a slightly larger headroom
        sm_y = (top_clear + bottom_clear) / 2.0 + 1.20
        sm_y = min(sm_y, top_clear - sm_h/2 + 0.02)  # allow 0.02 margin to the SR
        sm_group.move_to([sm_x, sm_y, 0])
        sm_group.shift(UP*0.5)

        sm_text = Text("Sarcomere", font_size=18, color=SM_LABEL_COLOR).set_z_index(65)
        sm_text.next_to(sm_group, UP, buff=0.08)

        # ---- Single Ca2+ dot & label (further left) ----
        ca_sr_group = VGroup(*[Dot(radius=CA_SR_R, color=CA_COLOR).move_to(sr.get_center()).set_z_index(55)
                               for _ in range(CA_SR_COUNT)])
        self.add(ca_sr_group)
        base_y = sr.get_center()[1]
        ca_target = np.array([sr.get_left()[0] - 0.7, base_y + 0.06, 0])  # further left
        self.play(ca_sr_group[0].animate.move_to(ca_target), run_time=0.6, rate_func=smooth)

        ca_label = Text("Ca²⁺", font_size=20, color=WHITE).set_z_index(200)
        ca_label.next_to(ca_sr_group[0], UP, buff=0.10)
        self.play(ca_sr_group[0].animate.scale(CA_PULSE_SCALE), FadeIn(ca_label), run_time=0.35)
        
        # keep Ca²⁺ label above everything else
        self.add_foreground_mobjects(ca_label)

        # ---- Ca → sarcomere arrow (bigger gap from label, short, horizontal, stays) ----
        start_pt = ca_label.get_left() + LEFT*0.12
        y        = ca_label.get_center()[1]
        
        sarc_right = sm_group.get_right()[0]
        gap_guard  = 0.06
        arrow_len  = 0.26
        
        nominal_end_x = start_pt[0] - arrow_len
        min_end_x     = sarc_right + gap_guard
        end_x         = max(nominal_end_x, min_end_x)
        
        min_visible = 0.12
        if end_x > start_pt[0] - min_visible:
            end_x = start_pt[0] - min_visible
            end_x = max(end_x, min_end_x + 0.02)
        
        end_pt = np.array([end_x, y, 0])
        
        ca_to_sm_arrow = Arrow(
            start_pt, end_pt,
            buff=0,
            tip_length=TO_SM_TIP*0.30,
            color=WHITE
        ).set_stroke(width=TO_SM_STROKE*0.50).set_z_index(200)
        
        self.add_foreground_mobjects(ca_to_sm_arrow)

        self.end_step()
        self.play(FadeOut(step8), run_time=0.10)
        self.remove(step8)

        # =========================
        # 9) Sarcomere contraction
        # =========================
        step9 = step_label(self, "Muscle contraction", width=26, y_shift=2.6)

        self.play(AnimationGroup(DrawBorderThenFill(sm_group, run_time=0.3),
                                 FadeIn(sm_text), lag_ratio=0.0))
        desired_gap   = SM_CONTRACT_TO
        inner_left_x  = sm_left[1].get_right()[0]
        inner_right_x = sm_right[1].get_left()[0]
        shift         = max(0, (inner_right_x - inner_left_x - desired_gap)/2)
        self.play(sm_left.animate.shift(RIGHT*shift),
                  sm_right.animate.shift(LEFT*shift),
                  run_time=SM_CONTRACT_TIME, rate_func=linear)

        self.play(FadeOut(step9), run_time=0.18)

        self.wait(1)
