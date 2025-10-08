// SPA navigation
function showPage(pageId) {

    document.querySelectorAll('section[data-page]').forEach(sec => {

        sec.classList.add('hidden');

    });

    document.getElementById(pageId).classList.remove('hidden');
    document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
    document.querySelector('nav a[data-page="'+pageId+'"]').classList.add('active');
    
    window.scrollTo(0,0);

}

window.addEventListener('DOMContentLoaded', () => {
    // Default to home
    showPage('home');

    document.querySelectorAll('nav a').forEach(a => {

        a.addEventListener('click', e => {

            e.preventDefault();
            showPage(a.getAttribute('data-page'));

        });

    });

});