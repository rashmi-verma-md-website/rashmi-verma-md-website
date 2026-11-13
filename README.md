# Rashmi Verma, MD — website

Static site for Dr. Rashmi Verma's neuro-ophthalmology office.

- `build.py` holds all page content and settings (`CONFIG`: phone, fax, address, hours, waitlist form link).
- `assets/` holds the stylesheet, images and downloadable files.
- `site/` is the generated website. Cloudflare Pages serves this folder as is (no build command, output directory `site`).

To change something, edit `build.py`, run `python3 build.py`, and commit both the source and `site/`.
