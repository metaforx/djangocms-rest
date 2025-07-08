document.addEventListener('DOMContentLoaded', function() {
    const toggles = document.querySelectorAll('.js-kvp:has(.indent)');
    toggles.forEach(kvp => {
        const content = kvp.querySelector('& > .indent');
        const toggle = kvp.querySelector('& > .key, & > .children');
        if (content) {
            content.dataset.scrollHeight = content.scrollHeight;
        }
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            kvp.classList.toggle('hidden');

        });
    });
});