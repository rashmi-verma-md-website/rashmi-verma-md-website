#!/usr/bin/env python3
"""Builds the static site into ./site from the page content below.

Run:  python3 build.py
Every page shares the header, footer and styles. To change a phone number,
address or the waitlist form link, edit CONFIG and rebuild.
"""
import html
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")

CONFIG = {
    "name": "Rashmi Verma, MD",
    "tagline": "Neuro-Ophthalmology",
    "domain": "https://neuroophtho.com",
    "email": "info@neuroophtho.com",
    "phone": "",          # e.g. "(516) 555-0100" — leave empty to hide
    "fax": "",            # e.g. "(516) 555-0101" — leave empty to hide
    "address": "",        # keep empty: Vedant decided (2026-11-21) no street address on the site
    "hours": "",          # e.g. "Monday to Friday, 8:30 am to 5:00 pm"
    "opening": "",         # e.g. "January 2027"; empty shows "opening soon"
    # Google Form (from the practice's Google Workspace, covered by the BAA).
    # Leave empty to show the email fallback instead of a form button.
    "waitlist_form_url": "https://forms.gle/bexYWKG3Z68H5Tz46",
    "jobs_form_url": "https://forms.gle/1Eg6ckXyhyy7jyCj7",
    "npp_effective": "November 16, 2026",
    "legal_entity": "Rashmi Verma MD PLLC",   # PLLC legal name once formed
    "year": "2026",
}

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("conditions.html", "Conditions"),
    ("services.html", "Services"),
    ("new-patients.html", "New Patients"),
    ("for-physicians.html", "For Physicians"),
    ("contact.html", "Contact"),
]

LEGAL = [
    ("privacy.html", "Privacy Policy"),
    ("notice-of-privacy-practices.html", "Notice of Privacy Practices"),
    ("sms-terms.html", "SMS Terms"),
    ("nondiscrimination.html", "Nondiscrimination & Language Assistance"),
    ("accessibility.html", "Accessibility & Language Help"),
    ("good-faith-estimate.html", "Good Faith Estimate"),
]

e = html.escape


def contact_lines():
    c = CONFIG
    rows = []
    if c["phone"]:
        tel = "".join(ch for ch in c["phone"] if ch.isdigit())
        rows.append(f'<li><span>Phone</span><a href="tel:+1{tel}">{e(c["phone"])}</a></li>')
    if c["fax"]:
        rows.append(f'<li><span>Fax</span>{e(c["fax"])}</li>')
    rows.append(f'<li><span>Email</span><a href="mailto:{c["email"]}">{c["email"]}</a></li>')
    rows.append(
        f'<li><span>Address</span>{e(c["address"]) if c["address"] else "Opening soon on Long Island, New York"}</li>'
    )
    if c["hours"]:
        rows.append(f'<li><span>Hours</span>{e(c["hours"])}</li>')
    return '<ul class="contact-list">' + "".join(rows) + "</ul>"


def waitlist_cta(label="Join the Waitlist"):
    url = CONFIG["waitlist_form_url"]
    if url:
        return f'<a class="btn btn-primary" href="{e(url)}" target="_blank" rel="noopener">{label}</a>'
    return f'<a class="btn btn-primary" href="contact.html#waitlist">{label}</a>'


def language_taglines():
    """Free language help taglines (16 languages) from assets/language-taglines.html.
    The source has a "[practice phone] (TTY: 711)" placeholder in each line. Until
    CONFIG phone is set, the call sentence is dropped and the practice email is shown."""
    src = open(os.path.join(HERE, "assets", "language-taglines.html"), encoding="utf-8").read()
    phone = CONFIG["phone"]
    mail = f'<bdi dir="ltr"><a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a></bdi>'
    if phone:
        return src.replace("[practice phone]", e(phone))
    out = []
    for line in src.splitlines():
        i = line.find("<bdi")
        if line.startswith("<p ") and i != -1:
            head = line[:i]
            cut = max(head.rfind(t) + len(t) for t in (". ", "。", "। ", "۔ ") if head.rfind(t) != -1)
            if 'lang="en"' in line:
                line = head[:cut] + f"Email {mail} or ask our front desk.</p>"
            else:
                line = head[:cut].rstrip() + f" {mail}</p>"
        out.append(line)
    return "\n".join(out)


def page(filename, title, description, body, active=None):
    c = CONFIG
    nav = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV
    )
    legal = " · ".join(f'<a href="{h}">{l}</a>' for h, l in LEGAL)
    entity = f"{e(c['legal_entity'])} · " if c["legal_entity"] else ""
    full_title = f"{title} | {c['name']}" if filename != "index.html" else f"{c['name']} | Neuro-Ophthalmologist on Long Island, NY"
    canonical = f"{c['domain']}/{'' if filename == 'index.html' else filename}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Lora:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="banner">Opening soon on Long Island. We are not yet seeing patients. <a href="contact.html#waitlist">Join the waitlist</a> and we'll contact you when scheduling opens.</div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="wordmark" href="index.html"><span class="wm-name">{c['name']}</span><span class="wm-tag">{c['tagline']}</span></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="site-nav" aria-label="Main">{nav}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <p class="footer-name">{c['name']}</p>
      <p>Board-certified neurologist, fellowship-trained in neuro-ophthalmology and pediatric ophthalmology. Care for adults and children on Long Island, New York.</p>
    </div>
    <div>
      <p class="footer-head">Contact</p>
      {contact_lines()}
    </div>
    <div>
      <p class="footer-head">Careers</p>
      <p>We're hiring part-time ophthalmic technicians and front desk staff. <a href="careers.html">See open positions</a>.</p>
      <p class="footer-head">Emergencies</p>
      <p>For a severe headache, sudden vision loss, new double vision, or other sudden neurological symptoms, call 911 or go to the nearest emergency room.</p>
    </div>
  </div>
  <div class="wrap footer-legal">
    <p>{legal}</p>
    <p>© {c['year']} {entity}{c['name']}. This website is for general information and is not medical advice.</p>
  </div>
</footer>
<script>
(function(){{var b=document.querySelector('.menu-toggle'),n=document.getElementById('site-nav');
if(b)b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}});}})();
</script>
</body>
</html>
"""


def cta_band(heading, text, button=None):
    button = button or waitlist_cta()
    return f"""<section class="cta-band"><div class="wrap narrow">
<h2>{heading}</h2><p>{text}</p>{button}
</div></section>"""


# ---------------------------------------------------------------- pages

PAGES = {}

PAGES["index.html"] = (
    "Home",
    "Dr. Rashmi Verma is a neuro-ophthalmologist caring for adults and children on Long Island, NY: optic neuritis, papilledema and IIH, double vision, visual field loss and more.",
    f"""
<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="eyebrow">Rashmi Verma, MD · Long Island, New York</p>
    <h1>Specialized neuro-ophthalmic care for adults and children</h1>
    <p class="lead">Neuro-ophthalmology is a subspecialty that cares for diseases affecting both the eyes and the brain, and the connections between them. When a visit to the neurologist or the ophthalmologist hasn't given you answers, it is time to see a neuro-ophthalmologist.</p>
    <p>Dr. Verma is a board-certified neurologist with dual fellowship training in neuro-ophthalmology and pediatric ophthalmology. She provides expert diagnosis and compassionate care for adult and pediatric patients.</p>
    <div class="btn-row">{waitlist_cta()}<a class="btn btn-ghost" href="about.html">Meet Dr. Verma</a></div>
  </div>
  <figure class="portrait"><img src="images/rashmi-verma-portrait.jpg" alt="Dr. Rashmi Verma, MD, neuro-ophthalmologist" width="480" height="720"></figure>
</div></section>

<section class="section"><div class="wrap">
  <p class="eyebrow">Conditions treated</p>
  <h2>Understanding your diagnosis</h2>
  <p class="section-lead">Neuro-ophthalmic conditions can be complex, hard to understand, and sometimes vision-threatening. Dr. Verma takes time to explain your diagnosis in simple, easy-to-understand language and guide you through every step of your care.</p>
  <div class="cards four">
    <article class="card"><h3>Optic neuritis</h3><p>Inflammation of the optic nerve that causes sudden vision loss or pain with eye movement, often associated with multiple sclerosis or other autoimmune conditions.</p></article>
    <article class="card"><h3>Papilledema and intracranial pressure</h3><p>Swelling of the optic nerve head from raised pressure inside the skull, which can threaten vision if not diagnosed and managed promptly.</p></article>
    <article class="card"><h3>Double vision (diplopia)</h3><p>Seeing two images of one object, from nerve palsies, muscle disorders, or neurological conditions affecting eye alignment.</p></article>
    <article class="card"><h3>Visual field loss</h3><p>Loss of side or central vision that can signal a problem along the visual pathway from the eye to the brain, including stroke or tumors.</p></article>
  </div>
  <p><a class="text-link" href="conditions.html">View all conditions →</a></p>
</div></section>

<section class="section alt"><div class="wrap">
  <p class="eyebrow">Why choose Dr. Verma</p>
  <h2>Expert care, close to home</h2>
  <div class="cards three">
    <article class="card"><h3>Subspecialty expertise</h3><p>Dedicated fellowship training in neuro-ophthalmology, a rare subspecialty that combines the depth of neurology with the precision of ophthalmology.</p></article>
    <article class="card"><h3>Adults and children</h3><p>Dr. Verma sees patients of all ages, from children with optic nerve abnormalities to adults with complex neurological vision disorders.</p></article>
    <article class="card"><h3>Personal attention</h3><p>Every patient is seen by Dr. Verma herself. No handoffs, just a thorough evaluation and a clear plan.</p></article>
  </div>
</div></section>

<section class="section"><div class="wrap two-col">
  <div><h2>Referred by your doctor?</h2><p>Most patients are referred by their eye doctor, neurologist, or primary care physician. Self-referrals are welcome too. See <a href="new-patients.html">New Patients</a> for what to expect.</p></div>
  <div><h2>Referring a patient?</h2><p>Dr. Verma sends a consultation note to the referring physician after every new visit. See <a href="for-physicians.html">For Physicians</a> for how to refer.</p></div>
</div></section>
""" + cta_band("Ready to take the next step?", "Dr. Verma's office is opening soon. Join the waitlist and we will call you as soon as appointments open."),
)

PAGES["about.html"] = (
    "About Dr. Verma",
    "Dr. Rashmi Verma is a neurology-trained neuro-ophthalmologist with fellowships at the University of Michigan Kellogg Eye Center and Akron Children's Hospital.",
    f"""
<section class="page-head"><div class="wrap hero-grid">
  <div>
    <p class="eyebrow">About Dr. Verma</p>
    <h1>Meet Rashmi Verma, MD</h1>
    <p class="lead">Dr. Verma is a neurology-trained neuro-ophthalmologist who cares for adults and children with disorders of the optic nerve, the brain, and the connections between the eye and the brain.</p>
    <p>She has had a distinguished academic career, with dual fellowship training in neuro-ophthalmology and pediatric ophthalmology at the University of Michigan and Akron Children's Hospital, and neurology residency at Mount Sinai. She is committed to dedicated, compassionate care for every patient.</p>
  </div>
  <figure class="portrait"><img src="images/rashmi-verma-portrait.jpg" alt="Dr. Rashmi Verma, MD" width="480" height="720"><figcaption>Rashmi Verma, MD · Neuro-Ophthalmologist · Long Island, New York</figcaption></figure>
</div></section>

<section class="section"><div class="wrap narrow prose">
  <h2>A subspecialist you can talk to</h2>
  <p>Dr. Verma completed fellowship training in neuro-ophthalmology at the W.K. Kellogg Eye Center, University of Michigan, and in pediatric ophthalmology and adult strabismus at Akron Children's Hospital. She completed her neurology residency at Mount Sinai Beth Israel / Mount Sinai West in New York and is board certified in neurology by the American Board of Psychiatry and Neurology.</p>
  <p>She has held faculty appointments, each with joint roles across ophthalmology, neurology, and pediatrics, at:</p>
  <ul>
    <li>Northwell Health, Donald and Barbara Zucker School of Medicine at Hofstra/Northwell</li>
    <li>Saint Louis University School of Medicine</li>
    <li>Montefiore Medical Center, Albert Einstein College of Medicine</li>
    <li>Stony Brook University, Renaissance School of Medicine (Director of Neuro-Ophthalmology, 2026)</li>
  </ul>
  <p>She has trained both ophthalmology and neurology residents and taught medical students throughout her career, and has given more than 50 invited lectures, Grand Rounds, and presentations at national and international meetings. She is a Fellow of the North American Neuro-Ophthalmology Society (NANOS), serves on the abstract committee for the journal <em>Neuro-Ophthalmology</em>, and reviews for the <em>Journal of Neuro-Ophthalmology</em> and the <em>Oman Journal of Ophthalmology</em>.</p>
</div></section>

<section class="section alt"><div class="wrap">
  <h2>Training and credentials</h2>
  <dl class="creds">
    <div><dt>Fellowship, Neuro-Ophthalmology</dt><dd>W.K. Kellogg Eye Center, University of Michigan, Ann Arbor, MI</dd></div>
    <div><dt>Fellowship, Pediatric Ophthalmology and Adult Strabismus</dt><dd>Akron Children's Hospital, Akron, OH</dd></div>
    <div><dt>Neurology Residency</dt><dd>Mount Sinai Beth Israel / Mount Sinai West, New York, NY; Saint Louis University School of Medicine, St. Louis, MO</dd></div>
    <div><dt>Ophthalmology Residency</dt><dd>Regional Institute of Ophthalmology, Gandhi Medical College, Barkatullah University, India</dd></div>
    <div><dt>Board Certification</dt><dd>American Board of Psychiatry and Neurology, Neurology (2020)</dd></div>
    <div><dt>Fellow</dt><dd>North American Neuro-Ophthalmology Society (NANOS), 2023</dd></div>
    <div><dt>Memberships</dt><dd>NANOS, American Academy of Neurology, American Medical Association, Women in Neuro-Ophthalmology</dd></div>
  </dl>
</div></section>

<section class="section"><div class="wrap">
  <h2>Areas of expertise</h2>
  <div class="cards two">
    <article class="card"><h3>Idiopathic intracranial hypertension (IIH)</h3><p>A special interest in the medical and surgical management of IIH in adults and children, including papilledema evaluation, weight management, medication, and surgery when indicated.</p></article>
    <article class="card"><h3>Pediatric neuro-ophthalmology</h3><p>Fellowship-trained care for children with optic nerve abnormalities, visual field defects, nystagmus, strabismus, and other conditions, with a family-centered approach.</p></article>
    <article class="card"><h3>Cranial nerve palsies and myasthenia gravis</h3><p>Diagnosis and management of double vision, cranial nerve palsies, and ocular myasthenia gravis.</p></article>
    <article class="card"><h3>Vision loss after stroke</h3><p>Assessment and rehabilitation planning for visual field loss after stroke or other events affecting the visual pathway.</p></article>
  </div>
</div></section>

<section class="section alt"><div class="wrap narrow">
  <blockquote class="quote"><p>“My goal is to give every patient clarity about their diagnosis, their options, and what comes next. Whether you are an adult facing a new neurological diagnosis or a parent seeking answers for your child, you deserve a thorough explanation and a physician who listens.”</p><cite>Rashmi Verma, MD</cite></blockquote>
</div></section>

<section class="section"><div class="wrap narrow">
  <h2>Selected publications</h2>
  <ol class="pubs">
    <li>Verma R. Neuro-ophthalmic manifestations of multiple sclerosis. <em>Int Ophthalmol Clin.</em> 2026;66(1).</li>
    <li>Mai K, Su R, Basalely A, et al. Anterior and posterior ischemic optic neuropathy in a child with focal segmental glomerulosclerosis on hemodialysis. <em>Pediatric Nephrology.</em> 2024;39(6).</li>
    <li>Nord JM, Shah PP, Verma R. Complete and uneventful recovery in a case of lymphocytic hypophysitis causing third nerve palsy. <em>Neuro-Ophthalmology.</em> 2022.</li>
    <li>Verma R, Wolfe G, Kupersmith MJ. Ocular myasthenia gravis: how effective is low dose prednisone long term? <em>J Neurol Sci.</em> 2020.</li>
    <li>Shah P, Gelnick S, Jonisch J, Verma R. Central retinal vein occlusion following BNT162b2 (Pfizer-BioNTech) COVID-19 mRNA vaccine: a case report. <em>Retinal Cases &amp; Brief Reports.</em> 2021.</li>
  </ol>
""" + ('<p class="pdf-link"><a class="text-link" href="files/a-typical-day-in-neuro-ophthalmology.pdf">Featured reading: A Typical Day in Neuro-Ophthalmology (PDF) →</a></p>' if os.path.exists(os.path.join(HERE, "assets", "files", "a-typical-day-in-neuro-ophthalmology.pdf")) else "") + """
</div></section>
""" + cta_band("Join the waitlist", "The office is not yet seeing patients. Join the waitlist and we'll contact you when scheduling opens."),
)

COND = [
    ("Optic nerve", "Optic neuritis", "Inflammation of the optic nerve, often causing sudden vision loss, pain with eye movement, and faded colors. Frequently associated with multiple sclerosis."),
    ("Optic nerve", "Papilledema and idiopathic intracranial hypertension (IIH)", "Swelling of the optic disc from raised pressure inside the skull. IIH is a common cause, particularly in women of childbearing age, and can lead to permanent vision loss if untreated."),
    ("Optic nerve", "Ischemic and other optic neuropathies", "Damage to the optic nerve from reduced blood flow (AION, PION, including evaluation for giant cell arteritis), compression, hereditary conditions such as Leber's, or toxic and nutritional causes."),
    ("Eye movement", "Double vision (diplopia)", "Seeing two images of one object, caused by misalignment of the eyes from problems with the nerves or muscles that move them. It can be a sign of a serious neurological condition."),
    ("Eye movement", "Cranial nerve palsies", "Weakness of the 3rd, 4th, or 6th cranial nerve, causing double vision, a drooping eyelid, or abnormal eye position. Causes include diabetes, high blood pressure, and aneurysm."),
    ("Neuromuscular", "Ocular myasthenia gravis", "An autoimmune condition causing drooping eyelids and double vision that change through the day."),
    ("Visual pathway", "Visual field loss", "Loss of side or central vision from damage anywhere from the retina to the back of the brain. The pattern of loss helps locate the underlying problem."),
    ("Visual pathway", "Vision changes after stroke", "Stroke affecting the visual pathways can cause loss of half the visual field (hemianopia), visual neglect, or cortical visual impairment."),
    ("Eyelid and face", "Blepharospasm and hemifacial spasm", "Involuntary eyelid closing or twitching of one side of the face, treated with Botox injections in the office."),
    ("Other", "Unexplained vision loss", "Vision changes that a standard eye exam does not explain."),
    ("Other", "Unequal or abnormal pupils", "Including anisocoria and Horner syndrome."),
    ("Other", "Migraine with visual symptoms", "Visual aura and other visual disturbances that need evaluation to rule out other causes."),
]

PAGES["conditions.html"] = (
    "Conditions Treated",
    "Neuro-ophthalmic conditions Dr. Rashmi Verma treats in adults and children: optic neuritis, papilledema and IIH, double vision, visual field loss, blepharospasm and more.",
    """
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Conditions we treat</p>
  <h1>Expert care for complex vision and neurological conditions</h1>
  <p class="lead">Many conditions that affect your vision have neurological causes, and they need a specialist trained in both fields to diagnose and treat them.</p>
</div></section>
<section class="section"><div class="wrap two-col">
  <div><h2>What is neuro-ophthalmology?</h2><p>Neuro-ophthalmology focuses on vision problems related to the nervous system: the optic nerves, the visual pathways in the brain, and the nerves that control eye movement. If your eye doctor has ruled out a problem with the eye itself, or your vision symptoms come with headaches or other neurological symptoms, a neuro-ophthalmologist may be the right specialist.</p></div>
  <div class="note"><h3>Adult and pediatric care</h3><p>Many neuro-ophthalmic conditions affect children differently than adults. Dr. Verma's dual fellowship training in pediatric ophthalmology and neuro-ophthalmology equips her to care for patients of all ages.</p></div>
</div></section>
<section class="section alt"><div class="wrap">
  <h2>Conditions we diagnose and treat</h2>
  <div class="cards three">
""" + "".join(f'<article class="card"><p class="tag">{e(t)}</p><h3>{e(n)}</h3><p>{e(d)}</p></article>' for t, n, d in COND) + """
  </div>
</div></section>
""" + cta_band("Not sure if your symptoms are neuro-ophthalmic?", "Many patients come to Dr. Verma after seeing other specialists without a clear diagnosis. If you have unexplained vision changes, eye movement problems, or vision symptoms with neurological complaints, an evaluation may provide answers."),
)

SERV = [
    ("Comprehensive neuro-ophthalmic evaluation", "A detailed exam of the visual system and its neurological connections: visual acuity, color vision, pupils, eye movements, and the optic nerve. Dr. Verma combines the eye exam with a neurological assessment to find where the problem lies, whether in the eye, optic nerve, visual pathway, or brain.", "Unexplained vision loss, visual field defects, double vision, optic nerve abnormalities, or vision symptoms with neurological complaints."),
    ("OCT imaging of the optic nerve and retina", "Optical coherence tomography (OCT) is a quick, painless scan that measures the optic nerve and retinal nerve fiber layer, detecting swelling, thinning, and changes invisible to the naked eye. It is especially useful for monitoring papilledema in IIH, recovery from optic neuritis, and early optic atrophy.", "Papilledema, optic neuritis, IIH, optic neuropathy, or any condition needing optic nerve monitoring over time."),
    ("Visual field testing", "Automated perimetry maps your side and central vision, detects blind spots, and tracks change over time. Results are interpreted alongside the full clinical picture.", "Suspected or known optic nerve disease, raised intracranial pressure, stroke, or any condition affecting the visual pathway."),
    ("Botox injections for blepharospasm and hemifacial spasm", "In-office onabotulinumtoxinA (Botox) injections to relax the muscles that cause involuntary eyelid closing or facial spasm. Treatment is usually repeated about every three months.", "Adults with benign essential blepharospasm or hemifacial spasm."),
    ("Pediatric neuro-ophthalmic evaluation", "Children can't always describe their symptoms, and their visual systems are still developing. Dr. Verma performs thorough, child-friendly evaluations and explains findings clearly to families.", "Children referred for optic nerve swelling, unexplained vision loss, nystagmus, abnormal eye movements, or suspected intracranial hypertension."),
    ("IIH diagnosis and management", "Ongoing care for idiopathic intracranial hypertension, including papilledema grading, visual field and OCT monitoring at each visit, and coordination of medical and surgical treatment with neurology and neurosurgery.", "Adults and children with known or suspected IIH or raised intracranial pressure."),
    ("Co-management with neurology and neurosurgery", "Pituitary tumors, multiple sclerosis, stroke, and intracranial hypertension often need care across specialties. Dr. Verma works closely with referring physicians and colleagues.", "Patients with pituitary or sellar tumors, MS-related vision symptoms, stroke, or conditions needing several specialists."),
    ("Telehealth follow-up visits", "Secure video visits for appropriate follow-ups, such as reviewing test results. Our office will let you know if your visit qualifies.", "Established patients whose follow-up does not need an in-person exam."),
]

PAGES["services.html"] = (
    "Services",
    "Neuro-ophthalmic evaluation, OCT imaging, visual field testing, Botox for blepharospasm and hemifacial spasm, pediatric evaluation, IIH care and telehealth with Dr. Rashmi Verma.",
    """
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Services</p>
  <h1>Comprehensive neuro-ophthalmic evaluation and care</h1>
  <p class="lead">Every visit begins with a thorough evaluation that combines the precision of ophthalmology with the diagnostic depth of neurology.</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="services">
""" + "".join(f'<article class="service"><h2>{e(n)}</h2><p>{e(d)}</p><p class="who"><strong>Who it is for:</strong> {e(w)}</p></article>' for n, d, w in SERV) + """
  </div>
</div></section>
<section class="section alt"><div class="wrap">
  <h2>Your first visit</h2>
  <ol class="steps">
    <li><h3>Referral and scheduling</h3><p>Most patients are referred by their ophthalmologist, neurologist, or primary care physician. Self-referrals are welcome.</p></li>
    <li><h3>Comprehensive evaluation</h3><p>A detailed history, a full neuro-ophthalmic exam, and any testing needed, such as visual fields or OCT, in a single appointment when possible.</p></li>
    <li><h3>Clear explanation</h3><p>Dr. Verma walks you through her findings, explains the diagnosis in plain language, and discusses your options.</p></li>
    <li><h3>Coordinated follow-up</h3><p>If you need monitoring or co-management, Dr. Verma coordinates directly with your care team.</p></li>
  </ol>
</div></section>
""" + cta_band("Interested in seeing Dr. Verma?", "The office is not yet seeing patients. Join the waitlist and we'll contact you when scheduling opens."),
)

PAGES["new-patients.html"] = (
    "New Patients",
    "What to expect at your first visit with Dr. Rashmi Verma: what to bring, insurance, Workers' Compensation, telehealth and how to schedule.",
    f"""
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">New patients</p>
  <h1>Preparing for your visit</h1>
  <p class="lead">Dr. Verma's office is opening soon and is not yet seeing patients. Join the waitlist and we'll contact you when appointments open. The information below describes visits once the office is open.</p>
  <div class="btn-row">{waitlist_cta()}</div>
</div></section>
<section class="section"><div class="wrap two-col">
  <div>
    <h2>What to bring</h2>
    <ul>
      <li>Photo ID and insurance card(s)</li>
      <li>A referral, if your plan requires one</li>
      <li>A list of your medications</li>
      <li>Your glasses and contact lenses</li>
      <li>MRI or CT reports and images (on disc or a portal link) and recent eye exam records</li>
      <li>For Workers' Compensation visits: your WCB claim number and the insurance carrier's name and address</li>
    </ul>
  </div>
  <div>
    <h2>How long it takes</h2>
    <p>Plan for 1.5 to 2 hours for a first visit, since testing is often done the same day. Your pupils may be dilated, so bring sunglasses and consider having someone drive you home.</p>
    <h2>If you were referred</h2>
    <p>Ask your doctor's office to send your records before your visit so Dr. Verma can review them in advance.</p>
  </div>
</div></section>
<section class="section alt"><div class="wrap two-col">
  <div>
    <h2>Insurance</h2>
    <p>Insurance details are coming soon. We will post the plans we participate in before the office opens. If we are out of network with your plan, we will give you a cost estimate before your visit.</p>
  </div>
  <div>
    <h2>Workers' Compensation</h2>
    <p>Once the office opens, we will accept New York State Workers' Compensation for work-related eye and vision injuries. Please bring your WCB claim number to your first visit.</p>
    <h2>Telehealth</h2>
    <p>Some follow-up visits can be done by secure video. We will let you know if your visit qualifies.</p>
  </div>
</div></section>
<section class="section"><div class="wrap narrow">
  <div class="note"><h3>Uninsured or self-pay patients</h3><p>You have the right to receive a Good Faith Estimate of expected charges. Ask us for one when you schedule. <a href="good-faith-estimate.html">Learn more</a>.</p></div>
</div></section>
""",
)

PAGES["for-physicians.html"] = (
    "For Physicians",
    "How to refer a patient to neuro-ophthalmologist Dr. Rashmi Verma on Long Island: what to send, urgent referrals and consultation notes.",
    f"""
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">For referring physicians</p>
  <h1>Referring a patient</h1>
  <p class="lead">Dr. Verma welcomes referrals from ophthalmologists, optometrists, neurologists, neurosurgeons, pediatricians, endocrinologists, rheumatologists, primary care physicians, and emergency departments. A consultation note goes back to the referring physician after every new visit.</p>
</div></section>
<section class="section"><div class="wrap two-col">
  <div>
    <div class="note"><h3>Not yet accepting referrals</h3><p>The office is opening soon and is not yet seeing patients. Until then, please continue to refer patients to their current care. Patients can join our waitlist, and we will post referral details here when the office opens.</p></div>
    <h2>How to refer, once we open</h2>
    <ol>
      <li>Send the referral to our office{(" by fax at " + e(CONFIG['fax'])) if CONFIG['fax'] else ""}{(" or call " + e(CONFIG['phone'])) if CONFIG['phone'] else ""}. Referral lines open when the office opens.</li>
      <li>Include the reason for referral, recent eye exam notes, visual fields or OCT if available, and any MRI or CT reports.</li>
      <li>We contact the patient to schedule and confirm insurance.</li>
    </ol>
    <h2>After the visit</h2>
    <p>You receive a consultation note with the diagnosis, test results, and plan. Patients return to your care for ongoing eye or neurological management, with co-management where it helps.</p>
  </div>
  <div>
    <h2>Common reasons to refer</h2>
    <ul>
      <li>Optic disc swelling or pallor</li>
      <li>Unexplained vision loss or visual field defect</li>
      <li>New double vision, ptosis, or anisocoria</li>
      <li>Suspected optic neuritis or demyelinating disease</li>
      <li>Known or suspected IIH, adult or pediatric</li>
      <li>Blepharospasm or hemifacial spasm for Botox</li>
      <li>Visual complaints after stroke, head injury, or brain surgery</li>
      <li>Pediatric optic nerve abnormalities, nystagmus, or strabismus with neurological features</li>
    </ul>
    <div class="note"><h3>Urgent concerns</h3><p>Once the office is open, please call directly about suspected giant cell arteritis, new papilledema, or acute vision loss. Send any patient with signs of stroke or an acute neurological deficit to the nearest emergency department first.</p></div>
  </div>
</div></section>
""",
)

PAGES["contact.html"] = (
    "Contact",
    f"Contact Dr. Rashmi Verma's neuro-ophthalmology office on Long Island, NY, opening soon. Join the appointment waitlist.",
    f"""
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Get in touch</p>
  <h1>Contact</h1>
  <p class="lead">The office is opening soon on Long Island, New York.</p>
</div></section>
<section class="section"><div class="wrap two-col">
  <div id="waitlist">
    <h2>Join the waitlist</h2>
    <p>We are not yet seeing patients. Join the waitlist and we'll call you as soon as scheduling opens. Joining does not book an appointment.</p>
    {waitlist_cta() if CONFIG['waitlist_form_url'] else f'<p>Email <a href="mailto:{CONFIG["email"]}?subject=Waitlist">{CONFIG["email"]}</a> with your name and the best phone number to reach you. Please do not include medical details.</p>'}
    <div class="note warn"><h3>Don't wait with sudden symptoms</h3><p>If you have a severe headache, sudden vision loss, new double vision, or other sudden neurological symptoms, call 911, go to the nearest emergency room, or contact your current doctor today.</p></div>
  </div>
  <div>
    <h2>Office information</h2>
    {contact_lines()}
    <h3>Referrals</h3>
    <p>Physicians: see <a href="for-physicians.html">For Physicians</a>.</p>
  </div>
</div></section>
""",
)

PAGES["privacy.html"] = (
    "Privacy Policy",
    "Website privacy policy.",
    f"""
<section class="page-head"><div class="wrap narrow"><h1>Privacy Policy</h1></div></section>
<section class="section"><div class="wrap narrow prose">
  <h2>Website privacy</h2>
  <p>{CONFIG['name']} respects your privacy. This website does not use advertising or tracking cookies. If you contact us or join the waitlist, we collect only the information you choose to send, such as your name, phone number, and email address, and use it only to respond to you and to let you know when scheduling opens. We do not sell your information.</p>
  <p>Mobile phone numbers and text messaging consent are never shared with third parties or affiliates for marketing or promotional purposes.</p>
  <p>Our waitlist form asks only for contact details. Please do not send medical information through the form or by email.</p>
  <h2>Your health information</h2>
  <p>How we use and protect your health information, and your rights, are described in our <a href="notice-of-privacy-practices.html">Notice of Privacy Practices</a>.</p>
  <h2>Questions</h2>
  <p>Email <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>.</p>
</div></section>
""",
)

PAGES["notice-of-privacy-practices.html"] = (
    "Notice of Privacy Practices",
    "HIPAA Notice of Privacy Practices: how your medical information may be used and disclosed, and how you can get access to it.",
    f"""
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">HIPAA</p>
  <h1>Notice of Privacy Practices</h1>
  <p class="lead">This notice describes how medical information about you may be used and disclosed and how you can get access to this information. Please review it carefully.</p>
  <p>Effective {CONFIG['npp_effective']} · {e(CONFIG['legal_entity']) if CONFIG['legal_entity'] else CONFIG['name']}</p>
</div></section>
<section class="section"><div class="wrap narrow prose">

  <h2>Your rights</h2>
  <p>When it comes to your health information, you have certain rights. This section explains your rights and some of our responsibilities to help you.</p>
  <h3>Get a copy of your medical record</h3>
  <ul>
    <li>You can ask to see or get an electronic or paper copy of your medical record and other health information we have about you. Ask us how to do this.</li>
    <li>We will provide a copy or a summary of your health information, usually within 30 days of your request. We may charge a reasonable, cost-based fee.</li>
  </ul>
  <h3>Ask us to correct your medical record</h3>
  <ul>
    <li>You can ask us to correct health information about you that you think is incorrect or incomplete. Ask us how to do this.</li>
    <li>We may say "no" to your request, but we'll tell you why in writing within 60 days.</li>
  </ul>
  <h3>Request confidential communications</h3>
  <ul>
    <li>You can ask us to contact you in a specific way (for example, home or office phone) or to send mail to a different address.</li>
    <li>We will say "yes" to all reasonable requests.</li>
  </ul>
  <h3>Ask us to limit what we use or share</h3>
  <ul>
    <li>You can ask us not to use or share certain health information for treatment, payment, or our operations. We are not required to agree, and we may say "no" if it would affect your care.</li>
    <li>If you pay for a service or health care item out of pocket in full, you can ask us not to share that information with your health insurer for payment or our operations. We will say "yes" unless a law requires us to share it.</li>
  </ul>
  <h3>Get a list of those with whom we've shared information</h3>
  <ul>
    <li>You can ask for a list (accounting) of the times we've shared your health information for six years prior to the date you ask, who we shared it with, and why.</li>
    <li>We will include all disclosures except those about treatment, payment, and health care operations, and certain other disclosures (such as any you asked us to make). We'll provide one accounting a year for free but will charge a reasonable, cost-based fee if you ask for another one within 12 months.</li>
  </ul>
  <h3>Get a copy of this privacy notice</h3>
  <p>You can ask for a paper copy of this notice at any time, even if you have agreed to receive it electronically. We will provide you with a paper copy promptly.</p>
  <h3>Choose someone to act for you</h3>
  <p>If you have given someone medical power of attorney or if someone is your legal guardian, that person can exercise your rights and make choices about your health information. We will make sure the person has this authority and can act for you before we take any action.</p>
  <h3>File a complaint if you feel your rights are violated</h3>
  <ul>
    <li>You can complain if you feel we have violated your rights by contacting our Privacy Officer using the information at the end of this notice.</li>
    <li>You can file a complaint with the U.S. Department of Health and Human Services Office for Civil Rights by sending a letter to 200 Independence Avenue, S.W., Washington, D.C. 20201, calling 1-877-696-6775, or visiting <a href="https://www.hhs.gov/ocr/privacy/hipaa/complaints/">www.hhs.gov/ocr/privacy/hipaa/complaints/</a>.</li>
    <li>We will not retaliate against you for filing a complaint.</li>
  </ul>

  <h2>Your choices</h2>
  <p>For certain health information, you can tell us your choices about what we share. If you have a clear preference for how we share your information in the situations described below, talk to us. Tell us what you want us to do, and we will follow your instructions.</p>
  <p>In these cases, you have both the right and choice to tell us to:</p>
  <ul>
    <li>Share information with your family, close friends, or others involved in your care</li>
    <li>Share information in a disaster relief situation</li>
  </ul>
  <p>If you are not able to tell us your preference, for example if you are unconscious, we may go ahead and share your information if we believe it is in your best interest. We may also share your information when needed to lessen a serious and imminent threat to health or safety.</p>
  <p>In these cases we never share your information unless you give us written permission:</p>
  <ul>
    <li>Marketing purposes</li>
    <li>Sale of your information</li>
  </ul>

  <h2>Our uses and disclosures</h2>
  <h3>How do we typically use or share your health information?</h3>
  <p><strong>Treat you.</strong> We can use your health information and share it with other professionals who are treating you. Example: Dr. Verma sends a consultation note to the doctor who referred you, or shares test results with your neurologist.</p>
  <p><strong>Run our organization.</strong> We can use and share your health information to run our practice, improve your care, and contact you when necessary. Example: we use health information about you to manage your treatment and services, or to send appointment reminders.</p>
  <p><strong>Bill for your services.</strong> We can use and share your health information to bill and get payment from health plans or other entities. Example: we give information about you to your health insurance plan or Workers' Compensation carrier so it will pay for your services.</p>
  <h3>How else can we use or share your health information?</h3>
  <p>We are allowed or required to share your information in other ways, usually in ways that contribute to the public good, such as public health and research. We have to meet many conditions in the law before we can share your information for these purposes. For more information see <a href="https://www.hhs.gov/ocr/privacy/hipaa/understanding/consumers/index.html">www.hhs.gov/ocr/privacy/hipaa/understanding/consumers/index.html</a>.</p>
  <ul>
    <li><strong>Help with public health and safety issues</strong>, such as preventing disease, helping with product recalls, reporting adverse reactions to medications, reporting suspected abuse, neglect, or domestic violence, and preventing or reducing a serious threat to anyone's health or safety.</li>
    <li><strong>Do research.</strong> We can use or share your information for health research, under the conditions the law sets.</li>
    <li><strong>Comply with the law.</strong> We will share information about you if state or federal laws require it, including with the Department of Health and Human Services if it wants to see that we're complying with federal privacy law.</li>
    <li><strong>Respond to organ and tissue donation requests</strong> and <strong>work with a medical examiner or funeral director</strong> when an individual dies.</li>
    <li><strong>Address workers' compensation, law enforcement, and other government requests.</strong> We can use or share health information about you for workers' compensation claims, for law enforcement purposes or with a law enforcement official, with health oversight agencies for activities authorized by law, and for special government functions such as military, national security, and presidential protective services.</li>
    <li><strong>Respond to lawsuits and legal actions.</strong> We can share health information about you in response to a court or administrative order, or in response to a subpoena.</li>
  </ul>
  <h3>New York law</h3>
  <p>New York law gives extra protection to some kinds of information, including HIV-related information, genetic test results, and certain mental health information. When New York law is more protective of your privacy than federal law, we follow New York law. For example, we will not share HIV-related information without your specific written consent except as New York law allows.</p>

  <h2>Our responsibilities</h2>
  <ul>
    <li>We are required by law to maintain the privacy and security of your protected health information.</li>
    <li>We will let you know promptly if a breach occurs that may have compromised the privacy or security of your information.</li>
    <li>We must follow the duties and privacy practices described in this notice and give you a copy of it.</li>
    <li>We will not use or share your information other than as described here unless you tell us we can in writing. If you tell us we can, you may change your mind at any time. Let us know in writing if you change your mind.</li>
  </ul>
  <p>For more information see <a href="https://www.hhs.gov/ocr/privacy/hipaa/understanding/consumers/noticepp.html">www.hhs.gov/ocr/privacy/hipaa/understanding/consumers/noticepp.html</a>.</p>

  <h2>Changes to the terms of this notice</h2>
  <p>We can change the terms of this notice, and the changes will apply to all information we have about you. The new notice will be available upon request, in our office, and on our website.</p>

  <h2>Contact our Privacy Officer</h2>
  <p>Privacy Officer: Rashmi Verma, MD<br>Email: <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>{("<br>Phone: " + e(CONFIG['phone'])) if CONFIG['phone'] else ""}{("<br>Mail: " + e(CONFIG['address'])) if CONFIG['address'] else ""}</p>
  <p>This notice is based on the model Notice of Privacy Practices published by the U.S. Department of Health and Human Services.</p>
</div></section>
""",
)

PAGES["sms-terms.html"] = (
    "SMS Terms",
    "Text messaging terms.",
    f"""
<section class="page-head"><div class="wrap narrow"><h1>SMS Terms</h1></div></section>
<section class="section"><div class="wrap narrow prose">
  <p>{CONFIG['name']} sends text messages about appointments, reminders, and office updates to patients who opt in. Message frequency varies. Message and data rates may apply.</p>
  <p>Reply <strong>STOP</strong> at any time to stop receiving messages, or <strong>HELP</strong> for help. You can also email <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>.</p>
  <p>Carriers are not liable for delayed or undelivered messages. Agreeing to receive texts is not a condition of receiving care. See our <a href="privacy.html">Privacy Policy</a> for how we handle your information.</p>
</div></section>
""",
)

PAGES["nondiscrimination.html"] = (
    "Nondiscrimination & Language Assistance",
    "Notice of nondiscrimination and availability of language assistance.",
    f"""
<section class="page-head"><div class="wrap narrow"><h1>Nondiscrimination and Language Assistance</h1></div></section>
<section class="section"><div class="wrap narrow prose">
  <p>{CONFIG['name']} complies with applicable federal civil rights laws and does not discriminate on the basis of race, color, national origin, age, disability, or sex (including sex characteristics, sexual orientation, and gender identity).</p>
  <p>We provide free aids and services to people with disabilities to communicate effectively with us, and free language assistance services, including qualified interpreters, to people whose primary language is not English. To request these services, email <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>.</p>
  <p>If you believe we have failed to provide these services or discriminated in another way, you can file a complaint with us at the email above, or with the U.S. Department of Health and Human Services, Office for Civil Rights, at <a href="https://ocrportal.hhs.gov/ocr/portal/lobby.jsf">ocrportal.hhs.gov</a> or 1-800-368-1019 (TDD 800-537-7697).</p>
  {language_taglines()}
</div></section>
""",
)

PAGES["accessibility.html"] = (
    "Accessibility & Language Help",
    "Accessibility, service animals, and free language help at Dr. Rashmi Verma's office.",
    f"""
<section class="page-head"><div class="wrap narrow"><h1>Accessibility and Language Help</h1><p class="lead">We want every patient to be able to reach us, understand their care, and visit comfortably.</p></div></section>
<section class="section"><div class="wrap narrow prose">
  <h2>At our office</h2>
  <p>Free aids and services are available, including large-print materials and qualified sign language interpreters. If you need an accommodation for your visit, please tell us when you are contacted to schedule, or email <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a>.</p>
  <p><strong>Service animals welcome. Pets and emotional support animals are not permitted.</strong></p>
  <h2>This website</h2>
  <p>We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA. If you have trouble using any part of this site, email <a href="mailto:{CONFIG['email']}">{CONFIG['email']}</a> and we will help you get the information another way.</p>
  {language_taglines()}
  <p>See also our <a href="nondiscrimination.html">Notice of Nondiscrimination</a>.</p>
</div></section>
""",
)

PAGES["good-faith-estimate.html"] = (
    "Good Faith Estimate",
    "Your right to a Good Faith Estimate of expected charges under the No Surprises Act.",
    f"""
<section class="page-head"><div class="wrap narrow"><h1>Your Right to a Good Faith Estimate</h1></div></section>
<section class="section"><div class="wrap narrow prose">
  <p>You have the right to receive a "Good Faith Estimate" explaining how much your medical care will cost.</p>
  <p>Under the law, health care providers need to give patients who don't have insurance or who are not using insurance an estimate of the bill for medical items and services.</p>
  <ul>
    <li>You have the right to receive a Good Faith Estimate for the total expected cost of any non-emergency items or services. This includes related costs like medical tests, prescription drugs, equipment, and hospital fees.</li>
    <li>Make sure your health care provider gives you a Good Faith Estimate in writing at least 1 business day before your medical service or item. You can also ask your health care provider, and any other provider you choose, for a Good Faith Estimate before you schedule an item or service.</li>
    <li>If you receive a bill that is at least $400 more than your Good Faith Estimate, you can dispute the bill.</li>
    <li>Make sure to save a copy or picture of your Good Faith Estimate.</li>
  </ul>
  <p>For questions or more information about your right to a Good Faith Estimate, visit <a href="https://www.cms.gov/nosurprises">www.cms.gov/nosurprises</a> or call 1-800-985-3059.</p>
</div></section>
""",
)

PAGES["careers.html"] = (
    "Careers",
    "Join Dr. Rashmi Verma's new neuro-ophthalmology office on Long Island. Hiring part-time ophthalmic technicians and front desk / medical assistants.",
    f"""
<section class="page-head"><div class="wrap narrow">
  <p class="eyebrow">Careers</p>
  <h1>Join our team</h1>
  <p class="lead">Dr. Verma is opening a new neuro-ophthalmology office on Long Island and is building a small, close-knit team. Everyone helps patients through their whole visit, from check-in to testing.</p>
  <div class="btn-row"><a class="btn btn-primary" href="{e(CONFIG['jobs_form_url'])}" target="_blank" rel="noopener">Apply Now</a></div>
</div></section>
<section class="section"><div class="wrap">
  <h2>Open positions</h2>
  <div class="cards two">
    <article class="card"><p class="tag">Part-time</p><h3>Ophthalmic Technician</h3><p>Patient work-ups, visual acuity and pupils, OCT imaging and visual field testing, plus front desk and phones on clinic days. COA or COT certification preferred; we will train the right person on our equipment.</p></article>
    <article class="card"><p class="tag">Part-time</p><h3>Front Desk / Medical Assistant</h3><p>Greeting and checking in patients, scheduling, insurance verification, and phones, plus helping with testing once trained. Medical office experience preferred.</p></article>
  </div>
  <div class="two-col">
    <div>
      <h2>What to expect</h2>
      <ul>
        <li>Part-time schedule on set clinic days</li>
        <li>Occasional evening or weekend clinics</li>
        <li>Paid holidays and paid time off</li>
        <li>Hands-on training in neuro-ophthalmic testing</li>
      </ul>
    </div>
    <div>
      <h2>How to apply</h2>
      <p>Fill out the short application form. We review every application and will contact you to set up an interview.</p>
      <p><a class="btn btn-primary" href="{e(CONFIG['jobs_form_url'])}" target="_blank" rel="noopener">Apply Now</a></p>
      <p class="small">{CONFIG['name']} is an equal opportunity employer.</p>
    </div>
  </div>
</div></section>
""",
)

NOT_FOUND = (
    "Page not found",
    "Page not found.",
    """<section class="page-head"><div class="wrap narrow"><h1>Page not found</h1><p class="lead">That page doesn't exist. <a href="index.html">Go to the home page</a>.</p></div></section>""",
)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for d in ("images", "files"):
        src = os.path.join(HERE, "assets", d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(OUT, d))
    shutil.copy(os.path.join(HERE, "assets", "styles.css"), OUT)
    for fn in ("favicon.svg",):
        p = os.path.join(HERE, "assets", fn)
        if os.path.exists(p):
            shutil.copy(p, OUT)
    for fn, (title, desc, body) in PAGES.items():
        with open(os.path.join(OUT, fn), "w") as f:
            f.write(page(fn, title, desc, body, active=fn))
    t, d, b = NOT_FOUND
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(page("404.html", t, d, b))
    urls = "".join(f"<url><loc>{CONFIG['domain']}/{'' if fn == 'index.html' else fn}</loc></url>" for fn in PAGES)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {CONFIG['domain']}/sitemap.xml\n")
    # Short link printed on business cards (QR code): /refer -> waitlist/referral form.
    # 302 so the target can change later without reprinting cards.
    target = CONFIG["waitlist_form_url"]
    with open(os.path.join(OUT, "_redirects"), "w") as f:
        f.write(f"/refer {target} 302\n/refer/ {target} 302\n")
    # Fallback page in case the redirect rules are not applied.
    os.makedirs(os.path.join(OUT, "refer"), exist_ok=True)
    with open(os.path.join(OUT, "refer", "index.html"), "w") as f:
        f.write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
                f'<meta http-equiv="refresh" content="0; url={e(target)}"><title>Refer a patient</title>'
                f'<script>location.replace({target!r});</script></head>'
                f'<body><p>Opening the referral form… <a href="{e(target)}">Continue</a></p></body></html>')
    print("Built", len(PAGES) + 1, "pages into", OUT)


if __name__ == "__main__":
    main()
