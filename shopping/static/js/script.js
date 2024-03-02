document.addEventListener('DOMContentLoaded', function () {
    const alert = document.querySelector('[data-alert]');
    if (alert) {
        setTimeout(function () {
            alert.style.display = 'none';
        }, 5000);
    }
}, false);

function changeIconColor(green = true) {
    const svg = document.getElementById('svgPopupIcon');
    if (green) {
        svg.classList.remove('text-red-400', 'dark:text-red-400');
        svg.classList.add('text-green-400', 'dark:text-green-400');
    } else {
        svg.classList.remove('text-green-400', 'dark:text-green-400');
        svg.classList.add('text-red-400', 'dark:text-red-400');
    }
}

// Path: shopping/static/js/script.js