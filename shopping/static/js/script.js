document.addEventListener('DOMContentLoaded', function () {
    const alert = document.querySelector('[data-alert]');
    if (alert) {
        setTimeout(function () {
            alert.style.display = 'none';
        }, 5000);
    }
}, false);