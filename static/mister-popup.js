(function initMisterPopup() {
    const popup = document.getElementById("misterPopup");
    if (!popup) {
        return;
    }

    const sessionKey = "mister-popup-dismissed";
    const form = popup.querySelector("[data-mister-popup-form]");
    const emailInput = popup.querySelector("#misterPopupEmail");
    const message = popup.querySelector("#misterPopupMessage");
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

    function setMessage(text, isError = false) {
        if (!message || !form) {
            return;
        }

        message.textContent = text;
        form.classList.toggle("is-error", isError);
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

    form?.addEventListener("submit", (event) => {
        event.preventDefault();

        const email = emailInput?.value.trim() || "";
        const valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        if (!valid) {
            setMessage("Please enter a valid email address.", true);
            emailInput?.focus();
            return;
        }

        setMessage("Thank you. Mister will be in touch.", false);
        if (emailInput) {
            emailInput.disabled = true;
        }

        window.setTimeout(() => {
            closePopup();
        }, 900);
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
