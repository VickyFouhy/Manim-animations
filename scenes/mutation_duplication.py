"""DuplicationExampleAligned

Converted from notebooks/mutations-duplication-inversion-translocation.ipynb (code unchanged apart from removing the notebook-only lines).

Render (from the repo folder, in the manim-env environment):
    python -m manim -ql scenes/mutation_duplication.py DuplicationExampleAligned     # quick preview (480p)
    python -m manim -qh scenes/mutation_duplication.py DuplicationExampleAligned     # final video (1080p)
"""
from manim import *

# ============================================================
# Helpers
# ============================================================

DNA_TEMPLATE_TO_MRNA = {"A": "U", "T": "A", "C": "G", "G": "C"}

def transcribe_template_dna_to_mrna(dna: str) -> str:
    dna = dna.replace(" ", "").upper()
    return "".join(DNA_TEMPLATE_TO_MRNA[b] for b in dna)

# FULL genetic code (no unknown amino acids)
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

def translate_mrna(mrna: str, truncate_at_stop: bool = False):
    mrna = mrna.replace(" ", "").upper()
    aas = []
    for i in range(0, len(mrna) - 2, 3):
        codon = mrna[i:i+3]
        aa = RNA_CODON_TABLE[codon]
        aas.append(aa)
        if truncate_at_stop and aa == "Stop":
            break
    return aas

def duplicate_bases(seq: str, start: int, length: int) -> str:
    """Duplicate a DNA segment starting at index (frameshift if length not multiple of 3)."""
    seq = seq.replace(" ", "").upper()
    segment = seq[start:start+length]
    return seq[:start+length] + segment + seq[start+length:]


# ============================================================
# Visual rows (same style as other animations)
# ============================================================

class BaseRow(VGroup):
    def __init__(self, bases, label, y, highlight_range=None):
        super().__init__()
        self.bases = bases.replace(" ", "").upper()
        self.y = y
        self.spacing = 0.62
        self.highlight_range = highlight_range
        self._build(label)

    def _build(self, label):
        x0 = -self.spacing * (len(self.bases) - 1) / 2
        self.letter_texts = []

        backbone = Line(
            [x0 - 0.5, self.y, 0],
            [x0 + self.spacing * (len(self.bases) - 1) + 0.5, self.y, 0]
        )

        ticks, letters = VGroup(), VGroup()

        for i, b in enumerate(self.bases):
            x = x0 + i * self.spacing
            tick = Line([x, self.y, 0], [x, self.y + 0.18, 0])
            txt = Text(b, font_size=28).next_to(tick, UP, buff=0.05)

            if self.highlight_range and i in self.highlight_range:
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


class AminoAcidRow(VGroup):
    def __init__(self, mrna, y, mrna_row, changed=None, label_x=None):
        super().__init__()
        aas = translate_mrna(mrna, truncate_at_stop=False)
        self.amino_acids = aas
        self.boxes = VGroup()
        self.labels = VGroup()

        for i, aa in enumerate(aas):
            x = mrna_row.codon_boxes[i].get_center()[0]
            box = RoundedRectangle(width=0.95, height=0.52, corner_radius=0.12)
            box.move_to([x, y, 0])

            if changed and i in changed:
                box.set_fill(YELLOW, opacity=0.6)
                box.set_stroke(YELLOW, width=3)

            self.boxes.add(box)
            self.labels.add(Text(aa, font_size=22).move_to(box))

        label = Text("Amino\nacid", font_size=24, line_spacing=0.9)
        label.move_to([label_x, y, 0]).shift(LEFT * 0.1)
        self.add(self.boxes, self.labels, label)


def build_rows(dna, center, highlight_range=None, aa_changed=None):
    dna = dna.replace(" ", "").upper()
    mrna = transcribe_template_dna_to_mrna(dna)

    dna_y, mrna_y, aa_y = center[1] + 1.35, center[1] + 0.25, center[1] - 0.90
    dna_row = BaseRow(dna, "DNA (template)", dna_y, highlight_range)
    mrna_row = BaseRow(mrna, "mRNA", mrna_y, highlight_range)
    aa_row = AminoAcidRow(mrna, aa_y, mrna_row, aa_changed, mrna_row.label.get_center()[0])
    return dna_row, mrna_row, aa_row


# ============================================================
# Scene: Duplication (frameshift)
# ============================================================

class DuplicationExampleAligned(Scene):
    def construct(self):
        header = Text("Original sequence", font_size=34).to_edge(UP)
        self.play(FadeIn(header))

        dna0 = "ATAGCATGA"
        dna_row0, mrna_row0, aa_row0 = build_rows(dna0, DOWN * 0.35)
        original_aas = aa_row0.amino_acids

        self.play(FadeIn(dna_row0))
        self.play(FadeIn(mrna_row0))
        self.play(FadeIn(aa_row0))
        self.wait(0.8)

        # --------------------------------------------------
        # Duplication example (frameshift)
        # --------------------------------------------------
        self.play(Transform(header, Text("Duplication", font_size=34).to_edge(UP)))

        dup_start = 2
        dup_length = 1  # single-base duplication → frameshift
        highlight_range = range(dup_start, dup_start + dup_length)

        # Highlight duplicated base
        dna_row_high, mrna_row_high, aa_row_high = build_rows(
            dna0, DOWN * 0.35, highlight_range=highlight_range
        )

        self.play(
            ReplacementTransform(dna_row0, dna_row_high),
            ReplacementTransform(mrna_row0, mrna_row_high),
            ReplacementTransform(aa_row0, aa_row_high),
            run_time=1.2
        )
        self.wait(0.4)

        # Perform duplication
        dna_new = duplicate_bases(dna0, dup_start, dup_length)
        mrna_new = transcribe_template_dna_to_mrna(dna_new)
        aas_new = translate_mrna(mrna_new, truncate_at_stop=False)

        changed = {i for i in range(len(aas_new)) if i >= len(original_aas) or aas_new[i] != original_aas[i]}

        dna_row_new, mrna_row_new, aa_row_new = build_rows(
            dna_new, DOWN * 0.35, highlight_range=highlight_range, aa_changed=changed
        )

        self.play(
            ReplacementTransform(dna_row_high, dna_row_new),
            ReplacementTransform(mrna_row_high, mrna_row_new),
            ReplacementTransform(aa_row_high, aa_row_new),
            run_time=1.8
        )

        text = Text(
            "Duplicated base causes a frameshift → downstream amino acids change",
            font_size=26
        ).to_edge(DOWN)

        self.play(FadeIn(text))
        self.wait(4.0)
