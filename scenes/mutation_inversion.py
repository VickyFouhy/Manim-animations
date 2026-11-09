"""InversionExampleAligned

Converted from notebooks/mutations-duplication-inversion-translocation.ipynb (code unchanged apart from removing the notebook-only lines).

Render (from the repo folder, in the manim-env environment):
    python -m manim -ql scenes/mutation_inversion.py InversionExampleAligned     # quick preview (480p)
    python -m manim -qh scenes/mutation_inversion.py InversionExampleAligned     # final video (1080p)
"""
from manim import *

# ============================================================
# Helpers: transcription & translation
# ============================================================

DNA_TEMPLATE_TO_MRNA = {"A": "U", "T": "A", "C": "G", "G": "C"}

def transcribe_template_dna_to_mrna(dna_template: str) -> str:
    dna_template = dna_template.replace(" ", "").upper()
    return "".join(DNA_TEMPLATE_TO_MRNA[b] for b in dna_template)

RNA_CODON_TABLE = {
    # U
    "UUU":"Phe","UUC":"Phe","UUA":"Leu","UUG":"Leu",
    "UCU":"Ser","UCC":"Ser","UCA":"Ser","UCG":"Ser",
    "UAU":"Tyr","UAC":"Tyr","UAA":"Stop","UAG":"Stop",
    "UGU":"Cys","UGC":"Cys","UGA":"Stop","UGG":"Trp",
    # C
    "CUU":"Leu","CUC":"Leu","CUA":"Leu","CUG":"Leu",
    "CCU":"Pro","CCC":"Pro","CCA":"Pro","CCG":"Pro",
    "CAU":"His","CAC":"His","CAA":"Gln","CAG":"Gln",
    "CGU":"Arg","CGC":"Arg","CGA":"Arg","CGG":"Arg",
    # A
    "AUU":"Ile","AUC":"Ile","AUA":"Ile","AUG":"Met",
    "ACU":"Thr","ACC":"Thr","ACA":"Thr","ACG":"Thr",
    "AAU":"Asn","AAC":"Asn","AAA":"Lys","AAG":"Lys",
    "AGU":"Ser","AGC":"Ser","AGA":"Arg","AGG":"Arg",
    # G
    "GUU":"Val","GUC":"Val","GUA":"Val","GUG":"Val",
    "GCU":"Ala","GCC":"Ala","GCA":"Ala","GCG":"Ala",
    "GAU":"Asp","GAC":"Asp","GAA":"Glu","GAG":"Glu",
    "GGU":"Gly","GGC":"Gly","GGA":"Gly","GGG":"Gly",
}

def translate_mrna_to_aas(mrna: str, truncate_at_stop: bool = True):
    mrna = mrna.replace(" ", "").upper()
    aas = []
    for i in range(0, len(mrna) - 2, 3):
        aa = RNA_CODON_TABLE[mrna[i:i+3]]
        aas.append(aa)
        if truncate_at_stop and aa == "Stop":
            break
    return aas

def invert_segment(seq: str, start: int, length: int) -> str:
    seq = seq.replace(" ", "").upper()
    seg = seq[start:start+length]
    return seq[:start] + seg[::-1] + seq[start+length:]


# ============================================================
# Visual components (unchanged)
# ============================================================

class BaseRow(VGroup):
    def __init__(self, bases, label, y, highlight_range=None):
        super().__init__()
        self.bases = bases.replace(" ", "").upper()
        self.y = y
        self.spacing = 0.62
        self.highlight_range = set(highlight_range) if highlight_range else set()
        self._build(label)

    def _build(self, label):
        x0 = -self.spacing * (len(self.bases) - 1) / 2
        self.letter_texts = []

        backbone = Line([x0 - 0.5, self.y, 0],
                        [x0 + self.spacing*(len(self.bases)-1) + 0.5, self.y, 0])

        ticks, letters = VGroup(), VGroup()

        for i, b in enumerate(self.bases):
            x = x0 + i * self.spacing
            tick = Line([x, self.y, 0], [x, self.y + 0.18, 0])
            txt = Text(b, font_size=28).next_to(tick, UP, buff=0.05)

            if i in self.highlight_range:
                txt.set_color(RED)
                box = SurroundingRectangle(txt, buff=0.06, corner_radius=0.08)
                box.set_stroke(RED, width=3)
                letters.add(VGroup(txt, box))
            else:
                letters.add(txt)

            self.letter_texts.append(txt)
            ticks.add(tick)

        codon_boxes = VGroup()
        for i in range(0, len(self.bases), 3):
            if i + 2 < len(self.bases):
                codon_boxes.add(
                    SurroundingRectangle(
                        VGroup(*self.letter_texts[i:i+3]),
                        buff=0.11,
                        corner_radius=0.10
                    )
                )

        label_txt = Text(label, font_size=26).next_to(backbone, LEFT, buff=0.65)
        self.add(backbone, ticks, letters, codon_boxes, label_txt)
        self.codon_boxes = codon_boxes
        self.label = label_txt

    def segment_center(self, start, length):
        return (self.letter_texts[start].get_center() +
                self.letter_texts[start+length-1].get_center()) / 2


class AminoAcidRow(VGroup):
    def __init__(self, mrna, y, mrna_row, changed=None, label_x=None):
        super().__init__()
        aas = translate_mrna_to_aas(mrna)
        self.boxes, self.labels = VGroup(), VGroup()

        for i, aa in enumerate(aas):
            x = mrna_row.codon_boxes[i].get_center()[0]
            box = RoundedRectangle(width=0.95, height=0.52, corner_radius=0.12).move_to([x, y, 0])
            if changed and i in changed:
                box.set_fill(YELLOW, opacity=0.6)
                box.set_stroke(YELLOW, width=3)
            self.boxes.add(box)
            self.labels.add(Text(aa, font_size=22).move_to(box))

        label = Text("Amino\nacid", font_size=24)
        label.move_to([label_x, y, 0]).shift(LEFT * 0.1)
        self.add(self.boxes, self.labels, label)


def build_rows(dna, center, highlight_range=None, aa_changed=None):
    mrna = transcribe_template_dna_to_mrna(dna)
    dna_y, mrna_y, aa_y = center[1] + 1.35, center[1] + 0.25, center[1] - 0.90
    dna_row = BaseRow(dna, "DNA (template)", dna_y, highlight_range)
    mrna_row = BaseRow(mrna, "mRNA", mrna_y, highlight_range)
    aa_row = AminoAcidRow(mrna, aa_y, mrna_row, aa_changed, mrna_row.label.get_center()[0])
    return dna_row, mrna_row, aa_row


# ============================================================
# Scene: Inversion (slowed inversion section)
# ============================================================

class InversionExampleAligned(Scene):
    def construct(self):
        header = Text("Original sequence", font_size=34).to_edge(UP)
        self.play(FadeIn(header))

        dna0 = "ATAGCATGA"
        dna_row0, mrna_row0, aa_row0 = build_rows(dna0, DOWN * 0.35)

        self.play(FadeIn(dna_row0))
        self.wait(0.25)
        self.play(FadeIn(mrna_row0))
        self.wait(0.25)
        self.play(FadeIn(aa_row0))
        self.wait(0.8)

        self.play(Transform(header, Text("Example: Inversion", font_size=34).to_edge(UP)))

        start, length = 3, 3
        highlight = range(start, start + length)

        dna_row_h, mrna_row_h, aa_row_h = build_rows(dna0, DOWN * 0.35, highlight)
        self.play(
            ReplacementTransform(dna_row0, dna_row_h),
            ReplacementTransform(mrna_row0, mrna_row_h),
            ReplacementTransform(aa_row0, aa_row_h),
            run_time=1.4
        )
        self.wait(0.8)

        seg = dna0[start:start+length]
        center = dna_row_h.segment_center(start, length)

        seg_letters = VGroup(*[Text(c, font_size=38).set_color(RED) for c in seg])
        seg_letters.arrange(RIGHT, buff=0.18).move_to(center + UP*1.0)

        arrow = Arrow(center + UP*0.75, center + UP*0.3)

        self.play(FadeIn(seg_letters), GrowArrow(arrow), run_time=1.2)
        self.wait(0.8)

        self.play(Rotate(seg_letters, PI), run_time=1.0)
        self.wait(0.6)

        seg_rev = VGroup(*[Text(c, font_size=38).set_color(RED) for c in seg[::-1]])
        seg_rev.arrange(RIGHT, buff=0.18).move_to(seg_letters.get_center())

        self.play(Transform(seg_letters, seg_rev), run_time=0.8)
        self.wait(0.6)

        dna_new = invert_segment(dna0, start, length)
        mrna_new = transcribe_template_dna_to_mrna(dna_new)
        aas_old = translate_mrna_to_aas(transcribe_template_dna_to_mrna(dna0))
        aas_new = translate_mrna_to_aas(mrna_new)
        changed = {i for i in range(len(aas_new)) if aas_new[i] != aas_old[i]}

        dna_row_n, mrna_row_n, aa_row_n = build_rows(dna_new, DOWN * 0.35, highlight, changed)

        self.play(
            seg_letters.animate.move_to(center + UP*1.0),
            FadeOut(arrow),
            run_time=0.8
        )
        self.wait(0.4)

        self.play(
            ReplacementTransform(dna_row_h, dna_row_n),
            ReplacementTransform(mrna_row_h, mrna_row_n),
            ReplacementTransform(aa_row_h, aa_row_n),
            run_time=1.6
        )

        self.wait(0.6)
        self.play(FadeOut(seg_letters), run_time=0.4)

        note = Text("Inversion flips a DNA segment → amino acids may change", font_size=24).to_edge(DOWN)
        self.play(FadeIn(note))
        self.wait(1.2)
        self.play(FadeOut(note))
        self.wait(0.6)
