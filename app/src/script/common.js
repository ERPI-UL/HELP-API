export function redirectHome() {
    setTimeout(() => {
        if (document.referrer.startsWith(window.location.origin))
            window.location.href = document.referrer;
        else window.location.href = window.location.origin;
    }, 1000);
}