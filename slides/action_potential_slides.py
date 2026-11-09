"""Action potential as click-through slides (Manim Slides test).

Based on notebooks/action-potential.ipynb (ActionPotentialFull), with:
- a pause (next_slide) after each stage, so the student clicks to continue
- a light background and dark text, matching the website (#faf8f8)
- a general stimulus channel ("Na⁺ channel") instead of "Ligand-gated Na⁺",
  since not every action potential starts with a ligand

Render and export (from this folder, in the manim-env environment):
    manim-slides render -qm action_potential_slides.py ActionPotentialSlides
    manim-slides convert ActionPotentialSlides action-potential.html
"""
from manim import *
from manim_slides import Slide
import numpy as np

config.background_color = "#faf8f8"
# 16:10 (taller than video's usual 16:9) so the caption has room at the bottom.
# Keep the usual width so the layout's x positions still fit.
config.pixel_width = 1280
config.pixel_height = 800
config.frame_width = 14.222
config.frame_height = 8.889
Text.set_default(font="Helvetica Neue")


class ActionPotentialSlides(Slide):
    def construct(self):
        # ===================== COLOURS (light background) =====================
        GRAPH_BLUE = "#284b63"      # site dark blue
        LABEL_GREY = "#4e4e4e"
        INK = "#2b2b2b"
        RESTING_GREEN = "#2E8B57"
        NA_COLOUR = "#D97706"
        STIM_COLOUR = "#B7791F"
        K_COLOUR = "#C2185B"
        MEMBRANE_COLOUR = "#84a59d"  # site sage green
        POSITIVE = "#C0392B"
        NEGATIVE = "#2E5EAA"
        CLOSED_RED = "#C0392B"
        OPEN_GREEN = "#2E8B57"
        PUMP_BLUE = "#284b63"

        STIM_FILL = "#E8C27A"
        NA_FILL = "#F2B66B"
        K_FILL = "#E58AB0"

        # ===================== LAYOUT =====================
        graph_center = UP * 2.05
        membrane_center = DOWN * 2.05
        mc_y = membrane_center[1]

        stim_x = -3.2
        vg_na_x = -1.2
        k_x = 2.8
        pump_x = 4.2

        # ===================== GRAPH =====================
        axes = Axes(
            x_range=[0, 7, 1], y_range=[-90, 50, 20],
            x_length=9, y_length=3.5,
            axis_config={"color": INK, "stroke_width": 2},
            x_axis_config={"include_ticks": False, "stroke_opacity": 0, "include_tip": False},
            y_axis_config={"include_ticks": True},
        ).move_to(graph_center)

        y_label = Text("mV", font_size=20, color=LABEL_GREY)
        y_label.next_to(axes.get_y_axis(), UP, buff=0.1)

        custom_x_axis = Arrow(
            start=axes.c2p(0, -90), end=axes.c2p(7, -90),
            color=INK, stroke_width=2, buff=0, max_tip_length_to_length_ratio=0.03,
        )
        x_label = Text("Time", font_size=20, color=LABEL_GREY)
        x_label.next_to(custom_x_axis, DOWN, buff=0.15)

        resting_line = DashedLine(axes.c2p(0, -70), axes.c2p(7, -70),
                                  color=RESTING_GREEN, stroke_width=1, dash_length=0.08)
        resting_lbl = Text("-70 mV", font_size=17, color=GRAPH_BLUE)
        resting_lbl.next_to(axes.c2p(0, -70), LEFT, buff=0.15)

        threshold_line = DashedLine(axes.c2p(0, -55), axes.c2p(7, -55),
                                    color=LABEL_GREY, stroke_width=1, dash_length=0.08)
        threshold_lbl = Text("-55 mV", font_size=17, color=GRAPH_BLUE)
        threshold_lbl.next_to(axes.c2p(0, -55), LEFT, buff=0.15)

        peak_lbl = Text("+30 mV", font_size=17, color=GRAPH_BLUE)
        peak_lbl.next_to(axes.c2p(0, 30), LEFT, buff=0.1)

        def ap_func(t):
            if t < 1.0: return -70                                    # Resting
            elif t < 1.8: return -70 + ((t - 1.0) / 0.8) * 15       # Stimulus: -70 → -55
            elif t < 2.5: return -55 + ((t - 1.8) / 0.7) * 85       # Depolarisation: -55 → +30
            elif t < 3.2: return 30 - ((t - 2.5) / 0.7) * 100       # Repolarisation: +30 → -70
            elif t < 3.8: return -70 - ((t - 3.2) / 0.6) * 10       # Hyperpolarisation: -70 → -80
            elif t < 5.0: return -80 + ((t - 3.8) / 1.2) * 10       # Recovery: -80 → -70
            else: return -70                                           # Resting

        t_vals = np.linspace(0, 6, 300)
        curve_points = [axes.c2p(t, ap_func(t)) for t in t_vals]

        def make_stage_label(text, position):
            label = Text(text, font_size=18, color=WHITE, weight=BOLD)
            bg = RoundedRectangle(width=label.width + 0.25, height=label.height + 0.15,
                                  corner_radius=0.06, fill_color=GRAPH_BLUE, fill_opacity=0.9, stroke_width=0)
            group = VGroup(bg, label)
            group.move_to(position)
            return group

        graph_stage_labels = [
            # below the resting line, where the graph is empty, so they don't hit the rising curve
            make_stage_label("Resting", axes.c2p(0.5, -81)),
            make_stage_label("Stimulus", axes.c2p(1.55, -81)),
            make_stage_label("Depolarisation", axes.c2p(2.8, 44)),
            make_stage_label("Repolarisation", axes.c2p(3.5, 8)),
            make_stage_label("Hyperpolarisation", axes.c2p(4.5, -85)),
            make_stage_label("Resting", axes.c2p(5.8, -52)),
        ]

        # ===================== VOLTAGE DISPLAY =====================
        voltage_val = ValueTracker(-70)
        vdisplay_center = RIGHT * 5.5 + UP * 2.5

        voltage_bg = RoundedRectangle(width=2.6, height=1.8, corner_radius=0.15,
                                      fill_color=WHITE, fill_opacity=1,
                                      stroke_color=GRAPH_BLUE, stroke_width=1.5).move_to(vdisplay_center)
        voltage_header = Text("P.D. across membrane", font_size=15, color=LABEL_GREY)
        voltage_header.move_to(vdisplay_center + UP * 0.55)
        voltage_display = always_redraw(lambda: Text(
            f"{round(voltage_val.get_value()):+d} mV",
            font_size=44, color=GRAPH_BLUE, weight=BOLD
        ).move_to(vdisplay_center + DOWN * 0.1))

        # ===================== MEMBRANE =====================
        mem_width = 9.0
        mem_height = 0.35
        outer_layer = Rectangle(width=mem_width, height=mem_height/2, fill_color=MEMBRANE_COLOUR,
                                fill_opacity=0.7, stroke_color=LABEL_GREY, stroke_width=1).move_to(membrane_center + UP * mem_height/4)
        inner_layer = Rectangle(width=mem_width, height=mem_height/2, fill_color=MEMBRANE_COLOUR,
                                fill_opacity=0.7, stroke_color=LABEL_GREY, stroke_width=1).move_to(membrane_center + DOWN * mem_height/4)
        membrane = VGroup(outer_layer, inner_layer)

        # left of the membrane, clear of the slide arrows at the bottom right
        outside_label = Text("Outside", font_size=15, color=LABEL_GREY).move_to([-5.15, mc_y + 0.3, 0])
        inside_label = Text("Inside", font_size=15, color=LABEL_GREY).move_to([-5.15, mc_y - 0.3, 0])

        # ===================== CHANNEL HELPERS =====================
        def make_channel(cx, stroke_color, fill_color):
            left = Rectangle(width=0.2, height=0.8, fill_color=fill_color, fill_opacity=0.9,
                             stroke_color=stroke_color, stroke_width=2).move_to([cx - 0.15, mc_y, 0])
            right = Rectangle(width=0.2, height=0.8, fill_color=fill_color, fill_opacity=0.9,
                              stroke_color=stroke_color, stroke_width=2).move_to([cx + 0.15, mc_y, 0])
            return VGroup(left, right)

        def make_gate_closed(cx):
            return Cross(stroke_color=CLOSED_RED, stroke_width=4).scale(0.15).move_to([cx, mc_y, 0])

        def make_gate_open(cx, direction_down=True, color=NA_COLOUR):
            if direction_down:
                return Arrow(start=[cx, mc_y+0.5, 0], end=[cx, mc_y-0.5, 0],
                             color=color, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.2)
            else:
                return Arrow(start=[cx, mc_y-0.5, 0], end=[cx, mc_y+0.5, 0],
                             color=color, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.2)

        def make_status(cx, text, color):
            return Text(text, font_size=14, color=color, weight=BOLD).move_to([cx, mc_y - 0.65, 0])

        # --- Na⁺ channel opened by the stimulus ---
        stim_channel = make_channel(stim_x, STIM_COLOUR, STIM_FILL)
        stim_label = Text("Na⁺ channel", font_size=17, color=STIM_COLOUR)
        stim_label.next_to(stim_channel, UP, buff=0.12)
        stim_gate_closed = make_gate_closed(stim_x)
        stim_gate_open = make_gate_open(stim_x, True, STIM_COLOUR)
        stim_status_closed = make_status(stim_x, "CLOSED", CLOSED_RED)
        stim_status_open = make_status(stim_x, "OPEN", OPEN_GREEN)
        stim_status = stim_status_closed.copy()

        # --- Voltage-gated Na⁺ ---
        vg_na_channel = make_channel(vg_na_x, NA_COLOUR, NA_FILL)
        vg_na_label = Text("Voltage-gated Na⁺", font_size=17, color=NA_COLOUR)
        vg_na_label.next_to(vg_na_channel, UP, buff=0.12)
        vg_na_gate_closed = make_gate_closed(vg_na_x)
        vg_na_gate_open = make_gate_open(vg_na_x, True, NA_COLOUR)
        vg_na_status_closed = make_status(vg_na_x, "CLOSED", CLOSED_RED)
        vg_na_status_open = make_status(vg_na_x, "OPEN", OPEN_GREEN)
        vg_na_status = vg_na_status_closed.copy()

        # --- Voltage-gated K⁺ ---
        k_channel = make_channel(k_x, K_COLOUR, K_FILL)
        k_label = Text("Voltage-gated K⁺", font_size=17, color=K_COLOUR)
        k_label.next_to(k_channel, UP, buff=0.12)
        k_gate_closed = make_gate_closed(k_x)
        k_gate_open = make_gate_open(k_x, False, K_COLOUR)
        k_status_closed = make_status(k_x, "CLOSED", CLOSED_RED)
        k_status_open = make_status(k_x, "OPEN", OPEN_GREEN)
        k_status = k_status_closed.copy()

        # --- Na⁺/K⁺ pump ---
        pump = Ellipse(width=1.0, height=1.0, fill_color=PUMP_BLUE, fill_opacity=0.95,
                       stroke_color=PUMP_BLUE, stroke_width=1.5).move_to([pump_x, mc_y, 0])
        pump_lbl = Text("Na⁺/K⁺\npump", font_size=13, color=WHITE, weight=BOLD).move_to(pump.get_center())
        pump_group = VGroup(pump, pump_lbl)

        # --- Charges ---
        def make_charges(text, color, y_offset, x_positions):
            charges = VGroup()
            for x in x_positions:
                c = Text(text, font_size=24, color=color, weight=BOLD).move_to([x, mc_y + y_offset, 0])
                charges.add(c)
            return charges

        outside_x = [-4.2]
        inside_x = [-4.2]
        charges_outside_pos = make_charges("+", POSITIVE, 0.55, outside_x)
        charges_inside_neg = make_charges("–", NEGATIVE, -0.55, inside_x)

        na_ions_outside = VGroup()
        for x in [-3.8, -0.3]:
            na_ions_outside.add(Text("Na⁺", font_size=17, color=NA_COLOUR, weight=BOLD).move_to([x, mc_y + 1.15, 0]))
        k_ions_inside = VGroup()
        for x in [1.8, 3.5]:
            k_ions_inside.add(Text("K⁺", font_size=17, color=K_COLOUR, weight=BOLD).move_to([x, mc_y - 0.95, 0]))

        stage_text = Text("Resting potential: membrane polarised at –70 mV",
                          font_size=20, color=INK).move_to(membrane_center + DOWN * 1.75)

        # ===================== ION HELPERS =====================
        def make_ion(label_text, color, position):
            dot = Dot(radius=0.16, color=color, fill_opacity=0.95)
            lbl = Text(label_text, font_size=12, color=WHITE, weight=BOLD).move_to(dot.get_center())
            ion = VGroup(dot, lbl); ion.move_to(position)
            return ion

        def make_ions_above(cx, lt, color, count=3):
            ions = VGroup()
            for i in range(count):
                ions.add(make_ion(lt, color, [cx + ([-0.3, 0, 0.3][i % 3]), mc_y + 1.0, 0]))
            return ions

        def make_ions_below(cx, lt, color, count=3):
            ions = VGroup()
            for i in range(count):
                ions.add(make_ion(lt, color, [cx + ([-0.3, 0, 0.3][i % 3]), mc_y - 1.0, 0]))
            return ions

        def animate_ions_down(ions, cx, run_time=2.0):
            return AnimationGroup(*[ion.animate.move_to([cx + (i-1)*0.4, mc_y - 1.0, 0])
                                    for i, ion in enumerate(ions)], lag_ratio=0.3, run_time=run_time)

        def animate_ions_up(ions, cx, run_time=2.0):
            return AnimationGroup(*[ion.animate.move_to([cx + (i-1)*0.4, mc_y + 1.0, 0])
                                    for i, ion in enumerate(ions)], lag_ratio=0.3, run_time=run_time)

        def caption(text):
            t = Text(text, font_size=20, color=INK)
            if t.width > 12.5:          # long captions shrink to fit the frame
                t.scale_to_fit_width(12.5)
            return t.move_to(stage_text.get_center())

        # ===================== SLIDES =====================

        # --- Slide 1: set the scene ---
        self.play(Create(axes), Create(custom_x_axis), Write(y_label), Write(x_label), run_time=1.5)
        self.play(Create(resting_line), Write(resting_lbl), Write(peak_lbl), run_time=1.2)
        self.play(FadeIn(membrane), FadeIn(outside_label), FadeIn(inside_label), run_time=1.0)
        self.play(
            FadeIn(stim_channel), FadeIn(stim_label),
            FadeIn(vg_na_channel), FadeIn(vg_na_label),
            FadeIn(k_channel), FadeIn(k_label),
            FadeIn(pump_group), run_time=1.0
        )
        self.play(FadeIn(charges_outside_pos), FadeIn(charges_inside_neg),
                  FadeIn(na_ions_outside), FadeIn(k_ions_inside), run_time=0.8)
        self.play(FadeIn(voltage_bg), Write(voltage_header), run_time=0.8)
        self.add(voltage_display)

        # --- Slide 2: resting (–70 mV) ---
        seg0 = VMobject(color=GRAPH_BLUE, stroke_width=3)
        seg0.set_points_smoothly(curve_points[0:51])
        self.play(
            Create(seg0, run_time=1.5), FadeIn(graph_stage_labels[0]),
            FadeIn(stim_gate_closed), FadeIn(stim_status),
            FadeIn(vg_na_gate_closed), FadeIn(vg_na_status),
            FadeIn(k_gate_closed), FadeIn(k_status), FadeIn(stage_text),
        )
        self.next_slide()

        # --- Slide 3: stimulus (–70 → –55 mV) ---
        seg1 = VMobject(color=GRAPH_BLUE, stroke_width=3)
        seg1.set_points_smoothly(curve_points[50:91])
        stim_ions = make_ions_above(stim_x, "Na⁺", STIM_COLOUR, 3)
        self.add(stim_ions)
        self.play(
            Create(seg1), FadeIn(graph_stage_labels[1]),
            Transform(stage_text, caption("Stimulus: Na⁺ channels open, so Na⁺ diffuses in")),
            FadeOut(stim_gate_closed), FadeIn(stim_gate_open),
            Transform(stim_status, stim_status_open.copy()),
            animate_ions_down(stim_ions, stim_x),
            voltage_val.animate.set_value(-55), run_time=2.5
        )
        self.next_slide()

        # --- Slide 4: threshold reached ---
        stim_gate_closed_2 = make_gate_closed(stim_x)
        self.play(
            Create(threshold_line), Write(threshold_lbl),
            Transform(stage_text, caption("Threshold (–55 mV) reached. Voltage-gated Na⁺ channels open")),
            FadeOut(stim_gate_open), FadeOut(stim_ions),
            FadeIn(stim_gate_closed_2), Transform(stim_status, stim_status_closed.copy()),
            FadeOut(vg_na_gate_closed), FadeIn(vg_na_gate_open),
            Transform(vg_na_status, vg_na_status_open.copy()), run_time=1.5
        )
        self.next_slide()

        # --- Slide 5: depolarisation (–55 → +30 mV) ---
        seg2 = VMobject(color=GRAPH_BLUE, stroke_width=3)
        seg2.set_points_smoothly(curve_points[90:126])
        vg_ions = make_ions_above(vg_na_x, "Na⁺", NA_COLOUR, 3)
        self.add(vg_ions)
        self.play(
            Create(seg2), FadeIn(graph_stage_labels[2]),
            Transform(stage_text, caption("Depolarisation: Na⁺ floods in, so the inside becomes positive")),
            animate_ions_down(vg_ions, vg_na_x),
            Transform(charges_outside_pos, make_charges("–", NEGATIVE, 0.55, outside_x)),
            Transform(charges_inside_neg, make_charges("+", POSITIVE, -0.55, inside_x)),
            voltage_val.animate.set_value(30), run_time=3.0
        )
        self.next_slide()

        # --- Slide 6: repolarisation (+30 → –70 mV) ---
        seg3 = VMobject(color=GRAPH_BLUE, stroke_width=3)
        seg3.set_points_smoothly(curve_points[125:161])
        vg_na_gate_closed_2 = make_gate_closed(vg_na_x)
        k_ions1 = make_ions_below(k_x, "K⁺", K_COLOUR, 3)
        self.add(k_ions1)
        self.play(
            Create(seg3), FadeIn(graph_stage_labels[3]),
            Transform(stage_text, caption("Repolarisation: Na⁺ channels close, K⁺ channels open, so K⁺ diffuses out")),
            FadeOut(vg_na_gate_open), FadeOut(vg_ions), FadeIn(vg_na_gate_closed_2),
            Transform(vg_na_status, vg_na_status_closed.copy()),
            FadeOut(k_gate_closed), FadeIn(k_gate_open), Transform(k_status, k_status_open.copy()),
            animate_ions_up(k_ions1, k_x),
            Transform(charges_outside_pos, make_charges("+", POSITIVE, 0.55, outside_x)),
            Transform(charges_inside_neg, make_charges("–", NEGATIVE, -0.55, inside_x)),
            voltage_val.animate.set_value(-70), run_time=3.0
        )
        self.next_slide()

        # --- Slide 7: hyperpolarisation (–70 → –80 mV) ---
        seg4 = VMobject(color=GRAPH_BLUE, stroke_width=3)
        seg4.set_points_smoothly(curve_points[160:191])
        extra_neg = make_charges("–", NEGATIVE, -0.55, [0.0])
        k_ions2 = make_ions_below(k_x, "K⁺", K_COLOUR, 2)
        for ion in k_ions2: ion.shift(RIGHT * 0.15)
        self.add(k_ions2)
        self.play(
            Create(seg4), FadeIn(graph_stage_labels[4]),
            Transform(stage_text, caption("Hyperpolarisation: K⁺ channels are slow to close, so it overshoots to –80 mV")),
            animate_ions_up(k_ions2, k_x), FadeIn(extra_neg),
            voltage_val.animate.set_value(-80), run_time=2.5
        )
        self.next_slide()

        # --- Slide 8: back to resting (–80 → –70 mV) ---
        seg5 = VMobject(color=GRAPH_BLUE, stroke_width=3)
        seg5.set_points_smoothly(curve_points[190:300])
        k_gate_closed_2 = make_gate_closed(k_x)
        self.play(
            Create(seg5), FadeIn(graph_stage_labels[5]),
            FadeOut(k_gate_open), FadeOut(k_ions1), FadeOut(k_ions2), FadeOut(extra_neg),
            FadeIn(k_gate_closed_2), Transform(k_status, k_status_closed.copy()),
            Transform(stage_text, caption("Resting potential restored: the Na⁺/K⁺ pump restores the ion balance (–70 mV)")),
            voltage_val.animate.set_value(-70), run_time=2.0
        )
        self.next_slide()
