const revealItems = Array.from(document.querySelectorAll("[data-reveal]"));
const mediaButtons = Array.from(document.querySelectorAll("[data-portfolio-media]"));
const carousels = Array.from(document.querySelectorAll("[data-carousel]"));

const dom = {
    lightbox: document.getElementById("portfolioLightbox"),
    lightboxImage: document.getElementById("portfolioLightboxImage"),
    lightboxTitle: document.getElementById("portfolioLightboxTitle"),
    lightboxCaption: document.getElementById("portfolioLightboxCaption"),
    lightboxPrev: document.getElementById("portfolioLightboxPrev"),
    lightboxNext: document.getElementById("portfolioLightboxNext"),
};

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const lightboxState = {
    group: null,
    index: 0,
    open: false,
};

const mediaGroups = mediaButtons.reduce((groups, button) => {
    const group = button.dataset.mediaGroup || "default";
    if (!groups[group]) {
        groups[group] = [];
    }
    groups[group].push(button);
    return groups;
}, {});

function visibleReveal() {
    if (reduceMotion) {
        revealItems.forEach((item) => item.classList.add("is-visible"));
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            });
        },
        { threshold: 0.14 }
    );

    revealItems.forEach((item) => observer.observe(item));
}

function groupItems(group) {
    return mediaGroups[group] || [];
}

function itemMeta(button) {
    return {
        src: button.dataset.mediaSrc,
        title: button.dataset.mediaTitle || "",
        caption: button.dataset.mediaCaption || "",
    };
}

function renderLightbox() {
    const buttons = groupItems(lightboxState.group);
    const activeButton = buttons[lightboxState.index];
    if (!activeButton) {
        return;
    }

    const meta = itemMeta(activeButton);
    dom.lightboxImage.src = meta.src;
    dom.lightboxImage.alt = meta.title;
    dom.lightboxTitle.textContent = meta.title;
    dom.lightboxCaption.textContent = meta.caption;

    if (dom.lightboxPrev && dom.lightboxNext) {
        const disabled = buttons.length <= 1;
        dom.lightboxPrev.disabled = disabled;
        dom.lightboxNext.disabled = disabled;
    }
}

function openLightbox(button) {
    if (!dom.lightbox) {
        return;
    }

    const group = button.dataset.mediaGroup || "default";
    const buttons = groupItems(group);
    lightboxState.group = group;
    lightboxState.index = buttons.indexOf(button);
    lightboxState.open = true;

    renderLightbox();
    dom.lightbox.hidden = false;
    document.body.classList.add("portfolio-lightbox-open");
}

function closeLightbox() {
    if (!dom.lightbox) {
        return;
    }

    lightboxState.open = false;
    dom.lightbox.hidden = true;
    document.body.classList.remove("portfolio-lightbox-open");
}

function stepLightbox(direction) {
    const buttons = groupItems(lightboxState.group);
    if (!lightboxState.open || buttons.length <= 1) {
        return;
    }

    lightboxState.index = (lightboxState.index + direction + buttons.length) % buttons.length;
    renderLightbox();
}

function initLightbox() {
    if (!dom.lightbox || !mediaButtons.length) {
        return;
    }

    mediaButtons.forEach((button) => {
        button.addEventListener("click", () => openLightbox(button));
    });

    dom.lightbox.querySelectorAll("[data-lightbox-close]").forEach((button) => {
        button.addEventListener("click", closeLightbox);
    });

    if (dom.lightboxPrev) {
        dom.lightboxPrev.addEventListener("click", () => stepLightbox(-1));
    }

    if (dom.lightboxNext) {
        dom.lightboxNext.addEventListener("click", () => stepLightbox(1));
    }

    document.addEventListener("keydown", (event) => {
        if (!lightboxState.open) {
            return;
        }

        if (event.key === "Escape") {
            closeLightbox();
        }

        if (event.key === "ArrowLeft") {
            stepLightbox(-1);
        }

        if (event.key === "ArrowRight") {
            stepLightbox(1);
        }
    });
}

function initCarousels() {
    carousels.forEach((carousel) => {
        const track = carousel.querySelector("[data-carousel-track]");
        const slides = Array.from(carousel.querySelectorAll("[data-carousel-slide]"));
        const prev = carousel.querySelector("[data-carousel-prev]");
        const next = carousel.querySelector("[data-carousel-next]");
        const dots = Array.from(carousel.querySelectorAll("[data-carousel-dot]"));
        const autoplayDelay = Number(carousel.dataset.carouselAutoplay) || 0;
        let activeIndex = 0;
        let autoplayId = null;

        if (!track || !slides.length) {
            return;
        }

        function stopAutoplay() {
            if (!autoplayId) {
                return;
            }

            window.clearInterval(autoplayId);
            autoplayId = null;
        }

        function startAutoplay() {
            if (reduceMotion || autoplayDelay <= 0 || slides.length <= 1 || autoplayId) {
                return;
            }

            autoplayId = window.setInterval(() => {
                activeIndex = (activeIndex + 1) % slides.length;
                render();
            }, autoplayDelay);
        }

        function restartAutoplay() {
            stopAutoplay();
            startAutoplay();
        }

        function render() {
            track.style.transform = `translateX(-${activeIndex * 100}%)`;

            slides.forEach((slide, index) => {
                const isActive = index === activeIndex;
                slide.classList.toggle("is-active", isActive);
                slide.setAttribute("aria-hidden", isActive ? "false" : "true");
            });

            dots.forEach((dot, index) => {
                const isActive = index === activeIndex;
                dot.classList.toggle("is-active", isActive);
                dot.setAttribute("aria-selected", isActive ? "true" : "false");
            });
        }

        prev?.addEventListener("click", () => {
            activeIndex = (activeIndex - 1 + slides.length) % slides.length;
            render();
            restartAutoplay();
        });

        next?.addEventListener("click", () => {
            activeIndex = (activeIndex + 1) % slides.length;
            render();
            restartAutoplay();
        });

        dots.forEach((dot) => {
            dot.addEventListener("click", () => {
                activeIndex = Number(dot.dataset.carouselIndex) || 0;
                render();
                restartAutoplay();
            });
        });

        carousel.addEventListener("mouseenter", stopAutoplay);
        carousel.addEventListener("mouseleave", startAutoplay);
        carousel.addEventListener("focusin", stopAutoplay);
        carousel.addEventListener("focusout", () => {
            if (!carousel.contains(document.activeElement)) {
                startAutoplay();
            }
        });

        document.addEventListener("visibilitychange", () => {
            if (document.hidden) {
                stopAutoplay();
                return;
            }

            startAutoplay();
        });

        render();
        startAutoplay();
    });
}

function disableExternalLinks(root = document) {
    const links = Array.from(root.querySelectorAll('a[href^="http://"], a[href^="https://"]'));

    links.forEach((link) => {
        if (link.dataset.externalDisabled === "true") {
            return;
        }

        const originalHref = link.getAttribute("href");
        link.dataset.externalDisabled = "true";
        link.dataset.originalHref = originalHref || "";
        link.removeAttribute("href");
        link.removeAttribute("target");
        link.removeAttribute("rel");
        link.setAttribute("aria-disabled", "true");
        link.setAttribute("tabindex", "-1");
        link.addEventListener("click", (event) => event.preventDefault());
    });
}

function disableExternalLinksInIframes() {
    document.querySelectorAll("iframe").forEach((frame) => {
        const apply = () => {
            try {
                if (frame.contentDocument) {
                    disableExternalLinks(frame.contentDocument);
                }
            } catch {
                // Ignore cross-origin frames.
            }
        };

        frame.addEventListener("load", apply);
        apply();
    });
}

visibleReveal();
initLightbox();
initCarousels();
disableExternalLinks();
disableExternalLinksInIframes();
