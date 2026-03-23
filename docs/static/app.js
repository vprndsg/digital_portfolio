const siteConfig = window.SITE_CONFIG || {};
const forecastDataCache = new Map();

const state = {
    experience: window.INITIAL_STATE,
    lightbox: {
        galleryId: 0,
        index: 0,
        open: false,
    },
};

const dom = {
    datePicker: document.getElementById("datePicker"),
    copyLinkButton: document.getElementById("copyLinkButton"),
    copyStatus: document.getElementById("copyStatus"),
    readingDate: document.getElementById("readingDate"),
    todayPhaseName: document.getElementById("todayPhaseName"),
    todaySignal: document.getElementById("todaySignal"),
    todayRibbon: document.getElementById("todayRibbon"),
    decisionVerdict: document.getElementById("decisionVerdict"),
    decisionHeadline: document.getElementById("decisionHeadline"),
    decisionSummary: document.getElementById("decisionSummary"),
    focusList: document.getElementById("focusList"),
    futureForecast: document.getElementById("futureForecast"),
    controlsPanel: document.getElementById("controlsPanel"),
    readingPanel: document.getElementById("readingPanel"),
    futurePanel: document.getElementById("futurePanel"),
    storyCards: Array.from(document.querySelectorAll("[data-story-card]")),
    lightbox: document.getElementById("lightbox"),
    lightboxImage: document.getElementById("lightboxImage"),
    lightboxTitle: document.getElementById("lightboxTitle"),
    lightboxCaption: document.getElementById("lightboxCaption"),
    lightboxStrip: document.getElementById("lightboxStrip"),
    lightboxPrev: document.getElementById("lightboxPrev"),
    lightboxNext: document.getElementById("lightboxNext"),
};

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function normalizedLabel(value) {
    return String(value ?? "").trim().toLowerCase();
}

function displayDate(value) {
    const date = new Date(`${value}T12:00:00`);
    return new Intl.DateTimeFormat("en-US", {
        month: "short",
        day: "numeric",
    }).format(date).toUpperCase();
}

function currentPacificDate() {
    const formatter = new Intl.DateTimeFormat("en-CA", {
        timeZone: siteConfig.time_zone || "America/Los_Angeles",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
    });
    const parts = formatter.formatToParts(new Date());
    const values = Object.fromEntries(parts.map((part) => [part.type, part.value]));
    return `${values.year}-${values.month}-${values.day}`;
}

function selectionFromQuery() {
    const params = new URLSearchParams(window.location.search);
    const party = normalizedLabel(params.get("party"));
    const appetite = normalizedLabel(params.get("appetite"));
    return {
        date: params.get("date") || "",
        party: ["solo", "pair", "crowd"].includes(party) ? party : "",
        appetite: ["comfort", "electric", "curious"].includes(appetite) ? appetite : "",
    };
}

function isSupportedDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(value))) {
        return false;
    }
    if (siteConfig.supported_min_date && value < siteConfig.supported_min_date) {
        return false;
    }
    if (siteConfig.supported_max_date && value > siteConfig.supported_max_date) {
        return false;
    }
    return true;
}

function applySupportedDateRange() {
    if (!dom.datePicker) {
        return;
    }
    if (siteConfig.supported_min_date) {
        dom.datePicker.min = siteConfig.supported_min_date;
    }
    if (siteConfig.supported_max_date) {
        dom.datePicker.max = siteConfig.supported_max_date;
    }
}

function applySelection(selection) {
    if (dom.datePicker) {
        dom.datePicker.value = selection.date;
    }

    const partyInput = document.querySelector(`input[name="party"][value="${selection.party}"]`);
    const appetiteInput = document.querySelector(`input[name="appetite"][value="${selection.appetite}"]`);

    if (partyInput) {
        partyInput.checked = true;
    }
    if (appetiteInput) {
        appetiteInput.checked = true;
    }
}

function currentSelection() {
    const partyMode = document.querySelector('input[name="party"]:checked')?.value || state.experience.party_mode;
    const appetite = document.querySelector('input[name="appetite"]:checked')?.value || state.experience.appetite;
    return {
        date: dom.datePicker?.value || state.experience.requested_date,
        party: partyMode,
        appetite,
    };
}

function selectionMatchesExperience(selection) {
    return (
        selection.date === state.experience.requested_date &&
        selection.party === state.experience.party_mode &&
        selection.appetite === state.experience.appetite
    );
}

function updateQueryString() {
    const selection = currentSelection();
    const query = new URLSearchParams(selection);
    const queryString = query.toString();
    const nextUrl = queryString ? `${window.location.pathname}?${queryString}` : window.location.pathname;
    window.history.replaceState({}, "", nextUrl);
}

function toneClass(dayType) {
    if (dayType === "Root Day") {
        return "root";
    }
    if (dayType === "Leaf Day") {
        return "leaf";
    }
    if (dayType === "Flower Day") {
        return "flower";
    }
    return "fruit";
}

function setTheme() {
    const today = state.experience.today;
    document.documentElement.style.setProperty("--signal", today.palette_primary);
    document.documentElement.style.setProperty("--panel-border", today.palette_primary);
    dom.readingPanel.dataset.tone = toneClass(today.day_type);
}

function focusItems(today) {
    return [
        `Focus on: ${today.day_type.replace(" Day", "").toLowerCase()} energy`,
        `Plate move: ${today.pizza_name}`,
        `Bottle mood: ${today.wine_name}`,
    ];
}

function renderToday() {
    const today = state.experience.today;
    dom.readingDate.textContent = displayDate(today.date);
    dom.todayPhaseName.textContent = today.moon_phase;
    dom.todaySignal.textContent = today.signal_name;
    dom.todayRibbon.textContent = `${today.motion.toUpperCase()} MOON | ${today.day_type.toUpperCase()} | ${displayDate(today.date)}`;
    dom.decisionVerdict.textContent = state.experience.decision.verdict;
    dom.decisionHeadline.textContent = state.experience.decision.headline;
    dom.decisionSummary.textContent = state.experience.decision.summary;
    dom.focusList.innerHTML = focusItems(today).map(
        (item, index) => `
            <li style="--item-delay:${index * 90}ms">
                <span>${escapeHtml(item)}</span>
            </li>
        `
    ).join("");
}

function forecastCard(item, index) {
    const tone = toneClass(item.day_type);
    return `
        <article class="forecast-card forecast-card-${tone}" style="--card-delay:${index * 90}ms">
            <div class="forecast-emblem forecast-emblem-${tone}">
                <span>${escapeHtml(item.day_type.replace(" Day", ""))}<br>DAY</span>
            </div>
            <div class="forecast-meta">
                <h3>${escapeHtml(displayDate(item.date))}</h3>
                <p class="forecast-line"><span>Lunar phase: ${escapeHtml(item.moon_phase)}</span></p>
                <p class="forecast-line"><span>Drinking well: ${escapeHtml(item.drinking_well)}</span></p>
                <p class="forecast-line"><span>Focus: ${escapeHtml(item.top_axis)} | ${escapeHtml(item.motion)}</span></p>
            </div>
        </article>
    `;
}

function renderFutureForecast() {
    const nextThree = state.experience.future_forecast || [];
    dom.futureForecast.innerHTML = nextThree.map((item, index) => forecastCard(item, index)).join("");
}

function syncForm() {
    applySelection({
        date: state.experience.requested_date,
        party: state.experience.party_mode,
        appetite: state.experience.appetite,
    });
}

function renderExperience() {
    setTheme();
    syncForm();
    renderToday();
    renderFutureForecast();
    updateQueryString();
}

function setLoading(isLoading) {
    [dom.controlsPanel, dom.readingPanel, dom.futurePanel].forEach((panel) => {
        panel.classList.toggle("is-loading", isLoading);
    });
}

function usesApiForecast() {
    return siteConfig.mode === "api";
}

async function loadForecastMonth(dateValue) {
    const monthKey = String(dateValue).slice(0, 7);
    if (!monthKey) {
        throw new Error("Missing month key");
    }

    if (!forecastDataCache.has(monthKey)) {
        const baseUrl = (siteConfig.forecast_data_base_url || "").replace(/\/$/, "");
        const request = fetch(`${baseUrl}/${monthKey}.json`).then(async (response) => {
            if (!response.ok) {
                throw new Error(`Request failed with ${response.status}`);
            }
            return response.json();
        });
        forecastDataCache.set(monthKey, request);
    }

    return forecastDataCache.get(monthKey);
}

async function fetchExperience() {
    setLoading(true);
    const selection = currentSelection();

    try {
        let nextState = null;

        if (usesApiForecast()) {
            const query = new URLSearchParams(selection);
            const response = await fetch(`${siteConfig.forecast_api_path || "/api/forecast"}?${query.toString()}`);
            if (!response.ok) {
                throw new Error(`Request failed with ${response.status}`);
            }
            nextState = await response.json();
        } else {
            const monthData = await loadForecastMonth(selection.date);
            nextState = monthData?.[selection.date]?.[selection.party]?.[selection.appetite];
        }

        if (!nextState) {
            throw new Error("Forecast data missing for selection");
        }

        const commit = () => {
            state.experience = nextState;
            renderExperience();
        };

        if (document.startViewTransition) {
            const transition = document.startViewTransition(commit);
            await transition.finished.catch(() => {});
        } else {
            commit();
        }
    } finally {
        setLoading(false);
    }
}

async function copyLink() {
    updateQueryString();
    try {
        await navigator.clipboard.writeText(window.location.href);
        dom.copyStatus.textContent = "Link copied.";
    } catch (error) {
        dom.copyStatus.textContent = "Could not copy automatically.";
    }
}

function galleryEntry(galleryId) {
    return window.BLOG_ENTRIES[galleryId];
}

function syncCardMedia(card, mediaIndex) {
    const entry = galleryEntry(Number(card.dataset.galleryId));
    const media = entry.media[mediaIndex];
    const mainImage = card.querySelector("[data-media-main]");
    const titleLabel = card.querySelector("[data-media-title]");
    const caption = card.querySelector("[data-media-caption]");
    const openButton = card.querySelector("[data-media-open]");

    card.dataset.activeIndex = String(mediaIndex);
    card.classList.add("is-swapping");
    mainImage.src = media.image;
    mainImage.alt = media.title;
    titleLabel.textContent = media.title;
    caption.textContent = media.caption;
    openButton.dataset.mediaIndex = String(mediaIndex);
    openButton.setAttribute("aria-label", `Open ${media.title}`);

    card.querySelectorAll("[data-media-thumb]").forEach((thumb, index) => {
        thumb.classList.toggle("is-active", index === mediaIndex);
    });

    window.setTimeout(() => {
        card.classList.remove("is-swapping");
    }, 220);
}

function openLightbox(galleryId, mediaIndex) {
    state.lightbox.galleryId = galleryId;
    state.lightbox.index = mediaIndex;
    state.lightbox.open = true;
    renderLightbox();
    dom.lightbox.hidden = false;
    requestAnimationFrame(() => {
        dom.lightbox.classList.add("is-open");
    });
    document.body.classList.add("lightbox-active");
}

function closeLightbox() {
    state.lightbox.open = false;
    dom.lightbox.classList.remove("is-open");
    document.body.classList.remove("lightbox-active");
    window.setTimeout(() => {
        if (!state.lightbox.open) {
            dom.lightbox.hidden = true;
        }
    }, 220);
}

function renderLightbox() {
    const entry = galleryEntry(state.lightbox.galleryId);
    const media = entry.media[state.lightbox.index];
    dom.lightboxImage.src = media.image;
    dom.lightboxImage.alt = media.title;
    dom.lightboxTitle.textContent = media.title;
    dom.lightboxCaption.textContent = media.caption;

    dom.lightboxStrip.innerHTML = entry.media.map((item, index) => `
        <button
            class="lightbox-thumb${index === state.lightbox.index ? " is-active" : ""}"
            type="button"
            data-lightbox-thumb="${index}"
            aria-label="View ${escapeHtml(item.title)}"
        >
            <img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.title)}">
        </button>
    `).join("");

    dom.lightboxPrev.disabled = entry.media.length <= 1;
    dom.lightboxNext.disabled = entry.media.length <= 1;

    dom.lightboxStrip.querySelectorAll("[data-lightbox-thumb]").forEach((thumb) => {
        thumb.addEventListener("click", () => {
            state.lightbox.index = Number(thumb.dataset.lightboxThumb);
            renderLightbox();
        });
    });
}

function stepLightbox(direction) {
    const entry = galleryEntry(state.lightbox.galleryId);
    const total = entry.media.length;
    if (total <= 1) {
        return;
    }
    state.lightbox.index = (state.lightbox.index + direction + total) % total;
    renderLightbox();
}

function bindStoryCards() {
    dom.storyCards.forEach((card, galleryId) => {
        card.dataset.galleryId = String(galleryId);
        card.dataset.activeIndex = "0";
        const openButton = card.querySelector("[data-media-open]");
        const expandButton = card.querySelector("[data-expand-button]");

        openButton.addEventListener("click", () => {
            openLightbox(galleryId, Number(card.dataset.activeIndex || "0"));
        });

        card.querySelectorAll("[data-media-thumb]").forEach((thumb) => {
            thumb.addEventListener("click", () => {
                syncCardMedia(card, Number(thumb.dataset.mediaIndex));
            });
        });

        expandButton.dataset.defaultLabel = expandButton.textContent;
        expandButton.addEventListener("click", () => {
            const willOpen = !card.classList.contains("is-open");

            dom.storyCards.forEach((otherCard) => {
                const otherButton = otherCard.querySelector("[data-expand-button]");
                otherCard.classList.remove("is-open");
                otherButton.setAttribute("aria-expanded", "false");
                otherButton.textContent = otherButton.dataset.defaultLabel;
            });

            if (willOpen) {
                card.classList.add("is-open");
                expandButton.setAttribute("aria-expanded", "true");
                expandButton.textContent = "Close";
            }
        });
    });
}

function bindLightbox() {
    dom.lightbox.querySelectorAll("[data-lightbox-close]").forEach((element) => {
        element.addEventListener("click", closeLightbox);
    });
    dom.lightboxPrev.addEventListener("click", () => stepLightbox(-1));
    dom.lightboxNext.addEventListener("click", () => stepLightbox(1));
    document.addEventListener("keydown", (event) => {
        if (!state.lightbox.open) {
            return;
        }
        if (event.key === "Escape") {
            closeLightbox();
        } else if (event.key === "ArrowLeft") {
            stepLightbox(-1);
        } else if (event.key === "ArrowRight") {
            stepLightbox(1);
        }
    });
}

function bindTiltSurfaces() {
    if (!window.matchMedia("(pointer:fine)").matches) {
        return;
    }
    document.querySelectorAll("[data-tilt]").forEach((surface) => {
        surface.addEventListener("pointermove", (event) => {
            const rect = surface.getBoundingClientRect();
            const x = (event.clientX - rect.left) / rect.width - 0.5;
            const y = (event.clientY - rect.top) / rect.height - 0.5;
            surface.style.setProperty("--tilt-x", `${x * 6}deg`);
            surface.style.setProperty("--tilt-y", `${y * -6}deg`);
            surface.style.setProperty("--glow-x", `${(x + 0.5) * 100}%`);
            surface.style.setProperty("--glow-y", `${(y + 0.5) * 100}%`);
        });
        surface.addEventListener("pointerleave", () => {
            surface.style.setProperty("--tilt-x", "0deg");
            surface.style.setProperty("--tilt-y", "0deg");
            surface.style.setProperty("--glow-x", "50%");
            surface.style.setProperty("--glow-y", "50%");
        });
    });
}

function retireRevealClasses() {
    document.querySelectorAll(".reveal").forEach((element) => {
        element.addEventListener("animationend", () => {
            element.classList.remove("reveal");
        }, { once: true });
    });
}

function bindControls() {
    dom.datePicker.addEventListener("change", () => {
        fetchExperience().catch(() => {
            dom.copyStatus.textContent = "Could not refresh the forecast.";
        });
    });

    document.querySelectorAll('input[name="party"]').forEach((input) => {
        input.addEventListener("change", () => {
            fetchExperience().catch(() => {
                dom.copyStatus.textContent = "Could not refresh the forecast.";
            });
        });
    });

    document.querySelectorAll('input[name="appetite"]').forEach((input) => {
        input.addEventListener("change", () => {
            fetchExperience().catch(() => {
                dom.copyStatus.textContent = "Could not refresh the forecast.";
            });
        });
    });

    dom.copyLinkButton.addEventListener("click", copyLink);
}

async function initializeExperience() {
    applySupportedDateRange();

    const querySelection = selectionFromQuery();
    const fallbackDate = isSupportedDate(currentPacificDate())
        ? currentPacificDate()
        : state.experience.requested_date;
    const targetSelection = {
        date: isSupportedDate(querySelection.date) ? querySelection.date : fallbackDate,
        party: querySelection.party || state.experience.party_mode,
        appetite: querySelection.appetite || state.experience.appetite,
    };

    if (querySelection.date && !isSupportedDate(querySelection.date)) {
        dom.copyStatus.textContent = "Requested date is outside the published forecast range.";
    }

    renderExperience();

    if (!selectionMatchesExperience(targetSelection)) {
        applySelection(targetSelection);
        try {
            await fetchExperience();
        } catch (error) {
            applySelection({
                date: state.experience.requested_date,
                party: state.experience.party_mode,
                appetite: state.experience.appetite,
            });
            renderExperience();
            if (!dom.copyStatus.textContent) {
                dom.copyStatus.textContent = "Could not load the forecast.";
            }
        }
    }
}

async function initialize() {
    bindControls();
    bindStoryCards();
    bindLightbox();
    bindTiltSurfaces();
    retireRevealClasses();
    await initializeExperience();
}

initialize().catch(() => {
    renderExperience();
    dom.copyStatus.textContent = "Could not load the forecast.";
});
