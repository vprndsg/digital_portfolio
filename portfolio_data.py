OWNER = {
    "name": "Michael Phillips",
    "title": "Digital Marketing Portfolio",
    "headline": "Launch systems, editorial storytelling, and digital experiences shaped for hospitality, luxury, and conversion.",
    "summary": "A portfolio foundation for email campaigns, events, splash pages, product storytelling, and live experimental work with a more polished Napa sensibility.",
    "journal_note": "The work I want to show is elegant without becoming sterile: warm hospitality, estate history, bottle-level detail, and enough discipline underneath that the campaign still performs.",
    "focus": [
        "Email campaigns",
        "Event creative",
        "Splash pages",
        "Product pages",
        "Interactive editorial concepts",
    ],
}


SIGNAL_STATS = [
    {"value": "5", "label": "case studies"},
    {"value": "4", "label": "core marketing surfaces"},
    {"value": "1", "label": "live interactive build"},
    {"value": "3", "label": "editorial story formats"},
]


PROJECTS = [
    {
        "slug": "biodynamic-chronicles",
        "theme": "plum",
        "category": "Interactive Editorial",
        "eyebrow": "Live Concept / Content Lab",
        "title": "Biodynamic Chronicles",
        "subtitle": "A daily wine-and-moon forecast designed like a living magazine, with a forecast rail on the left and a story feed on the right.",
        "summary": "I took a weird niche idea and turned it into a habit-forming digital object: part forecast, part editorial feed, part brand world.",
        "hero_image": "media/biodynamic-chronicles-preview.svg",
        "hero_alt": "Preview illustration of the Biodynamic Chronicles split-screen forecast and story feed",
        "scope": [
            {"value": "1", "label": "live forecast engine"},
            {"value": "3", "label": "seeded story formats"},
            {"value": "2", "label": "content columns"},
            {"value": "1", "label": "interactive demo"},
        ],
        "roles": [
            "Concept direction",
            "UX design",
            "Frontend build",
            "Editorial framing",
            "Interaction design",
        ],
        "tools": ["Flask", "Jinja", "JavaScript", "CSS", "Content strategy"],
        "deliverables": [
            "Interactive microsite",
            "Forecast UX",
            "Editorial feed system",
            "Motion and media behavior",
            "Portfolio-ready case study",
        ],
        "challenge": "Biodynamic wine culture can feel opaque, mystical, and slightly unserious from the outside. The challenge was turning that into something a stranger could understand in seconds and still want to explore.",
        "approach": [
            {
                "title": "Anchor the premise with a usable forecast",
                "body": "The forecast column gives today's reading and the next three days first, so the concept feels structured before it gets atmospheric.",
            },
            {
                "title": "Make the story feed feel like a publication",
                "body": "Instead of generic blog cards, the right rail acts like a magazine feed with a wine write-up, an adventure story, and a photo essay.",
            },
            {
                "title": "Treat interaction as proof of craft",
                "body": "Layered image reveals, expandable stories, and a lightbox turn the page from a mockup into a usable digital object.",
            },
        ],
        "artifacts": [
            {
                "eyebrow": "Forecast UX",
                "title": "Daily reading desk",
                "copy": "A structured module for today's moon state, decision framing, and a three-day forecast that can update live.",
            },
            {
                "eyebrow": "Editorial system",
                "title": "Three content modes",
                "copy": "Wine criticism, travel-story energy, and photo storytelling live inside one consistent visual frame.",
            },
            {
                "eyebrow": "Interaction layer",
                "title": "Media that feels handled",
                "copy": "Cards expand, images layer forward, and galleries open into a lightbox instead of sitting flat on the page.",
            },
        ],
        "gallery": [
            {
                "title": "Chronicles home screen",
                "caption": "The live split-screen view: forecast left, stories right, with a retro-editorial treatment designed for modern screens.",
                "image": "media/biodynamic-chronicles-preview.svg",
            },
            {
                "title": "Wine write-up media frame",
                "caption": "A single-image story mode that reads like a cover shot rather than a generic blog thumbnail.",
                "image": "media/merlot-nocturne.svg",
            },
            {
                "title": "Photo essay gallery",
                "caption": "The photo essay mode uses multiple frames, layered reveals, and a lightbox to make the page feel tactile.",
                "image": "media/harvest-frame-2.svg",
            },
        ],
        "closing_note": "This project shows how I think when the brief is loose: find the hook, design the system, then give it enough polish that people want to play with it.",
        "live_route": "chronicles_live",
        "card_points": ["Live demo", "Editorial design", "Interaction system"],
    },
    {
        "slug": "harvest-weekend-email-system",
        "theme": "amber",
        "category": "Email Campaigns",
        "eyebrow": "Real Sends / Beauregard Vineyards",
        "title": "Beauregard Vineyards Email Campaigns",
        "subtitle": "Lead the email marketing strategy via Mailchimp and manage front-end e-commerce operations in Commerce7, overseeing everything from campaign execution and segmentation to promotional builds and product bundling.",
        "summary": "This case study swaps placeholder mockups for real campaign work: two conversion emails and one event invitation with the original copy, imagery, and offer framing preserved.",
        "hero_image": "media/harvest-email-system.svg",
        "hero_alt": "Email campaign case-study mockup showing layered desktop and mobile modules",
        "scope": [
            {"value": "3", "label": "real deployed sends"},
            {"value": "2", "label": "sales campaigns"},
            {"value": "1", "label": "event invitation"},
            {"value": "1", "label": "consistent house voice"},
        ],
        "roles": [
            "Email strategy",
            "Copy direction",
            "Template editing",
            "Campaign packaging",
        ],
        "tools": [
            "Mailchimp",
            "HTML",
            "Copywriting",
            "Campaign design",
            "Adobe Photoshop",
            "Google AI Studio",
            "Commerce7",
            "Tock",
            "Photography",
        ],
        "deliverables": [
            "2021 Pinot Noir inventory offer",
            "Scary Good 2022 Pinot Noir sale",
            "Oysters in the Redwoods event invite",
            "Offer framing and promo-code hierarchy",
            "Brand-consistent footer and social modules",
        ],
        "challenge": "The harder part of winery email is not building a template. It is keeping the voice believable across very different jobs: moving library inventory, making a seasonal sale feel distinctive, and inviting guests into an in-person event without flattening everything into the same generic blast.",
        "approach": [
            {
                "title": "Lead with a human hook, not just the offer",
                "body": "The strongest sales send starts with a real cellar-story setup, then earns the discount instead of shouting it in the first line.",
            },
            {
                "title": "Shift the visual tone to match the moment",
                "body": "The Halloween sale uses louder typography and color, while the event invite slows down and lets the estate photography and menu narrative do more of the persuasion.",
            },
            {
                "title": "Keep every send pointed at one action",
                "body": "Whether the goal is purchase or attendance, each email keeps the next step obvious with a clear CTA, supporting product context, and minimal competing paths.",
            },
        ],
        "artifacts": [
            {
                "eyebrow": "Voice strategy",
                "title": "Founder-led copy that still converts",
                "copy": "The 2021 Pinot email reads like a note from the winery, then turns that intimacy into urgency with press validation, pricing contrast, and a direct purchase path.",
            },
            {
                "eyebrow": "Campaign range",
                "title": "Sales and event formats under one brand",
                "copy": "The examples show the same winery voice stretching across commerce and hospitality, without every send feeling like the same cloned template.",
            },
            {
                "eyebrow": "Execution",
                "title": "Real HTML sends, not concept boards",
                "copy": "These examples are archived email builds rendered directly in the portfolio so the case study shows shipped work rather than polished mockup theater.",
            },
        ],
        "gallery": [],
        "email_examples": [
            {
                "eyebrow": "Library inventory sale",
                "title": "An accidental discovery",
                "summary": "A founder-letter sales email built around a cellar inventory mistake, a 94-point review, and a 50% six-pack offer for the 2021 Pinot Noir Santa Cruz Mountains.",
                "file": "email_examples/beauregard-accidental-discovery.html",
                "tags": ["Founder voice", "Promo code", "Press quote"],
            },
            {
                "eyebrow": "Seasonal promotion",
                "title": "Scary Good 2022 Pinot Noir Sale",
                "summary": "A bolder, holiday-timed promotion that uses a themed headline, strong pricing contrast, and a single purchase CTA to move six-bottle packs.",
                "file": "email_examples/beauregard-scary-good-sale.html",
                "tags": ["Seasonal angle", "Offer hierarchy", "Single CTA"],
            },
            {
                "eyebrow": "Event invitation",
                "title": "Oysters in the Redwoods",
                "summary": "An event-driven send pairing oysters with the 2024 Chardonnay Metallique, using destination photography and host-style copy instead of hard-sell tactics.",
                "file": "email_examples/beauregard-oysters-redwoods.html",
                "tags": ["Event invite", "Hospitality tone", "Estate imagery"],
            },
        ],
        "closing_note": "Using archived sends here makes the portfolio stronger because the email work is no longer hypothetical. It shows real brand voice, real offer structure, and real campaign variety.",
        "card_points": ["3 real sends", "Sales + event email", "Brand voice"],
    },
    {
        "slug": "asado-vineyard-dinner",
        "theme": "violet",
        "category": "Events",
        "eyebrow": "Hospitality Programming / Event Curation",
        "title": "Asado Vineyard Dinner",
        "subtitle": "A chef-led vineyard dinner built from first outreach through guest communication, on-site service, and post-event wine follow-up.",
        "summary": "This project shows how I curate special events end to end: finding the chef, shaping the experience, building the email and ticket path, organizing rentals and guest outreach, serving the event, and following up afterward to sell featured wines.",
        "hero_image": "media/asada-vineyard-dinner-hero.jpg",
        "hero_alt": "Hero photo from the Asado Vineyard Dinner event",
        "scope": [
            {"value": "1", "label": "chef-driven vineyard dinner"},
            {"value": "60", "label": "guest seats managed"},
            {"value": "1", "label": "sales email + ticket push"},
            {"value": "1", "label": "post-event wine follow-up"},
        ],
        "roles": [
            "Chef sourcing and outreach",
            "Experience concepting",
            "Email campaign creation",
            "Guest communication",
            "Rental and vendor coordination",
            "On-site hosting and service",
            "Post-event wine sales follow-up",
        ],
        "tools": [
            "Cross-team coordination",
            "HTML",
            "Mailchimp",
            "Tock",
            "C7",
            "Copywriting",
            "Campaign Design",
        ],
        "deliverables": [
            "Event concept and positioning",
            "Ticketing and guest communications",
            "Launch email and CTA flow",
            "Rental and production coordination",
            "On-site event service",
            "Post-event follow-up to sell featured wines",
        ],
        "challenge": "A special dinner has to do more than look good on paper. The work needs to attract the right guests, make the evening feel singular before they arrive, execute smoothly on the ground, and then extend the momentum into follow-up wine sales after the tables are cleared.",
        "approach": [
            {
                "title": "Start with the right culinary partner",
                "body": "The event began with identifying and reaching out to Chef Diego Felix, then shaping the dinner around his fire-driven cooking and the Beauregard ranch setting so the concept felt specific instead of generic.",
            },
            {
                "title": "Build the event like a hospitality funnel",
                "body": "I wrote and packaged the launch email, handled the ticketing path, coordinated guest outreach, and kept the messaging aligned from invitation through purchase so the event felt composed before anyone arrived.",
            },
            {
                "title": "Carry the experience through the final pour",
                "body": "The job did not stop at promotion. I organized rentals, created and printed the menu, helped set the event, served the dinner itself, and followed up afterward with guests to continue the relationship and sell the featured wines.",
            },
        ],
        "artifacts": [
            {
                "eyebrow": "Chef partnership",
                "title": "Experience built around a real culinary point of view",
                "copy": "Rather than plugging food into a winery event template, the dinner was shaped around Diego Felix's live-fire style and the atmosphere of the Beauregard ranch.",
            },
            {
                "eyebrow": "Guest journey",
                "title": "Invitation, ticketing, and communication flow",
                "copy": "The event story lived across the email send, purchase path, and direct guest communication, making the night feel curated before check-in.",
            },
            {
                "eyebrow": "Revenue follow-through",
                "title": "Post-event follow-up tied back to wine sales",
                "copy": "After the dinner, outreach focused on the featured wines poured that night so the event functioned as both hospitality and conversion.",
            },
        ],
        "gallery": [
            {
                "title": "Hero dinner frame",
                "caption": "The main event image sets the tone: open-air hospitality, ranch atmosphere, and a dinner meant to feel singular rather than routine.",
                "image": "media/asada-vineyard-dinner-hero.jpg",
            },
            {
                "title": "Vineyard dinner setup",
                "caption": "Chef Diego and I in the Beauregard Ranch",
                "image": "media/asada-vineyard-dinner-01.jpg",
            },
            {
                "title": "Service and ranch detail",
                "caption": "Chef Diego speaks to the table",
                "image": "media/asada-vineyard-dinner-02.jpg",
            },
        ],
        "menu_file": "media/asada-vineyard-dinner-menu.pdf",
        "email_examples": [
            {
                "eyebrow": "Event launch email",
                "title": "Argentinian Asado at the Beauregard Ranch",
                "summary": "The launch email positioned the dinner around Chef Diego Felix, the live-fire menu, ticket urgency, and the distinct ranch atmosphere that made the event feel worth showing up for.",
                "file": "email_examples/beauregard-argentinian-asado.html",
                "tags": ["Chef story", "Ticket CTA", "Hospitality positioning"],
            },
        ],
        "closing_note": "This project matters because it shows that I can do more than design a pretty invitation. I can build the event, fill the seats, execute the night, and turn the experience into ongoing customer value.",
        "card_points": ["Chef sourcing", "Guest experience", "Post-event wine sales"],
    },
    {
        "slug": "midnight-bottle-drop",
        "theme": "teal",
        "category": "Splash Pages",
        "eyebrow": "Launch / Drop Page",
        "title": "Midnight Bottle Drop",
        "subtitle": "A fast splash-page system for a timed release, balancing urgency with enough editorial framing to feel intentional.",
        "summary": "This project turns a simple drop page into something sharper: a clear action path wrapped in mood, proof, and product context.",
        "homepage_summary": "Used social media to promote special events, new wines, and brand culture.",
        "hero_image": "media/midnight-bottle-drop.svg",
        "hero_alt": "Landing page mockup for a midnight bottle release",
        "scope": [
            {"value": "3", "label": "page states"},
            {"value": "1", "label": "countdown system"},
            {"value": "4", "label": "conversion modules"},
            {"value": "2", "label": "mobile breakpoints"},
        ],
        "roles": [
            "Landing page strategy",
            "UX writing",
            "Conversion hierarchy",
            "Art direction",
        ],
        "tools": [
            "Social media",
            "Photography",
            "Cross promotion",
            "Adobe",
        ],
        "deliverables": [
            "Pre-drop waitlist page",
            "Live drop page",
            "Sold-out fallback page",
            "Countdown and social assets",
        ],
        "challenge": "Timed launches can easily become generic urgency pages. The task here was to preserve speed and clarity while giving the drop a specific identity people would remember.",
        "approach": [
            {
                "title": "Give the page a before, during, and after state",
                "body": "The system plans for pre-launch waitlist mode, live-drop conversion mode, and sold-out mode so the story does not collapse when inventory changes.",
            },
            {
                "title": "Balance tempo and detail",
                "body": "The above-the-fold area is built for a quick decision, while lower modules let more curious shoppers understand why the product matters.",
            },
            {
                "title": "Make urgency feel branded",
                "body": "Typography, motion, and the countdown treatment support the mood instead of looking like a tacked-on commerce widget.",
            },
        ],
        "artifacts": [
            {
                "eyebrow": "State design",
                "title": "Three launch states",
                "copy": "Waitlist, live, and sold-out states share one visual system so the page still feels composed when the status changes.",
            },
            {
                "eyebrow": "Conversion UX",
                "title": "Single-decision hero",
                "copy": "The first screen is built around one action and one reason to care, reducing hesitation without stripping away mood.",
            },
            {
                "eyebrow": "Content framing",
                "title": "Editorial support below the fold",
                "copy": "Tasting notes, origin details, and serving cues support the sale instead of hiding behind generic specs.",
            },
        ],
        "social_examples": [
            {
                "eyebrow": "Social concept 01",
                "title": "Launch social post 01",
                "summary": "One of the vertical social assets created to support the Midnight Bottle Drop release.",
                "image": "media/social-media/midnight-bottle-drop-social-01.jpg",
            },
            {
                "eyebrow": "Social concept 02",
                "title": "Launch social post 02",
                "summary": "One of the vertical social assets created to support the Midnight Bottle Drop release.",
                "image": "media/social-media/midnight-bottle-drop-social-02.jpg",
            },
            {
                "eyebrow": "Social concept 03",
                "title": "Launch social post 03",
                "summary": "One of the vertical social assets created to support the Midnight Bottle Drop release.",
                "image": "media/social-media/midnight-bottle-drop-social-03.jpg",
            },
            {
                "eyebrow": "Social concept 04",
                "title": "Launch social post 04",
                "summary": "One of the vertical social assets created to support the Midnight Bottle Drop release.",
                "image": "media/social-media/midnight-bottle-drop-social-04.jpg",
            },
            {
                "eyebrow": "Social concept 05",
                "title": "Launch social post 05",
                "summary": "One of the vertical social assets created to support the Midnight Bottle Drop release.",
                "image": "media/social-media/midnight-bottle-drop-social-05.jpg",
            },
            {
                "eyebrow": "Social concept 06",
                "title": "Launch social post 06",
                "summary": "One of the vertical social assets created to support the Midnight Bottle Drop release.",
                "image": "media/social-media/midnight-bottle-drop-social-06.jpg",
            },
        ],
        "gallery": [],
        "closing_note": "This is the kind of page I like to build: crisp, narrow, and persuasive without feeling sterile.",
        "card_points": ["Launch pacing", "Conversion design", "Brand voice"],
    },
    {
        "slug": "bitter-orange-lambrusco-pdp",
        "theme": "rose",
        "category": "Product Pages",
        "eyebrow": "Merchandising / PDP System",
        "title": "Bitter Orange Lambrusco PDP",
        "subtitle": "A product-detail page system that blends taste, photography, and cross-sell logic into a more opinionated merch story.",
        "summary": "This page treats the product detail page like editorial merchandising, not a warehouse shelf with a button under it.",
        "homepage_title": "Website Updates",
        "homepage_subtitle": "Product, splash page, and event page website updates built to support merchandising, launches, and hospitality moments.",
        "homepage_summary": "",
        "hero_image": "media/bitter-orange-lambrusco-pdp.svg",
        "hero_alt": "Product page mockup featuring bottle photography, tasting notes, and bundle modules",
        "scope": [
            {"value": "1", "label": "hero PDP"},
            {"value": "5", "label": "content modules"},
            {"value": "2", "label": "cross-sell paths"},
            {"value": "1", "label": "bundle story"},
        ],
        "roles": [
            "Product storytelling",
            "Information hierarchy",
            "Photography direction",
            "Cross-sell strategy",
        ],
        "tools": [
            "Commerce7",
            "Inventory management",
            "Commerce7 collections",
            "Promotions",
            "Photography",
        ],
        "deliverables": [
            "PDP hero layout",
            "Tasting notes module",
            "Food pairing strip",
            "Bundle recommendation",
            "Mobile buy box refinement",
        ],
        "challenge": "Many product pages describe products correctly but fail to create desire. The goal was to make the PDP do better emotional and merchandising work without burying the purchase flow.",
        "approach": [
            {
                "title": "Lead with taste and shape",
                "body": "The product story starts with what the bottle feels like in the mouth and at the table, not just origin data and SKU details.",
            },
            {
                "title": "Use modules that earn their place",
                "body": "Every content block either sharpens understanding, increases confidence, or creates a higher-value path like a bundle.",
            },
            {
                "title": "Keep the buy box honest",
                "body": "The purchase controls stay visible and simple while the supporting modules do the seduction work around them.",
            },
        ],
        "artifacts": [
            {
                "eyebrow": "Hero content",
                "title": "Bottle story above the fold",
                "copy": "Large photography, compressed tasting notes, and one clean buy decision keep the top of the PDP direct and memorable.",
            },
            {
                "eyebrow": "Merchandising",
                "title": "Bundle logic",
                "copy": "Cross-sell is framed as a better meal or better occasion, not just a generic 'you may also like' box.",
            },
            {
                "eyebrow": "Mobile commerce",
                "title": "Thumb-first purchase flow",
                "copy": "Price, quantity, and CTA remain easy to reach while the story modules stack in a way that still feels premium.",
            },
        ],
        "product_examples": [
            {
                "eyebrow": "Example Page",
                "title": "2021 Cabernet Sauvignon Beauregard Ranch",
                "summary": "A Cabernet splash-page mockup built around estate history, mountain-vineyard specs, critic scores, and a more restrained luxury layout.",
                "file": "product_examples/beauregard-cabernet-splash.html",
            },
        ],
        "gallery": [],
        "closing_note": "This page helps show that I care about conversion, but I want conversion to come from sharper storytelling rather than more noise.",
        "card_points": ["PDP strategy", "Merchandising", "Mobile commerce"],
    },
]


PROJECT_MAP = {project["slug"]: project for project in PROJECTS}


def get_project(slug):
    return PROJECT_MAP.get(slug)


def get_related_projects(slug, limit=3):
    projects = [project for project in PROJECTS if project["slug"] != slug]
    return projects[:limit]
