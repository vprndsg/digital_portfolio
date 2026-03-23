(function initMisterPopup() {
    const popup = document.getElementById("misterPopup");
    if (!popup) {
        return;
    }

    const sessionKey = "mister-popup-dismissed";
    const closeTriggers = Array.from(
        popup.querySelectorAll("[data-mister-popup-close], [data-mister-popup-dismiss]")
    );
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let timerId = null;

    function readSessionFlag() {
        try {
            return window.sessionStorage.getItem(sessionKey) === "1";
        } catch (error) {
            return false;
        }
    }

    function writeSessionFlag() {
        try {
            window.sessionStorage.setItem(sessionKey, "1");
        } catch (error) {
            // Ignore storage availability failures and fall back to this-page behavior.
        }
    }

    function closePopup() {
        if (popup.hidden) {
            return;
        }

        popup.classList.remove("is-visible");
        popup.hidden = true;
        document.body.classList.remove("mister-popup-open");
        writeSessionFlag();
    }

    function openPopup() {
        if (readSessionFlag() || !popup.hidden) {
            return;
        }

        popup.hidden = false;
        document.body.classList.add("mister-popup-open");

        if (reduceMotion) {
            popup.classList.add("is-visible");
        } else {
            window.requestAnimationFrame(() => {
                popup.classList.add("is-visible");
            });
        }

        popup.querySelector(".mister-popup__close")?.focus();
    }

    closeTriggers.forEach((trigger) => {
        trigger.addEventListener("click", () => {
            closePopup();
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !popup.hidden) {
            closePopup();
        }
    });

    if (readSessionFlag()) {
        return;
    }

    timerId = window.setTimeout(openPopup, 4000);

    window.addEventListener("pagehide", () => {
        if (timerId) {
            window.clearTimeout(timerId);
        }
    });
})();
