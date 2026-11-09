"""Neuromuscular junction as click-through slides.

Reuses the animation in scenes/synapse_neuromuscular_junction.py, with:
- a pause (next_slide) after each label and each step, so the student clicks to continue
- the same colours as the video, on a black background

Render and export (from this folder, in the manim-env environment):
    manim-slides render -qm synapse_slides.py SynapseSlides
    manim-slides convert --one-file -ccontrols=true -cprogress=true -cslide_number=true SynapseSlides synapse.html
"""
import sys
from pathlib import Path

from manim import *
from manim_slides import Slide

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scenes"))
import synapse_neuromuscular_junction as synapse

# 16:10, the same shape as the action potential slides
config.pixel_width = 1280
config.pixel_height = 800
config.frame_width = 14.222
config.frame_height = 8.889

synapse.STEP_HOLD = 0.3   # captions stay until the click, so no need to hold before animating


class SynapseSlides(Slide, synapse.Synapse_Receptors_DownAP_SR_Sized_WithSarcomereRight_Anim):
    def end_step(self):
        self.next_slide()
