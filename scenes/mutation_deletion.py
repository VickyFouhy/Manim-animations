"""DeletionExampleAligned

Converted from notebooks/mutations-addition-deletion-substitution.ipynb (code unchanged apart from removing the notebook-only lines).

Render (from the repo folder, in the manim-env environment):
    python -m manim -ql scenes/mutation_deletion.py DeletionExampleAligned     # quick preview (480p)
    python -m manim -qh scenes/mutation_deletion.py DeletionExampleAligned     # final video (1080p)
"""
from manim import *

# ============================================================
# Helpers: transcription & translation
# ============================================================

DNA_TEMPLATE_TO_MRNA = {"A": "U", "T": "A", "C": "G", "G": "C"}

def transcribe_template_dna_to_mrna(dna_template: str) -> str:
    dna_template = dna_template.replace(" ", "").upper()
    return "".join(DNA_TEMPLATE_TO_MRNA[b] for b in dna_template)

# Full RNA codon table (3-letter amino acids); Stop included (we won't focus on stop here)
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

def translate_mrna_to_aas(mrna: str, truncate_at_stop: bool = False):
    """
    For the deletion demo, we DON'T want stop-codon behaviour to dominate,
    so default truncate_at_stop=False (translate all complete codons).
    """
    mrna = mrna.replace(" ", "").upper()
    aas = []
    for i in range(0, len(mrna) - 2, 3):
        codon = mrna[i:i+3]
        aa = RNA_CODON_TABLE.get(codon, "?")
        aas.append(aa)
        if truncate_at_stop and aa == "Stop":
            break
    return aas

def delete_base(seq: str, index: int) -> str:
    seq = seq.replace(" ", "").upper()
    if index < 0 or index >= len(seq):
        return seq
    return seq[:index] + seq[index+1:]


# ============================================================
# Visual components (same look as your Addition version)
# ============================================================

class BaseRow(VGroup):
    def __init__(self, bases: str, label: str, y: float, highlight_index=None, highlight_color=RED):
        super().__init__()
        self.bases = bases.replace(" ", "").upper()
        self.label_text = label
        self.y = y
        self.highlight_index = highlight_index
        self.highlight_color = highlight_color
        self.spacing = 0.62
        self._build()

    def _wipe(self):
        if self.submobjects:
            self.remove(*self.submobjects)

    def _build(self):
        self._wipe()
        n = len(self.bases)
        x0 = -self.spacing * (n - 1) / 2 if n > 1 else 0

        self.backbone = Line([x0 - 0.5, self.y, 0], [x0 + self.spacing*(n-1) + 0.5, self.y, 0])

        self.ticks = VGroup()
        self.letters = VGroup()
        self.letter_texts = []

        for i, b in enumerate(self.bases):
            x = x0 + i * self.spacing
            tick = Line([x, self.y, 0], [x, self.y + 0.18, 0])
            txt = Text(b, font_size=28).next_to(tick, UP, buff=0.05)

            if self.highlight_index is not None and i == self.highlight_index:
                txt.set_color(self.highlight_color)
                box = SurroundingRectangle(txt, buff=0.06, corner_radius=0.08)
                box.set_stroke(self.highlight_color, width=3)
                box.set_fill(opacity=0)
                self.letters.add(VGroup(txt, box))
                self.letter_texts.append(txt)
            else:
                self.letters.add(txt)
                self.letter_texts.append(txt)

            self.ticks.add(tick)

        self.codon_boxes = VGroup()
        for i in range(0, n, 3):
            if i + 2 < n:
                grp = VGroup(*self.letter_texts[i:i+3])
                self.codon_boxes.add(SurroundingRectangle(grp, buff=0.11, corner_radius=0.10))

        self.label = Text(self.label_text, font_size=26).next_to(self.backbone, LEFT, buff=0.65)
        self.add(self.backbone, self.ticks, self.letters, self.codon_boxes, self.label)


class AminoAcidRow(VGroup):
    """
    Amino acids aligned DIRECTLY under mRNA codon boxes.
    Label: "Amino\nacid" aligned with mRNA label x.
    """
    def __init__(self, mrna: str, y: float, mrna_row: BaseRow, changed_indices=None, label_x=None):
        super().__init__()
        self.mrna = mrna.replace(" ", "").upper()
        self.y = y
        self.mrna_row = mrna_row
        self.changed_indices = changed_indices or set()
        self.label_x = label_x
        self._build()

    def _wipe(self):
        if self.submobjects:
            self.remove(*self.submobjects)

    def _build(self):
        self._wipe()

        aas = translate_mrna_to_aas(self.mrna, truncate_at_stop=False)
        self.amino_acids = aas

        self.boxes = VGroup()
        self.labels = VGroup()

        n = min(len(aas), len(self.mrna_row.codon_boxes))
        for i in range(n):
            x = self.mrna_row.codon_boxes[i].get_center()[0]
            rect = RoundedRectangle(width=0.95, height=0.52, corner_radius=0.12)
            rect.move_to([x, self.y, 0])

            if i in self.changed_indices:
                rect.set_fill(YELLOW, opacity=0.6)
                rect.set_stroke(YELLOW, width=3)

            txt = Text(aas[i], font_size=22).move_to(rect.get_center())
            self.boxes.add(rect)
            self.labels.add(txt)

        self.label = Text("Amino\nacid", font_size=24, line_spacing=0.9)
        if self.label_x is not None:
            self.label.move_to([self.label_x, self.y, 0]).shift(LEFT*0.1)
        elif len(self.boxes) > 0:
            self.label.next_to(self.boxes[0], LEFT, buff=0.75)

        self.add(self.boxes, self.labels, self.label)


def build_rows(dna_template: str, center=DOWN*0.35, highlight_index=None, aa_changed=None):
    dna_template = dna_template.replace(" ", "").upper()
    mrna = transcribe_template_dna_to_mrna(dna_template)

    dna_y  = center[1] + 1.35
    mrna_y = center[1] + 0.25
    aa_y   = mrna_y - 1.15

    dna_row = BaseRow(dna_template, "DNA (template)", y=dna_y, highlight_index=highlight_index)
    mrna_row = BaseRow(mrna, "mRNA", y=mrna_y, highlight_index=highlight_index)

    label_x = mrna_row.label.get_center()[0]
    aa_row = AminoAcidRow(mrna, y=aa_y, mrna_row=mrna_row, changed_indices=aa_changed or set(), label_x=label_x)

    return dna_row, mrna_row, aa_row


# ============================================================
# Scene: Deletion example (shift left)
# ============================================================

class DeletionExampleAligned(Scene):
    def construct(self):
        header = Text("Original Sequence", font_size=34).to_edge(UP)
        self.play(FadeIn(header, shift=DOWN*0.1))

        dna0 = "ATAGCATGA"
        dna_row0, mrna_row0, aa_row0 = build_rows(dna0, center=DOWN*0.35)
        original_aas = list(aa_row0.amino_acids)

        # Appear in order: DNA -> mRNA -> amino acids
        self.play(FadeIn(dna_row0))
        self.wait(0.25)
        self.play(FadeIn(mrna_row0))
        self.wait(0.25)
        self.play(FadeIn(aa_row0))
        self.wait(0.8)

        # Switch header
        self.play(Transform(header, Text("Deletion", font_size=34).to_edge(UP)))

        # Choose a deletion index (0-based)
        delete_index = 2  # delete the 3rd base
        deleted_base = dna0[delete_index]

        # Show the base being deleted hovering above its position (red)
        delete_pos = dna_row0.letter_texts[delete_index].get_center()
        hovering = Text(deleted_base, font_size=44).set_color(RED).move_to(delete_pos + UP*0.95)
        arrow = Arrow(delete_pos + UP*0.75, delete_pos + UP*0.25, buff=0.05).set_opacity(0.7)

        # Briefly highlight the base in the DNA row before deletion
        dna_row_high, mrna_row_high, aa_row_high = build_rows(
            dna0,
            center=DOWN*0.35,
            highlight_index=delete_index,
            aa_changed=set()
        )

        self.play(
            ReplacementTransform(dna_row0, dna_row_high),
            ReplacementTransform(mrna_row0, mrna_row_high),
            ReplacementTransform(aa_row0, aa_row_high),
            FadeIn(hovering, shift=DOWN*0.1),
            GrowArrow(arrow),
            run_time=1.2
        )
        self.wait(0.2)

        # Perform deletion
        dna_new = delete_base(dna0, delete_index)
        mrna_new = transcribe_template_dna_to_mrna(dna_new)
        new_aas = translate_mrna_to_aas(mrna_new, truncate_at_stop=False)

        changed = {i for i in range(len(new_aas)) if i >= len(original_aas) or new_aas[i] != original_aas[i]}

        dna_row_new, mrna_row_new, aa_row_new = build_rows(
            dna_new,
            center=DOWN*0.35,
            highlight_index=None,
            aa_changed=changed
        )

        # Animate: hovering base disappears, sequences shift LEFT via transform to shorter rows
        self.play(
            FadeOut(hovering),
            FadeOut(arrow),
            ReplacementTransform(dna_row_high, dna_row_new),
            ReplacementTransform(mrna_row_high, mrna_row_new),
            ReplacementTransform(aa_row_high, aa_row_new),
            run_time=1.8
        )

        # ---------------------------
        # NEW: explanatory text (bottom)
        # ---------------------------
        note = Text("Frameshift mutation → downstream amino acids change", font_size=24).to_edge(DOWN)
        self.play(FadeIn(note, shift=UP*0.1))
        self.wait(4.0)
        self.play(FadeOut(note))
        # ---------------------------

        self.wait(0.8)
