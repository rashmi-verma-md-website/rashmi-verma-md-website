"""Patient-education pages for individual conditions.

Each entry: slug -> dict(title, card_title, description, summary, sections, urgent).
sections is a list of (heading, html) pairs. HTML is trusted (written here).
build.py turns each entry into <slug>.html and links the matching cards to it.
"""

CONDITION_PAGES = {
    "optic-neuritis": dict(
        title="Optic Neuritis",
        description="Optic neuritis explained: symptoms, causes including multiple sclerosis, NMOSD and MOGAD, testing, treatment and recovery. Neuro-ophthalmologist Dr. Rashmi Verma, Long Island.",
        summary="Optic neuritis is inflammation of the optic nerve, the cable that carries what the eye sees to the brain. It usually affects one eye and often improves over weeks to months, but finding the cause matters for protecting your vision and your long-term health.",
        sections=[
            ("Common symptoms", """<ul>
  <li>Blurred, dim or lost vision in one eye that develops over hours to a few days</li>
  <li>Pain behind the eye, often worse when you move your eye</li>
  <li>Colors, especially red, looking faded or washed out</li>
  <li>A dark or blurry spot in the center of your vision</li>
</ul>
<p>In children, optic neuritis more often affects both eyes and may follow a viral illness.</p>"""),
            ("What causes it?", """<p>Optic neuritis happens when the immune system attacks the coating (myelin) around the optic nerve. It can be:</p>
<ul>
  <li><strong>Linked to multiple sclerosis (MS).</strong> Optic neuritis is sometimes the first sign of MS.</li>
  <li><strong>Part of another demyelinating disease,</strong> such as neuromyelitis optica spectrum disorder (NMOSD) or MOG antibody–associated disease (MOGAD). These need different treatment, so telling them apart is important.</li>
  <li><strong>Related to infection or other inflammatory conditions,</strong> such as sarcoidosis.</li>
</ul>"""),
            ("How it is diagnosed", """<p>Dr. Verma checks your vision, color vision, pupils and the optic nerve, and may order:</p>
<ul>
  <li><strong>Visual field testing</strong> to map any blind spots</li>
  <li><strong>OCT imaging</strong> to measure swelling or thinning of the optic nerve</li>
  <li><strong>MRI of the brain and eye sockets</strong> to look for inflammation and signs of MS</li>
  <li><strong>Blood tests</strong> for antibodies linked to NMOSD and MOGAD, when appropriate</li>
</ul>"""),
            ("Treatment and recovery", """<p>Many people recover much of their vision over several weeks to months. High-dose steroids may be recommended to speed recovery, and prompt treatment is especially important when NMOSD or MOGAD is suspected. Some people notice that colors or contrast stay slightly different after recovery.</p>
<p>If tests suggest MS or another demyelinating disease, Dr. Verma works with your neurologist so you can start long-term treatment that lowers the risk of future attacks.</p>"""),
        ],
        urgent="Sudden vision loss needs to be checked the same day. If vision loss comes with weakness, numbness, trouble speaking or a severe headache, call 911.",
    ),
    "papilledema-iih": dict(
        title="Papilledema and Idiopathic Intracranial Hypertension (IIH)",
        description="Papilledema and idiopathic intracranial hypertension (IIH) explained: symptoms, causes, testing, treatment and vision monitoring. Neuro-ophthalmologist Dr. Rashmi Verma, Long Island.",
        summary="Papilledema is swelling of the optic nerves caused by raised pressure inside the skull. Idiopathic intracranial hypertension (IIH) is one of its most common causes. Without treatment, the pressure can slowly and permanently damage vision, often without warning.",
        sections=[
            ("Common symptoms", """<ul>
  <li>Headaches, often daily and sometimes worse when lying down or in the morning</li>
  <li>Brief episodes of dimmed or lost vision lasting seconds, often when standing up or bending over</li>
  <li>A whooshing sound in the ears that pulses with the heartbeat</li>
  <li>Double vision</li>
  <li>Blurred vision or loss of side vision</li>
</ul>
<p>Some people have no symptoms, and the swelling is found during a routine eye exam.</p>"""),
            ("What causes it?", """<p>Papilledema can be caused by brain tumors, blood clots in the brain's veins, infections, bleeding or other conditions, so it always needs prompt brain imaging.</p>
<p>When no other cause is found, the diagnosis is <strong>idiopathic intracranial hypertension (IIH)</strong>. IIH is most common in young women, especially after recent weight gain, but it can also occur in older women, men and children. Some medicines, such as tetracycline antibiotics and high doses of vitamin A, can contribute.</p>"""),
            ("How it is diagnosed", """<ul>
  <li><strong>Dilated eye exam</strong> to see and grade the optic nerve swelling</li>
  <li><strong>OCT imaging</strong> to measure the swelling precisely</li>
  <li><strong>Visual field testing</strong> to check for loss of side vision</li>
  <li><strong>MRI and MR venography</strong> of the brain to look for other causes</li>
  <li><strong>Lumbar puncture (spinal tap)</strong> to measure the pressure of the fluid around the brain and test the fluid</li>
</ul>"""),
            ("Treatment", """<ul>
  <li><strong>Medication</strong> such as acetazolamide, which reduces the fluid that builds up pressure</li>
  <li><strong>Weight management,</strong> which can lower the pressure for many patients. Dr. Verma coordinates with weight management programs.</li>
  <li><strong>Headache treatment,</strong> in coordination with your neurologist</li>
  <li><strong>Surgery when vision is at risk,</strong> such as optic nerve sheath fenestration, a shunt, or venous sinus stenting, performed by surgical colleagues</li>
</ul>
<p>Because vision can worsen without obvious symptoms, regular visits with visual field testing and OCT are an important part of care.</p>"""),
        ],
        urgent="If your vision is getting worse quickly, or you have a sudden severe headache, go to the nearest emergency room or call 911.",
    ),
    "double-vision": dict(
        title="Double Vision (Diplopia)",
        description="Double vision (diplopia) explained: one eye versus both eyes, causes such as cranial nerve palsies and myasthenia gravis, testing and treatment. Neuro-ophthalmologist Dr. Rashmi Verma, Long Island.",
        summary="Double vision, or diplopia, means seeing two images of one object. The images may be side by side, one above the other, or tilted. Finding the cause is important, because double vision can be the first sign of a nerve, muscle or brain problem.",
        sections=[
            ("One eye or both eyes?", """<p>Cover one eye, then the other.</p>
<ul>
  <li><strong>If the double vision goes away when either eye is covered,</strong> the eyes are not lined up. This is called binocular double vision, and it is the type a neuro-ophthalmologist evaluates.</li>
  <li><strong>If it stays when you look with only one eye,</strong> the cause is usually in the eye itself, such as dry eye, cataract or a glasses prescription. Your regular eye doctor can help with this.</li>
</ul>"""),
            ("What causes it?", """<ul>
  <li><strong>Cranial nerve palsies:</strong> weakness of the nerves that move the eyes, from diabetes, high blood pressure, aneurysm, trauma, tumor or stroke</li>
  <li><strong>Myasthenia gravis:</strong> an autoimmune condition that causes double vision and droopy eyelids that often worsen as the day goes on</li>
  <li><strong>Thyroid eye disease:</strong> swelling of the eye muscles</li>
  <li><strong>Childhood eye misalignment (strabismus)</strong> that becomes harder to control over time</li>
  <li><strong>Conditions affecting the brainstem,</strong> such as stroke or multiple sclerosis</li>
</ul>"""),
            ("How it is diagnosed", """<p>Dr. Verma measures how your eyes line up in different directions using prisms, examines eye movements, eyelids and pupils, and checks for fatigue. Depending on the findings, blood tests or brain imaging may be needed.</p>"""),
            ("Treatment", """<ul>
  <li><strong>Treating the cause,</strong> such as myasthenia gravis or thyroid eye disease</li>
  <li><strong>Watchful waiting:</strong> many nerve palsies from diabetes or high blood pressure improve on their own within about three months</li>
  <li><strong>Relief while you recover:</strong> patching one eye or temporary stick-on prism lenses</li>
  <li><strong>Prism glasses</strong> for long-term double vision</li>
  <li><strong>Referral for eye muscle surgery</strong> when double vision is stable and does not resolve</li>
</ul>"""),
        ],
        urgent="Call 911 if double vision starts suddenly together with a droopy eyelid, a severe headache, weakness, numbness, slurred speech or trouble swallowing.",
    ),
    "visual-field-loss": dict(
        title="Visual Field Loss",
        description="Visual field loss explained: patterns of side and central vision loss, causes such as stroke, pituitary tumors and optic nerve disease, testing and rehabilitation. Neuro-ophthalmologist Dr. Rashmi Verma, Long Island.",
        summary="Your visual field is everything you can see while looking straight ahead, including your side vision. Loss of part of the visual field can come from damage anywhere along the pathway from the eye to the back of the brain. The pattern of loss helps show where the problem is.",
        sections=[
            ("Signs you may notice", """<ul>
  <li>Bumping into things or people on one side</li>
  <li>Missing words or losing your place when reading</li>
  <li>People or cars seeming to appear out of nowhere</li>
  <li>Trouble driving or judging your surroundings</li>
</ul>
<p>Many people do not notice the loss at first, because the brain fills in the gaps.</p>"""),
            ("Common patterns and causes", """<ul>
  <li><strong>Loss in one eye:</strong> usually a problem with the retina or optic nerve, such as optic neuritis, glaucoma or reduced blood flow to the optic nerve</li>
  <li><strong>Loss of the outer side of vision in both eyes:</strong> often from pressure on the optic chiasm, where the optic nerves cross, most commonly by a pituitary tumor</li>
  <li><strong>Loss of the same side of vision in both eyes (hemianopia):</strong> from damage behind the optic chiasm, such as stroke, tumor or head injury</li>
</ul>"""),
            ("How it is diagnosed", """<ul>
  <li><strong>Automated visual field testing</strong> to map exactly which areas are affected</li>
  <li><strong>OCT imaging</strong> of the optic nerve and retina</li>
  <li><strong>A complete neuro-ophthalmic exam</strong></li>
  <li><strong>MRI or other imaging</strong> when needed to find the cause</li>
</ul>"""),
            ("Treatment and rehabilitation", """<p>Treatment focuses on the cause. For example, vision may improve after treatment of a pituitary tumor, and some loss after stroke improves in the first months.</p>
<p>When loss is permanent, rehabilitation can help you make the most of the vision you have: scanning techniques, reading strategies, prism glasses and referral to low vision and occupational therapy services. Dr. Verma can also advise you about driving safety.</p>"""),
        ],
        urgent="Sudden loss of vision in one or both eyes can be a sign of stroke. Call 911 right away.",
    ),
}
