"""SubstitutionExamplesAligned

Converted from notebooks/mutations-addition-deletion-substitution.ipynb (code unchanged apart from removing the notebook-only lines).

Render (from the repo folder, in the manim-env environment):
    python -m manim -ql scenes/mutation_substitution.py SubstitutionExamplesAligned     # quick preview (480p)
    python -m manim -qh scenes/mutation_substitution.py SubstitutionExamplesAligned     # final video (1080p)
"""
from manim import *

# ============================================================
# Helpers
# ============================================================

DNA_TEMPLATE_TO_MRNA = {"A": "U", "T": "A", "C": "G", "G": "C"}

def transcribe_template_dna_to_mrna(dna: str) -> str:
    dna = dna.replace(" ", "").upper()
    return "".join(DNA_TEMPLATE_TO_MRNA[b] for b in dna)

# Minimal table covering the codons used here + Stop codons
RNA_CODON_TABLE = {
    "UAU": "Tyr", "UAC": "Tyr",
    "CGU": "Arg", "CGC": "Arg", "CGA": "Arg", "CGG": "Arg",
    "ACU": "Thr", "ACC": "Thr", "ACA": "Thr", "ACG": "Thr",
    "AGU": "Ser", "AGC": "Ser",
    "UCU": "Ser", "UCC": "Ser", "UCA": "Ser", "UCG": "Ser",
    "UAA": "Stop", "UAG": "Stop", "UGA": "Stop",
}

def translate_mrna(mrna: str, truncate_at_stop: bool = True):
    mrna = mrna.replace(" ", "").upper()
    aas = []
    for i in range(0, len(mrna) - 2, 3):
        aa = RNA_CODON_TABLE.get(mrna[i:i+3], "?")
        aas.append(aa)
        if truncate_at_stop and aa == "Stop":
            break
    return aas

def substitute_base(seq: str, index: int, new_base: str) -> str:
    seq = seq.replace(" ", "").upper()
    return seq[:index] + new_base.upper() + seq[index+1:]


def substitution_arrow(target_text: Mobject) -> Arrow:
    """Large, obvious arrow pointing at substituted nucleotide."""
    top = target_text.get_center() + UP * 0.9
    bottom = target_text.get_center() + UP * 0.15
    arrow = Arrow(
        start=top,
        end=bottom,
        buff=0.0,
        max_tip_length_to_length_ratio=0.45
    )
    arrow.set_stroke(width=4)
    arrow.set_color(RED)
    return arrow


# ============================================================
# Visual rows
# ============================================================

class BaseRow(VGroup):
    def __init__(self, bases, label, y, highlight_index=None):
        super().__init__()
        self.bases = bases.replace(" ", "").upper()
        self.y = y
        self.spacing = 0.62
        self.highlight_index = highlight_index
        self._build(label)

    def _build(self, label):
        x0 = -self.spacing * (len(self.bases) - 1) / 2
        self.letter_texts = []

        backbone = Line([x0 - 0.5, self.y, 0],
                        [x0 + self.spacing * (len(self.bases) - 1) + 0.5, self.y, 0])
        ticks, letters = VGroup(), VGroup()

        for i, b in enumerate(self.bases):
            x = x0 + i * self.spacing
            tick = Line([x, self.y, 0], [x, self.y + 0.18, 0])
            txt = Text(b, font_size=28).next_to(tick, UP, buff=0.05)
            if i == self.highlight_index:
                txt.set_color(RED)
            ticks.add(tick)
            letters.add(txt)
            self.letter_texts.append(txt)

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
        aas = translate_mrna(mrna, truncate_at_stop=True)
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


def build_rows(dna, center, highlight_index=None, aa_changed=None):
    dna = dna.replace(" ", "").upper()
    mrna = transcribe_template_dna_to_mrna(dna)

    dna_y, mrna_y, aa_y = center[1] + 1.35, center[1] + 0.25, center[1] - 0.90
    dna_row = BaseRow(dna, "DNA (template)", dna_y, highlight_index)
    mrna_row = BaseRow(mrna, "mRNA", mrna_y, highlight_index)
    aa_row = AminoAcidRow(mrna, aa_y, mrna_row, aa_changed, mrna_row.label.get_center()[0])
    return dna_row, mrna_row, aa_row


# ============================================================
# Scene (3 examples: silent -> missense -> nonsense)
# ============================================================

class SubstitutionExamplesAligned(Scene):
    def construct(self):
        header = Text("Original sequence", font_size=34).to_edge(UP)
        self.play(FadeIn(header))

        dna0 = "ATAGCATGA"
        dna_row0, mrna_row0, aa_row0 = build_rows(dna0, DOWN * 0.35)
        original_mrna = transcribe_template_dna_to_mrna(dna0)
        original_aas = translate_mrna(original_mrna, truncate_at_stop=True)

        # Appear in order: DNA -> mRNA -> amino acids
        self.play(FadeIn(dna_row0))
        self.wait(0.25)
        self.play(FadeIn(mrna_row0))
        self.wait(0.25)
        self.play(FadeIn(aa_row0))
        self.wait(0.8)

        # Helper to reset to original rows (keeps positions consistent)
        def reset_from(current_dna, current_mrna, current_aa):
            new_dna, new_mrna, new_aa = build_rows(dna0, DOWN * 0.35)
            self.play(
                ReplacementTransform(current_dna, new_dna),
                ReplacementTransform(current_mrna, new_mrna),
                ReplacementTransform(current_aa, new_aa),
                run_time=1.0
            )
            self.wait(0.3)
            return new_dna, new_mrna, new_aa

        # --------------------------------------------------
        # Example 1: Silent (AAs unchanged)
        # DNA index 2: A -> G makes mRNA UAU -> UAC (Tyr stays Tyr)
        # --------------------------------------------------
        self.play(Transform(header, Text("Example 1: Substitution (silent)", font_size=34).to_edge(UP)))

        idx, new_base = 2, "G"
        arrow = substitution_arrow(dna_row0.letter_texts[idx])
        self.play(FadeIn(arrow))
        self.wait(0.3)

        dna1 = substitute_base(dna0, idx, new_base)
        mrna1 = transcribe_template_dna_to_mrna(dna1)
        aas1 = translate_mrna(mrna1, truncate_at_stop=True)

        codon_i = idx // 3
        changed = set()  # silent -> no AA box highlight
        dna_row1, mrna_row1, aa_row1 = build_rows(dna1, DOWN * 0.35, highlight_index=idx, aa_changed=changed)

        self.play(
            ReplacementTransform(dna_row0, dna_row1),
            ReplacementTransform(mrna_row0, mrna_row1),
            ReplacementTransform(aa_row0, aa_row1),
            FadeOut(arrow),
            run_time=1.6
        )

        silent_text = Text(
            f"Silent: amino acid {original_aas[codon_i]} stays the same",
            font_size=26
        ).to_edge(DOWN)
        self.play(FadeIn(silent_text))
        self.wait(3.0)
        self.play(FadeOut(silent_text))

        dna_row0, mrna_row0, aa_row0 = reset_from(dna_row1, mrna_row1, aa_row1)

        # --------------------------------------------------
        # Example 2: Missense (AA changes)
        # DNA index 3: G -> T makes mRNA CGU -> AGU (Arg -> Ser)
        # --------------------------------------------------
        self.play(Transform(header, Text("Example 2: Substitution (missense)", font_size=34).to_edge(UP)))

        idx, new_base = 3, "T"
        arrow = substitution_arrow(dna_row0.letter_texts[idx])
        self.play(FadeIn(arrow))
        self.wait(0.3)

        dna2 = substitute_base(dna0, idx, new_base)
        mrna2 = transcribe_template_dna_to_mrna(dna2)
        aas2 = translate_mrna(mrna2, truncate_at_stop=True)

        # highlight changed codon box
        changed2 = {i for i in range(min(len(original_aas), len(aas2))) if aas2[i] != original_aas[i]}
        # if lengths differ (shouldn't here), mark extras too
        changed2 |= set(range(min(len(original_aas), len(aas2)), max(len(original_aas), len(aas2))))

        dna_row2, mrna_row2, aa_row2 = build_rows(dna2, DOWN * 0.35, highlight_index=idx, aa_changed=changed2)

        self.play(
            ReplacementTransform(dna_row0, dna_row2),
            ReplacementTransform(mrna_row0, mrna_row2),
            ReplacementTransform(aa_row0, aa_row2),
            FadeOut(arrow),
            run_time=1.6
        )

        miss_i = idx // 3
        missense_text = Text(
            f"Missense: {original_aas[miss_i]} → {aas2[miss_i]}",
            font_size=26
        ).to_edge(DOWN)
        self.play(FadeIn(missense_text))
        self.wait(3.0)
        self.play(FadeOut(missense_text))

        dna_row0, mrna_row0, aa_row0 = reset_from(dna_row2, mrna_row2, aa_row2)

        # --------------------------------------------------
        # Example 3: Nonsense (Stop)
        # DNA index 2: A -> T makes mRNA UAU -> UAA (Tyr -> Stop)
        # --------------------------------------------------
        self.play(Transform(header, Text("Example 3: Substitution (nonsense)", font_size=34).to_edge(UP)))

        idx, new_base = 2, "T"
        arrow = substitution_arrow(dna_row0.letter_texts[idx])
        self.play(FadeIn(arrow))
        self.wait(0.3)

        dna3 = substitute_base(dna0, idx, new_base)
        mrna3 = transcribe_template_dna_to_mrna(dna3)
        aas3 = translate_mrna(mrna3, truncate_at_stop=True)  # will stop at Stop

        # highlight the codon that became Stop (first codon here)
        nonsense_i = idx // 3
        changed3 = {nonsense_i}

        dna_row3, mrna_row3, aa_row3 = build_rows(dna3, DOWN * 0.35, highlight_index=idx, aa_changed=changed3)

        self.play(
            ReplacementTransform(dna_row0, dna_row3),
            ReplacementTransform(mrna_row0, mrna_row3),
            ReplacementTransform(aa_row0, aa_row3),
            FadeOut(arrow),
            run_time=1.6
        )

        nonsense_text = Text(
            f"Nonsense: {original_aas[nonsense_i]} → Stop (translation ends early)",
            font_size=26
        ).to_edge(DOWN)
        self.play(FadeIn(nonsense_text))
        self.wait(3.2)
        self.play(FadeOut(nonsense_text))

        self.wait(0.6)
