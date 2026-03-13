## Repository for personal website (ehulland.github.io)
### Quarto refactor of the academic pages version by [Stuart Geiger](https://github.com/staeiou) from the [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/), which is © 2016 Michael Rose and released under the MIT License. 

### Local script setup

If you run the helper scripts in `scripts/`, install Python dependencies first:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python scripts/build_site_pages.py
python scripts/generate_talks_geo.py
```

Organized into 6 sections with additional contact information on the landing page:
* About Me
* Publications
* Talks and Presentations
* Timeline Map
* Posts
* CV
