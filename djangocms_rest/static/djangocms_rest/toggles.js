document.addEventListener('DOMContentLoaded', function() {
    const toggles = document.querySelectorAll('.js-kvp:has(.indent)');

    toggles.forEach(kvp => {
        const content = kvp.querySelector('& > .indent');
        const toggle = kvp.querySelector('& > .toggle');
        if (content) {
            content.dataset.scrollHeight = content.scrollHeight;
        }
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            kvp.classList.toggle('hidden');
        });
        toggle.addEventListener('dblclick', function(e) {
            e.stopPropagation();
        });
    });
});