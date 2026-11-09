"""LFilament_CaBind_TMBack_OvalHead

Converted from notebooks/sliding-filament-theory.ipynb (code unchanged apart from removing the notebook-only lines).

Render (from the repo folder, in the manim-env environment):
    python -m manim -ql scenes/sliding_filament.py LFilament_CaBind_TMBack_OvalHead     # quick preview (480p)
    python -m manim -qh scenes/sliding_filament.py LFilament_CaBind_TMBack_OvalHead     # final video (1080p)
"""
from manim import *
import numpy as np

# ======================
# KNOBS / PALETTE
# ======================
GLOBAL_SCALE       = 1.15

ACTIN_COLOR        = "#00D5FF"
TROPOMYOSIN_COLOR  = "#F60079"
TROPONIN_COLOR     = "#F39C12"
MYOSIN_COLOR       = "#8F5AFF"

# Calcium (distinct from troponin)
CA_DOT_COLOR       = "#00FF00"
CA_TEXT_COLOR      = "#00FF00"

# Actin double helix
BEADS_PER_STRAND   = 18
BEAD_SPACING       = 0.35
BEAD_RADIUS        = 0.12
HELIX_Y_OFFSET     = 0.13
HELIX_WAVE_AMP     = 0.10
HELIX_WAVE_PER     = 4.0

# Tropomyosin rope (animated roll)
TM_STROKE_WIDTH    = 12
TM_WAVE_AMP        = 0.06
TM_WAVE_PER        = 6.0
TM_Y_OFFSET        = 0.05

# Troponin triads
TN_PERIOD_EVERY    = 4
TN_DOT_RADIUS      = 0.075

# Myosin geometry
MYOSIN_LEN         = 6.5
MYOSIN_THICK       = 0.40
HEAD_STEM_LEN      = 0.8
HEAD_OVAL_W        = 0.75
HEAD_OVAL_H        = 0.45
STEM_ANGLE_DEG     = 45   # stem ~45°
HEAD_START_DEG     = 90   # oval head upright (cocked)
HEAD_STROKE        = 8

# Spacing
INTER_FILAMENT_GAP = 1.95
ACTIN_Y            = +INTER_FILAMENT_GAP/2
MYOSIN_Y           = -INTER_FILAMENT_GAP/2
X_CENTER           = 0.0

# ADP & Pi
ADP_R, PI_R        = 0.2, 0.2
ADP_COLOR          = "#F1C40F"
PI_COLOR           = "#F39C12"
ADP_FONT, PI_FONT  = 12, 12
ADP_TEXT_COLOR     = BLACK
PI_TEXT_COLOR      = BLACK
ADP_STROKE, PI_STROKE = 2, 1.8

# Calcium label & timing
CA_DOT_R = 0.2
CA_FONT  = 25
CA_FROM  = LEFT*4.0 + UP*2.0
CA_TRAVEL_TIME = 2.8
CA_LABEL_FADE_FRACTION = 0.55
CA_BOUND_OFFSET = UP*0.08 + LEFT*0.06

# Labels (persistent names)
LABEL_SCALE        = 0.52
LEFT_LABEL_BUFF    = 0.68

# Actin nudge after Ca2+ binds
ACTIN_NUDGE        = 0.07
ACTIN_NUDGE_TIME   = 0.45

# Step cue
STEP_FONT          = 22
STEP_TEXT_COLOR    = WHITE
STEP_BG_COLOR      = BLACK
STEP_BG_OPACITY    = 0.35
STEP_FADE_IN       = 0.25
STEP_LINGER        = 1.4   # longer linger
STEP_FADE_OUT      = 0.25

def cue_step(scene, text, anchor=None, direction=UP, buff=0.25,
             t_in=STEP_FADE_IN, linger=STEP_LINGER, t_out=STEP_FADE_OUT, z=100):
    label = Text(text, font_size=STEP_FONT, color=STEP_TEXT_COLOR)
    if anchor is None:
        label.to_edge(UP, buff=0.4)
    else:
        label.next_to(anchor, direction, buff=buff)
    bg = SurroundingRectangle(label, buff=0.12, corner_radius=0.12)
    bg.set_fill(STEP_BG_COLOR, STEP_BG_OPACITY).set_stroke(width=0)
    group = VGroup(bg, label).set_z_index(z)
    scene.play(FadeIn(group, shift=UP*0.12), run_time=t_in)
    scene.wait(linger)
    scene.play(FadeOut(group, shift=UP*0.12), run_time=t_out)

# ATP badge
ATP_COLOR          = "#FFD200"
ATP_POINTS         = 8
ATP_OUTER_R        = 0.28
ATP_INNER_R        = 0.14
ATP_FONT           = 20
ATP_FROM           = RIGHT*3.5 + DOWN*0.3
ATP_BIND_OFFSET    = RIGHT*0.18 + UP*0.06
ATP_BIND_TIME      = 0.8
HEAD_RESET_TIME    = 0.9

def make_atp_badge(center=np.array([0,0,0]), points=ATP_POINTS, outer=ATP_OUTER_R, inner=ATP_INNER_R, color=ATP_COLOR, font_size=ATP_FONT):
    verts = []
    for i in range(points*2):
        r = outer if i % 2 == 0 else inner
        t = i * np.pi / points
        verts.append(center + np.array([r*np.cos(t), r*np.sin(t), 0]))
    star  = Polygon(*verts, color=color, fill_color=color, fill_opacity=1.0)
    label = Text("ATP", font_size=font_size, color=BLACK).move_to(star.get_center())
    return VGroup(star, label)

# Mini sarcomere inset (no Z-lines)
def make_sarcomere_inset():
    spacing_y = 0.36
    actin_len = 1.6
    gap       = 2.6
    myosin_w  = 2.1
    m_height  = 1.2
    base_actin = Rectangle(height=0.12, width=actin_len)\
                    .set_fill(ACTIN_COLOR, 0.9).set_stroke(ACTIN_COLOR, 2)
    actin_left = VGroup(base_actin.copy().shift( UP*spacing_y),
                        base_actin.copy(),
                        base_actin.copy().shift(DOWN*spacing_y)).shift(LEFT*gap/2)
    actin_right= VGroup(base_actin.copy().shift( UP*spacing_y),
                        base_actin.copy(),
                        base_actin.copy().shift(DOWN*spacing_y)).shift(RIGHT*gap/2)
    base_myosin= Rectangle(height=0.20, width=myosin_w)\
                    .set_fill(MYOSIN_COLOR, 0.9).set_stroke(MYOSIN_COLOR, 2)
    myosin = VGroup(base_myosin.copy().shift(UP*0.25),
                    base_myosin.copy().shift(DOWN*0.25))
    m_line = Line(UP*(m_height/2+0.10), DOWN*(m_height/2+0.10)).set_stroke(GREY_B, 2)
    label = Text("Sarcomere", font_size=24, color=WHITE).next_to(m_line, UP, buff=0.15)
    sarco = VGroup(actin_left, actin_right, myosin, m_line, label)
    sarco.scale(0.75).to_corner(UR, buff=0.35).set_z_index(200)
    return {"group": sarco, "actin_left": actin_left, "actin_right": actin_right, "myosin": myosin, "m_line": m_line}

# BIND: move straight up (no angle change), keep bulb pinned; stem re-hinges every frame
def bind_head_to_actin_vertical(scene, backbone, stem, bulb, left_strand, right_strand,
                                *, CONTACT_OVERLAP=0.06, APPROACH_GAP=0.05,
                                APPROACH_TIME=0.6, BIND_SNAP_TIME=0.25):
    stem.clear_updaters(); bulb.clear_updaters()

    beads = list(left_strand) + list(right_strand)
    bx, by, _ = bulb.get_center()
    higher = [b for b in beads if b.get_center()[1] >= by - 1e-6] or beads
    target_bead = min(higher, key=lambda d: abs(d.get_center()[0] - bx))

    bead_pt    = target_bead.get_center()
    contact_pt = bead_pt + DOWN*CONTACT_OVERLAP
    approach_pt= np.array([bx, contact_pt[1] - APPROACH_GAP, 0.0])

    # keep stem connected to backbone top → bulb center; recompute pivot every frame
    def _lock_stem(_m):
        pivot = backbone.get_center() + np.array([0.0, backbone.height/2, 0.0])
        stem.put_start_and_end_on(pivot, bulb.get_center())
    stem.add_updater(_lock_stem)

    # 1) straight up approach, 2) snap to contact
    scene.play(bulb.animate.move_to(approach_pt), run_time=APPROACH_TIME, rate_func=smooth)
    scene.play(bulb.animate.move_to(contact_pt), run_time=BIND_SNAP_TIME, rate_func=smooth)

    # pin the bulb at the bead
    def _lock_bulb(_m): bulb.move_to(target_bead.get_center() + DOWN*CONTACT_OVERLAP)
    bulb.add_updater(_lock_bulb)
    scene.play(Indicate(target_bead, color=WHITE, scale_factor=1.06), run_time=0.25)

    def unlock_bulb():
        try: bulb.remove_updater(_lock_bulb)
        except Exception: pass
    def unlock_stem():
        try: stem.remove_updater(_lock_stem)
        except Exception: pass
    return target_bead, unlock_bulb, unlock_stem


class LFilament_CaBind_TMBack_OvalHead(Scene):
    def construct(self):
        # ---------- Actin ----------
        def strand(sign=+1):
            dots = VGroup()
            for i in range(BEADS_PER_STRAND):
                x = i*BEAD_SPACING
                y = sign*HELIX_Y_OFFSET + HELIX_WAVE_AMP*np.sin(2*np.pi*i/HELIX_WAVE_PER)
                dots.add(Circle(radius=BEAD_RADIUS, color=ACTIN_COLOR,
                                fill_color=ACTIN_COLOR, fill_opacity=1).move_to([x, y, 0]))
            return dots

        left_strand  = strand(+1)
        right_strand = strand(-1).shift(RIGHT*(BEAD_SPACING*0.5))
        actin        = VGroup(left_strand, right_strand).move_to([X_CENTER, ACTIN_Y, 0]).set_z_index(5)

        # ---------- Tropomyosin ----------
        x0 = left_strand[0].get_center()[0]
        x1 = left_strand[-1].get_center()[0]
        xs = np.linspace(x0, x1, 80)
        y_mid = (left_strand[0].get_center()[1] + right_strand[0].get_center()[1]) / 2

        phase = ValueTracker(0.0)
        amp   = ValueTracker(TM_WAVE_AMP)
        tm    = VMobject(color=TROPOMYOSIN_COLOR).set_stroke(width=TM_STROKE_WIDTH).set_z_index(7)
        def update_tm(m):
            ph = phase.get_value(); A = amp.get_value()
            y_center = y_mid + TM_Y_OFFSET
            pts = [[x, y_center + A*np.sin(2*np.pi*j/len(xs)*(len(xs)/TM_WAVE_PER) + ph), 0]
                   for j, x in enumerate(xs)]
            m.set_points_smoothly(pts)
        update_tm(tm); tm.add_updater(update_tm)

        # ---------- Troponin ----------
        troponin = VGroup().set_z_index(9)
        y_center = y_mid + TM_Y_OFFSET
        for i in range(0, BEADS_PER_STRAND, TN_PERIOD_EVERY):
            cx = left_strand[i].get_center()[0]
            j = int(np.argmin(np.abs(xs - cx)))
            base = np.array([xs[j], y_center + TM_WAVE_AMP*np.sin(2*np.pi*j/len(xs)*(len(xs)/TM_WAVE_PER)), 0])
            tri = VGroup(
                Circle(radius=TN_DOT_RADIUS, color=TROPONIN_COLOR, fill_color=TROPONIN_COLOR, fill_opacity=1).move_to(base + np.array([0.00, 0.10, 0])),
                Circle(radius=TN_DOT_RADIUS, color=TROPONIN_COLOR, fill_color=TROPONIN_COLOR, fill_opacity=1).move_to(base + np.array([-0.09, -0.05, 0])),
                Circle(radius=TN_DOT_RADIUS, color=TROPONIN_COLOR, fill_color=TROPONIN_COLOR, fill_opacity=1).move_to(base + np.array([0.09, -0.05, 0])),
            )
            troponin.add(tri)

        thin_filament = VGroup(actin, tm, troponin)

        # ---------- Labels (place once, then never reflow) ----------
        actin_label = Text("Actin", color=ACTIN_COLOR).scale(LABEL_SCALE).next_to(actin, UP, buff=0.35).align_to(actin, LEFT)
        tm_label    = Text("Tropomyosin", color=TROPOMYOSIN_COLOR).scale(LABEL_SCALE)
        tm_label.next_to(actin, LEFT, buff=LEFT_LABEL_BUFF); tm_label.set_y(y_mid + TM_Y_OFFSET)
        tn_label    = Text("Troponin", color=TROPONIN_COLOR).scale(LABEL_SCALE).next_to(tm_label, DOWN, buff=0.18).align_to(tm_label, LEFT)

        # Left-hand Myosin label (next to bottom filament region)
        myosin_side_label = Text("Myosin", color=MYOSIN_COLOR).scale(LABEL_SCALE)
        myosin_side_label.next_to(actin, LEFT, buff=LEFT_LABEL_BUFF)
        myosin_side_label.set_y(MYOSIN_Y)

        # ---------- Myosin + head (in front of actin) ----------
        backbone = Rectangle(width=MYOSIN_LEN, height=MYOSIN_THICK,
                             color=MYOSIN_COLOR, fill_color=MYOSIN_COLOR, fill_opacity=0.95).move_to([X_CENTER, MYOSIN_Y, 0]).set_z_index(50)

        # STEM at ~45°
        ang = np.deg2rad(STEM_ANGLE_DEG)
        start = backbone.get_center() + np.array([0.0,  MYOSIN_THICK/2, 0])
        end   = start + np.array([+HEAD_STEM_LEN*np.cos(ang),  HEAD_STEM_LEN*np.sin(ang), 0])
        stem  = Line(start, end, color=MYOSIN_COLOR).set_stroke(width=HEAD_STROKE).set_z_index(55)

        # OVAL HEAD at 90° (upright)
        bulb  = Ellipse(width=HEAD_OVAL_W, height=HEAD_OVAL_H,
                        color=MYOSIN_COLOR, fill_color=MYOSIN_COLOR, fill_opacity=1).move_to(end + RIGHT*0.05)
        bulb.rotate(np.deg2rad(HEAD_START_DEG), about_point=bulb.get_center())
        head  = VGroup(stem, bulb).set_z_index(60)

        # Ligands follow stem
        adp_c = Circle(radius=ADP_R, color=BLACK, stroke_width=ADP_STROKE, fill_color=ADP_COLOR, fill_opacity=1).set_z_index(70)
        pi_c  = Circle(radius=PI_R,  color=BLACK, stroke_width=PI_STROKE,  fill_color=PI_COLOR,  fill_opacity=1).set_z_index(70)
        adp_t = Text("ADP", font_size=ADP_FONT, color=ADP_TEXT_COLOR).set_z_index(71)
        pi_t  = Text("Pi",  font_size=PI_FONT,  color=PI_TEXT_COLOR).set_z_index(71)
        LIG_ALONG = 0.4; LIG_PERP = 0.3
        def place_on_stem(mobj, side=+1, along=LIG_ALONG, off=LIG_PERP):
            s = stem.get_start(); e = stem.get_end()
            v = e - s; L = np.linalg.norm(v) if np.linalg.norm(v) != 0 else 1.0
            u = v / L; perp = np.array([-u[1], u[0], 0.0])
            mobj.move_to(e - u*along + side*perp*off)
        for m in (adp_c, pi_c, adp_t, pi_t): m.clear_updaters()
        adp_c.add_updater(lambda m: place_on_stem(m, side=+1))
        pi_c .add_updater(lambda m: place_on_stem(m, side=-1))
        adp_t.add_updater(lambda m: m.move_to(adp_c.get_center()))
        pi_t .add_updater(lambda m: m.move_to(pi_c.get_center()))

        # === Sites shifted RIGHT to match binding position ===
        target_beads = VGroup(right_strand[10], right_strand[11])
        def make_site_rings(color):
            rings = VGroup()
            for bead in target_beads:
                ring = Circle(radius=BEAD_RADIUS*1.6, color=color).set_stroke(width=4).set_fill(opacity=0).set_z_index(100)
                ring.add_updater(lambda m, b=bead: m.move_to(b.get_center()))
                rings.add(ring)
            return rings
        blocked_rings = make_site_rings(WHITE)
        exposed_rings = make_site_rings("#00FF00")
        blocked_label = Text("actin-myosin sites blocked", color=WHITE, font_size=20).set_z_index(100)
        exposed_label = Text("actin-myosin sites exposed", color=WHITE, font_size=20).set_z_index(100)

        # Label for cocked myosin heads
        cocked_label = Text("myosin heads high-energy position 'cocked'",
                            color=WHITE, font_size=20).set_z_index(100)

        # NEW: label for tropomyosin movement
        tm_shift_label = Text("tropomyosin changes position",
                              color=WHITE, font_size=20).set_z_index(100)
        tm_shift_label.add_updater(lambda m: m.next_to(thin_filament, UP, buff=0.8))

        anchor_group = VGroup(*target_beads)
        blocked_label.add_updater(lambda m: m.next_to(anchor_group, UP, buff=0.8))
        exposed_label.add_updater(lambda m: m.next_to(anchor_group, UP, buff=0.8))
        cocked_label.add_updater(lambda m: m.next_to(anchor_group, UP, buff=0.8))

        for g in (blocked_rings, exposed_rings, blocked_label, exposed_label, cocked_label, tm_shift_label):
            g.set_opacity(0)

        # Collect & scale
        diagram = VGroup(
            thin_filament, backbone, head, adp_c, pi_c, adp_t, pi_t,
            actin_label, tm_label, tn_label, myosin_side_label,
            Text("Myosin", color=MYOSIN_COLOR, font_size=28).next_to(backbone, DOWN, buff=0.35)
        ).scale(GLOBAL_SCALE)
        for g in (blocked_rings, exposed_rings, blocked_label, exposed_label, cocked_label, tm_shift_label):
            g.scale(GLOBAL_SCALE)

        # Store initial head position (for "cycle stops" reset)
        initial_bulb_pos = bulb.get_center()

        # --- Sarcomere inset ---
        sarco = make_sarcomere_inset()
        self.play(FadeIn(sarco["group"]), run_time=0.7)
        self.wait(0.4)

        # --- Sarcoplasmic reticulum (for later 'cycle stops') ---
        sr_box = Rectangle(width=2.2, height=0.8, color=BLUE_E, fill_color=BLUE_E, fill_opacity=0.8)
        sr_box.to_corner(UL, buff=0.4)
        sr_text = Text("Sarcoplasmic\nreticulum", font_size=20, color=WHITE).move_to(sr_box.get_center())
        sr_group = VGroup(sr_box, sr_text).set_z_index(80)
        sr_group.set_opacity(0)
        self.add(sr_group)

        # --- Contraction arrows (follow their anchors via updaters; start hidden) ---
        actin_arrow = Arrow(ORIGIN, RIGHT*0.7, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        actin_arrow.set_color(YELLOW).set_z_index(999).set_opacity(0)
        def _upd_actin_arrow(m):
            tip_center = right_strand[-1].get_center() + UP*0.45
            m.put_start_and_end_on(tip_center - RIGHT*0.35, tip_center + RIGHT*0.35)
        actin_arrow.add_updater(_upd_actin_arrow)
        
        sarco_arrow = Arrow(ORIGIN, LEFT*0.56, buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        sarco_arrow.set_color(YELLOW).set_z_index(999).set_opacity(0)
        def _upd_sarco_arrow(m):
            anchor = sarco["actin_right"].get_top() + RIGHT*0.20 + UP*0.12
            m.put_start_and_end_on(anchor + RIGHT*0.28, anchor - RIGHT*0.28)
        sarco_arrow.add_updater(_upd_sarco_arrow)

        # ======== SEQUENCE ========
        actin.set_z_index(5); tm.set_z_index(10); troponin.set_z_index(20)

        # 1) Actin + labels
        self.play(FadeIn(left_strand, shift=LEFT*0.2),
                  FadeIn(right_strand, shift=RIGHT*0.2), run_time=0.7)
        self.play(Write(actin_label), run_time=0.35)
        self.play(Create(tm), run_time=0.6)
        self.play(Write(tm_label), run_time=0.35)
        self.play(FadeIn(troponin, scale=0.9), run_time=0.6)
        self.play(Write(tn_label), run_time=0.35)
        self.bring_to_front(troponin)

        # 2) Bring in myosin + side label
        self.play(FadeIn(VGroup(backbone, head, adp_c, adp_t, pi_c, pi_t)), run_time=0.8)
        self.play(Write(myosin_side_label), run_time=0.35)

        # 2b) Cocked label right after myosin, before blocked + Ca
        self.add(cocked_label)
        self.bring_to_front(cocked_label)
        self.play(cocked_label.animate.set_opacity(1), run_time=0.4)
        self.wait(1.4)
        self.play(cocked_label.animate.set_opacity(0), run_time=0.35)

        # 3) Show blocked sites, then hide
        self.add(blocked_rings, blocked_label)
        self.bring_to_front(blocked_rings, blocked_label)
        self.play(blocked_rings.animate.set_opacity(1), blocked_label.animate.set_opacity(1), run_time=0.4)
        self.wait(1.4)
        self.play(blocked_rings.animate.set_opacity(0), blocked_label.animate.set_opacity(0), run_time=0.35)

        # 4) Ca2+ binds near RIGHT site
        target_mean_x = np.mean([b.get_center()[0] for b in target_beads])
        tri_by_x = min(range(len(troponin)), key=lambda i: abs(troponin[i].get_center()[0] - target_mean_x))
        bind_pt  = troponin[tri_by_x].get_center()
        start_pt = bind_pt + CA_FROM
        ca_dot = Dot(radius=CA_DOT_R, color=CA_DOT_COLOR).move_to(start_pt).set_z_index(30)
        ca_tag = Text("Ca²⁺", font_size=CA_FONT, color=CA_TEXT_COLOR).next_to(ca_dot, DOWN, buff=0.1).set_z_index(30)
        mid_pt = (start_pt + bind_pt)/2 + UP*0.4
        self.play(FadeIn(ca_dot, shift=LEFT*0.2+DOWN*0.2), FadeIn(ca_tag), run_time=0.45)

        ca_path = VMobject()
        ca_path.set_points_smoothly(np.array([start_pt, mid_pt, bind_pt]))
        self.play(
            MoveAlongPath(ca_dot, ca_path),
            Succession(Wait(CA_TRAVEL_TIME*CA_LABEL_FADE_FRACTION), FadeOut(ca_tag, run_time=0.25)),
            run_time=CA_TRAVEL_TIME, rate_func=linear
        )

        self.play(Indicate(troponin[tri_by_x], color=TROPONIN_COLOR, scale_factor=1.08), run_time=0.45)
        ca_dot.add_updater(lambda m, tri=troponin[tri_by_x]: m.move_to(tri.get_center() + CA_BOUND_OFFSET))

        # Tropomyosin shift
        self.play(phase.animate.increment_value(np.pi), amp.animate.set_value(TM_WAVE_AMP*0.4), run_time=0.8, rate_func=smooth)
        tm.remove_updater(update_tm); tm.set_z_index(3)
        self.play(thin_filament.animate.shift(UP*ACTIN_NUDGE), run_time=ACTIN_NUDGE_TIME, rate_func=there_and_back)

        # "tropomyosin changes position" label
        self.add(tm_shift_label)
        self.bring_to_front(tm_shift_label)
        self.play(tm_shift_label.animate.set_opacity(1), run_time=0.4)
        self.wait(1.4)
        self.play(tm_shift_label.animate.set_opacity(0), run_time=0.35)

        # Exposed (right-side), then hide
        self.add(exposed_rings, exposed_label); self.bring_to_front(exposed_rings, exposed_label)
        self.play(exposed_rings.animate.set_opacity(1), exposed_label.animate.set_opacity(1), run_time=0.4)
        self.wait(1.4)
        self.play(exposed_rings.animate.set_opacity(0), exposed_label.animate.set_opacity(0), run_time=0.35)

        # 5) Bind straight up (no angle change)
        target_bead, unlock_bulb, unlock_stem = bind_head_to_actin_vertical(
            self, backbone, stem, bulb, left_strand, right_strand,
            CONTACT_OVERLAP=0.08, APPROACH_GAP=0.05, APPROACH_TIME=0.6, BIND_SNAP_TIME=0.25
        )
        cue_step(self, "Cross-bridge formation", anchor=actin, direction=UP)

        # ----- POWER STROKE with contraction arrows -----
        PULL_DIST        = 0.45
        BULB_ROT_DEG     = -45
        ADP_RELEASE_DROP = DOWN*0.55 + LEFT*0.10
        PI_RELEASE_DROP  = DOWN*0.55 + RIGHT*0.10
        INSET_SLIDE      = 0.28

        attach_pos = bulb.get_center()
        unlock_bulb()   # stop following the bead
        def keep_bulb_worldpos(_m): bulb.move_to(attach_pos)
        bulb.add_updater(keep_bulb_worldpos)

        for m in (adp_c, pi_c, adp_t, pi_t): m.clear_updaters()
        adp_group, pi_group = VGroup(adp_c, adp_t), VGroup(pi_c, pi_t)

        ps_text = Text("Power stroke", font_size=STEP_FONT, color=STEP_TEXT_COLOR).next_to(actin, UP, buff=0.25)
        ps_bg   = SurroundingRectangle(ps_text, buff=0.12, corner_radius=0.12).set_fill(BLACK, 0.35).set_stroke(width=0)
        ps_cue  = VGroup(ps_bg, ps_text).set_z_index(120)

        # SHOW arrows while stroke happens
        self.play(
            actin_arrow.animate.set_opacity(1),
            sarco_arrow.animate.set_opacity(1),
            Rotate(bulb, angle=np.deg2rad(BULB_ROT_DEG), about_point=bulb.get_center()),
            thin_filament.animate.shift(RIGHT * PULL_DIST),
            backbone.animate.shift(LEFT * PULL_DIST),
            sarco["actin_left"].animate.shift(RIGHT * INSET_SLIDE),
            sarco["actin_right"].animate.shift(LEFT  * INSET_SLIDE),
            adp_group.animate.shift(ADP_RELEASE_DROP),
            pi_group.animate.shift(PI_RELEASE_DROP),
            FadeIn(ps_cue, shift=UP*0.12),
            run_time=1.0, rate_func=smooth
        )
        self.play(FadeOut(ps_cue, shift=UP*0.12), run_time=0.25)

        # Sarcomere contraction label
        cue_step(self, "Sarcomere contraction", anchor=actin, direction=UP, linger=1.4)

        # Hide the arrows
        self.play(FadeOut(actin_arrow), FadeOut(sarco_arrow), run_time=0.3)

        # 6) ATP binds → detach at the new position (no snap-back)
        self.play(FadeOut(adp_group), FadeOut(pi_group), run_time=0.35)
        atp = make_atp_badge().set_z_index(80)
        atp.move_to(bulb.get_center() + ATP_FROM)
        atp_target = bulb.get_center() + ATP_BIND_OFFSET

        atp_path = VMobject()
        atp_path.set_points_smoothly(np.array([
            atp.get_center(),
            (atp.get_center()+atp_target)/2 + UP*0.2,
            atp_target
        ]))

        self.play(FadeIn(atp, scale=0.85), run_time=0.25)
        self.play(MoveAlongPath(atp, atp_path), run_time=ATP_BIND_TIME, rate_func=smooth)
        cue_step(self, "ATP binds → detachment", anchor=actin, direction=UP)
        atp.add_updater(lambda m: m.move_to(bulb.get_center() + ATP_BIND_OFFSET))

        # Detach & shorten stem
        bulb.remove_updater(keep_bulb_worldpos)
        try: unlock_stem()
        except Exception: pass

        pivot = backbone.get_center() + np.array([0.0, backbone.height/2, 0.0])
        vec   = bulb.get_center() - pivot
        L     = np.linalg.norm(vec) if np.linalg.norm(vec) != 0 else 1.0
        u     = vec / L
        SHORTEN     = 0.50
        new_end     = pivot + u * max(L - SHORTEN, 0.20)
        DETACH_AWAY = DOWN * 0.18

        def _lock_stem_detach(_m): stem.put_start_and_end_on(pivot, bulb.get_center())
        stem.add_updater(_lock_stem_detach)

        self.play(bulb.animate.move_to(new_end + DETACH_AWAY), run_time=0.6, rate_func=smooth)

        stem.remove_updater(_lock_stem_detach)

        # 7) ATP hydrolysis → re-cock head back to 90°
        atp.clear_updaters()
        def stem_anchor(side, along=0.4, off=0.3):
            s = stem.get_start(); e = stem.get_end()
            v = e - s; L = np.linalg.norm(v) if np.linalg.norm(v) != 0 else 1.0
            u2 = v / L; perp = np.array([-u2[1], u2[0], 0.0])
            return e - u2*along + side*perp*off
        adp2_c = Circle(radius=ADP_R, color=BLACK, stroke_width=ADP_STROKE, fill_color=ADP_COLOR, fill_opacity=1).move_to(stem_anchor(+1))
        adp2_t = Text("ADP", font_size=ADP_FONT, color=ADP_TEXT_COLOR).move_to(adp2_c.get_center())
        pi2_c  = Circle(radius=PI_R,  color=BLACK, stroke_width=PI_STROKE,  fill_color=PI_COLOR,  fill_opacity=1).move_to(stem_anchor(-1))
        pi2_t  = Text("Pi", font_size=PI_FONT,  color=PI_TEXT_COLOR).move_to(pi2_c.get_center())

        hydro_text = Text("ATP hydrolysis → ADP + Pi (re-cocking)", font_size=STEP_FONT, color=STEP_TEXT_COLOR).next_to(actin, UP, buff=0.25)
        hydro_bg   = SurroundingRectangle(hydro_text, buff=0.12, corner_radius=0.12).set_fill(BLACK, 0.35).set_stroke(width=0)
        hydro_cue  = VGroup(hydro_bg, hydro_text).set_z_index(120)
        self.play(
            FadeIn(hydro_cue, shift=UP*0.12),
            TransformFromCopy(atp, adp2_c),
            TransformFromCopy(atp, adp2_t),
            TransformFromCopy(atp, pi2_c),
            TransformFromCopy(atp, pi2_t),
            Rotate(bulb, angle=np.deg2rad(+45), about_point=bulb.get_center()),
            run_time=0.9
        )
        self.wait(1.4)  # match STEP_LINGER, or tweak to taste
        
        self.play(FadeOut(atp, scale=0.85), run_time=0.25)
        self.play(FadeOut(hydro_cue, shift=UP*0.12), run_time=0.3)

        adp2_c.add_updater(lambda m: m.move_to(stem_anchor(+1)))
        pi2_c.add_updater(lambda m: m.move_to(stem_anchor(-1)))
        adp2_t.add_updater(lambda m: m.move_to(adp2_c.get_center()))
        pi2_t.add_updater(lambda m: m.move_to(pi2_c.get_center()))

        # -------- EXTRA: simplified loop + stop --------

        # 8) Cycle continues?
        cue_step(self, "Cycle continues?", anchor=actin, direction=UP, linger=1.4)

        # 9) Re-bind to actin again (binding only, no second stroke)
        target_bead2, unlock_bulb2, unlock_stem2 = bind_head_to_actin_vertical(
            self, backbone, stem, bulb, left_strand, right_strand,
            CONTACT_OVERLAP=0.08, APPROACH_GAP=0.05, APPROACH_TIME=0.6, BIND_SNAP_TIME=0.25
        )

        cue_step(
            self,
            "As long as muscle fibre is stimulated\nby nerve impulses",
            anchor=actin,
            direction=UP,
            linger=1.4
        )

                # 10) Cycle stops
        cue_step(self, "Cycle stops", anchor=actin, direction=UP, linger=1.4)
        
        # Release bind updaters and return head + sarcomere inset to relaxed state
        unlock_bulb2()
        unlock_stem2()
        pivot_relax = backbone.get_center() + np.array([0.0, backbone.height/2, 0.0])
        def _lock_stem_relax(_m): stem.put_start_and_end_on(pivot_relax, bulb.get_center())
        stem.add_updater(_lock_stem_relax)
        self.play(
            bulb.animate.move_to(initial_bulb_pos),
            sarco["actin_left"].animate.shift(LEFT * INSET_SLIDE),
            sarco["actin_right"].animate.shift(RIGHT * INSET_SLIDE),
            run_time=1.0,
            rate_func=smooth
        )
        stem.remove_updater(_lock_stem_relax)

        # ---- UPDATED Ca2+ RETURN WITH LABELS & ATP ----
        self.play(sr_group.animate.set_opacity(1), run_time=1.0)

        # Make Ca2+ label follow the dot on the way back
        ca_dot.clear_updaters()
        ca_return_label = Text("Ca²⁺", font_size=CA_FONT, color=CA_TEXT_COLOR).set_z_index(30)
        ca_return_label.next_to(ca_dot, DOWN, buff=0.1)
        ca_return_label.add_updater(lambda m: m.next_to(ca_dot, DOWN, buff=0.1))
        
        # Send Ca2+ to the edge of the sarcoplasmic reticulum (right edge, slightly down)
        sr_target = sr_box.get_right() + DOWN*0.05
        
        mid_back = (ca_dot.get_center() + sr_target)/2 + UP*0.6
        ca_back_path = VMobject()
        ca_back_path.set_points_smoothly(
            np.array([
                ca_dot.get_center(),
                mid_back,
                sr_target
            ])
        )

        # ATP label along the path (pump uses ATP)
        atp_transport = Text("Active transport", font_size=24, color=YELLOW).set_z_index(85)
        atp_transport.move_to(mid_back + UP*0.2)

        self.add(ca_return_label, atp_transport)
        self.bring_to_front(ca_dot, ca_return_label, atp_transport)

        # Slower return to emphasise active transport
        self.play(MoveAlongPath(ca_dot, ca_back_path), run_time=5.0, rate_func=smooth)
        self.play(FadeOut(atp_transport), run_time=0.4)
        self.play(FadeOut(ca_dot), FadeOut(ca_return_label), run_time=0.4)

        self.wait(2)
