# Home page sections for jobenilagan.com.
# Papers are referenced by DOI and rendered from data.PUBS.
# Videos are on the Ateneo BUILD YouTube channel.

YT = "https://www.youtube.com/watch?v="

INTRO = ("I build and evaluate AI systems for learning, small businesses and public services, "
         "using design-based research. I joined Ateneo full-time in 2019 after more than 26 years "
         "in industry and completed a PhD in Computer Science in 2026.")

RESEARCH = [
    dict(
        title="AI-assisted workflows that harden into fixed pipelines",
        text=("How AI-assisted work in a research lab moves from open-ended prompting to fixed, checked "
              "pipelines, and which controls make that work safe to run. I also use these pipelines to make "
              "public explainer videos that are revised from viewer comments."),
        papers=["10.1109/ms.2026.3716868", "10.2139/ssrn.6358278", "10.2139/ssrn.6366020",
                "10.14569/ijacsa.2026.0170207"],
        videos=[("Why Katipunan traffic keeps getting worse (explainer, v4)", "rmaYzHz3bqs")],
    ),
    dict(
        title="Conversational tutoring and learning simulations",
        text=("Tutors and simulated characters built on large language models for entrepreneurship and "
              "management students. Students interview simulated customers and test their financial models "
              "with a simulated mentor. Teachers can write these simulations in plain language. This was the subject of my PhD dissertation, "
              "<i>The Design and Use of Conversational Intelligent Tutoring Systems and Customer Validation "
              "Simulation in Technology Entrepreneurship Education</i> (2026), supervised by "
              "Ma. Mercedes T. Rodrigo."),
        papers=["10.2139/ssrn.6520018", "10.1007/978-3-032-30015-7_35", "10.1007/978-3-032-30833-7_17",
                "10.1007/978-3-031-92967-0_4", "10.1007/978-981-96-6938-7_22"],
        videos=[("How do AI models play customers? (ICICT 2026)", "ZLICdqswr_w"),
                ("Can AI playing experts help design a learning app? (ICCE 2026)", "en2wQuWUInU")],
    ),
    dict(
        title="Digital public infrastructure and identity verification",
        text=("Through the Ateneo Technical Resource Lab, we help local governments, NGOs and financial "
              "institutions verify the Philippine National ID (PhilSys), including in places with no "
              "internet signal."),
        papers=[],
        videos=[("CLIK Offline Verifier: checking National IDs with no internet", "t3TFSYwOU0c"),
                ("Checking a National ID where there is no signal", "1ll42on66ks"),
                ("What is a National ID?", "CN8bM8aHR5U")],
    ),
]

PROJECTS = [
    dict(name="LiteChat", url=None,
         text=("A platform for running classroom simulations on several large language models. VentureBot, "
               "the customer-interview simulation in my dissertation, runs on it. Funded by an Ateneo URC "
               "grant, <i>Simulation-Enabled Lessons in Higher Education</i>.")),
    dict(name="Reading small-business paper records", url=None,
         text=("Research on reading the handwritten logbooks and receipts of small Philippine businesses with "
               "OCR and large language models, and turning them into sales, inventory and receivables records. "
               "This work led to <a href=\"https://meetklaro.com/\">KLARO</a>."),
         papers=["10.1007/978-3-031-93429-2_18", "10.1007/978-3-032-30044-7_1"],
         videos=[("Can a low-cost app read a food stall's notebook? (HCII 2025)", "ERkrAHm3f04")]),
    dict(name="Ateneo Technical Resource Lab (TRL)", url="https://trl.ph/",
         text=("Run by BUILD and launched with Co-Develop in May 2024. It runs the DPI Experience Center "
               "and built the eKYC extension for National ID verification, which DICT and PSA approved "
               "in November 2025.")),
    dict(name="Breathe Metro Manila", url="https://map.clarity.io/breathe-metro-manila",
         text=("An air quality coalition of Manila Observatory, the Ateneo School of Medicine and Public "
               "Health, Clarity Movement and BUILD, which publishes real-time air quality readings for "
               "Metro Manila. I lead BUILD's part. BUILD built the coalition's iPhone and Apple Watch apps "
               "for reading the data.")),
    dict(name="Tom Taps", url="https://apps.apple.com/app/id6760241580",
         text=("A picture board for children who don't speak, or don't speak yet. They tap pictures to build "
               "sentences that the app says aloud in English, Filipino or Spanish. Built with "
               "speech-language pathologists and published by Archmob Pte Ltd for iPhone and iPad.")),
    dict(name="Kanji Mentor", url="https://apps.apple.com/app/id6760374345",
         text=("A kanji writing app for JLPT learners. It hides each kanji until you draw it from memory, "
               "then reveals it and uses AI to check your handwriting for balance, stroke order and spacing. "
               "Reviews follow a spaced repetition schedule. Published by Archmob Pte Ltd for iPhone and iPad.")),
    dict(name="Katipunan traffic explainer", url=YT + "rmaYzHz3bqs",
         text=("A ten-minute video on why traffic on Katipunan Avenue keeps getting worse, made with an "
               "AI-assisted pipeline. Each version is posted, and viewer comments go into the next one. "
               "It is on version 4.")),
]

BACKGROUND_INTRO = "Before Ateneo I spent more than 26 years in industry."
BACKGROUND = [
    ("Seer Technologies, co-founder and CEO, 17 years",
     "Mobile apps, cloud management and data services."),
    ("Oracle Philippines, Technical Solutions Manager, 9 years", ""),
]

TEACHING_INTRO = ("I direct the BS Information Technology Entrepreneurship program at the John Gokongwei "
                  "School of Management. Courses I teach:")
TEACHING = [
    ("ITENT 122", "Product Management: Pricing and Costing"),
    ("DECSC 25", "Innovation Management and Human-Centered Design"),
    ("OPMAN 146", "Service Management, with a focus on customer experience"),
    ("", "Solutions Architecture"),
]
TEACHING_NOTE = "DECSC 25 and OPMAN 146 are built around design thinking and jobs-to-be-done."
