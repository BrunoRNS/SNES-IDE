/**
 * SNES-IDE - gh-pages script.js
 * Copyright (C) 2025 BrunoRNS
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

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
    showPage('home');

    document.querySelectorAll('nav a').forEach(a => {

        a.addEventListener('click', e => {

            e.preventDefault();
            showPage(a.getAttribute('data-page'));

        });

    });

});