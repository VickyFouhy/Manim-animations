# Manim Biology

Testing animations for A-level Biology, made with [Manim](https://www.manim.community/). Each file in `scenes/` renders one animation, and each file in `slides/` renders a step-by-step animation for the website. 

This repo holds the code only. Rendered videos are not stored here: run a scene to make them.

## Animations

| File | Topic | Scene |
|---|---|---|
| `scenes/action_potential.py` | Nerve impulses | `ActionPotentialFull` |
| `scenes/synapse_neuromuscular_junction.py` | Cholinergic synapse at a neuromuscular junction | `Synapse_Receptors_DownAP_SR_Sized_WithSarcomereRight_Anim` |
| `scenes/sarcomere_contraction.py` | Sarcomere contraction | `Sarcomere_Contraction` |
| `scenes/sliding_filament.py` | Sliding filament theory | `LFilament_CaBind_TMBack_OvalHead` |
| `scenes/mutation_addition.py` | Gene mutations | `AdditionFrameshiftAligned` |
| `scenes/mutation_deletion.py` | Gene mutations | `DeletionExampleAligned` |
| `scenes/mutation_substitution.py` | Gene mutations | `SubstitutionExamplesAligned` |
| `scenes/mutation_duplication.py` | Gene mutations | `DuplicationExampleAligned` |
| `scenes/mutation_inversion.py` | Gene mutations | `InversionExampleAligned` |
| `scenes/mutation_translocation.py` | Gene mutations | `TranslocationTwoExamplesAnimatedOnly` |

## Setup (once)

You need [conda](https://docs.conda.io/) (for example Anaconda or Miniconda) and [ffmpeg](https://ffmpeg.org/). On a Mac with Homebrew: `brew install ffmpeg`. None of the scenes need LaTeX.

```bash
git clone https://github.com/VickyFouhy/Manim-animations.git
cd Manim-animations
conda create -n manim-env python=3.10
conda activate manim-env
pip install -r requirements.txt
```

## Running an animation

From the repo folder:

```bash
conda activate manim-env
python -m manim -pql scenes/action_potential.py ActionPotentialFull
```

The first part is the file, the last part is the scene name (from the table above, or the first line of each file). `-p` opens the video when it finishes (leave it out to just save it). Videos are saved in `media/videos/`, which git ignores.

Use `python -m manim`, not plain `manim`: in this environment the plain `manim` command runs ManimGL, a different version that can't run these files.

### Quality

| Flag | Quality | Use |
|---|---|---|
| `-ql` | 480p, 15 fps | checking and previews (fast) |
| `-qm` | 720p, 30 fps | the website's step-by-step slides |
| `-qh` | 1080p, 60 fps | final video |
| `-qk` | 4K, 60 fps | final video (slow) |

Add `-s` to render only the last frame as a still image, which is useful for checking layout. Add `-v WARNING` to hide Manim's progress log.

## Slides (step-by-step animations)

`slides/` holds animations made with [Manim Slides](https://manim-slides.eertmans.be/): the animation pauses after each step and the student clicks to continue. They are exported as a single HTML file for the website.

| File | Topic | Scene | On the website |
|---|---|---|---|
| `slides/action_potential_slides.py` | Nerve impulses | `ActionPotentialSlides` | Nerve Impulses page (`static/animations/action-potential.html` in BiologyNotes) |
| `slides/synapse_slides.py` | Neuromuscular junction | `SynapseSlides` | Not yet |

`synapse_slides.py` reuses the animation in `scenes/synapse_neuromuscular_junction.py` (black background), so changes to that scene show up in both.

To render and export (16:10; swap in the file, scene and HTML names for other slides):

```bash
conda activate manim-env
cd slides
manim-slides render -qm action_potential_slides.py ActionPotentialSlides
manim-slides convert --one-file -ccontrols=true -cprogress=true -cslide_number=true ActionPotentialSlides action-potential.html
```

`-ccontrols=true` shows the on-screen arrows (they're off by default). Copy the HTML into BiologyNotes at `static/animations/`. To try changes on the site first, put it in `static/_test/`, which BiologyNotes git-ignores. The rendered clips (`slides/slides/`) and exported HTML are git-ignored here.

## Images

The sarcomere animation can show an arm contracting, using two images (`scenes/assets/arm_s.png` and `arm_f.png`). They are from Canva, so they are not included here. Without them, the animation runs as normal with no arm.
