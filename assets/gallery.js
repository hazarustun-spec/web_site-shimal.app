'use strict';
const gallery = document.querySelector('#screenshots');
const links = [...document.querySelectorAll('[data-gallery-index]')];
const controls = document.querySelector('.gallery-controls');
const previous = document.querySelector('[data-gallery-prev]');
const next = document.querySelector('[data-gallery-next]');
const dialog = document.querySelector('#screenshot-dialog');
const image = document.querySelector('#viewer-image');
const caption = document.querySelector('#viewer-caption');
const viewerPrevious = document.querySelector('#viewer-prev');
const viewerNext = document.querySelector('#viewer-next');
let current = 0;
let opener;
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function updateControls() {
  previous.disabled = gallery.scrollLeft < 2;
  next.disabled = gallery.scrollLeft + gallery.clientWidth >= gallery.scrollWidth - 2;
}
function scrollGallery(direction) {
  gallery.scrollBy({ left: direction * gallery.clientWidth * 0.8, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
}
function showScreenshot(index) {
  current = Math.max(0, Math.min(links.length - 1, index));
  image.src = links[current].href;
  image.alt = links[current].querySelector('img').alt;
  caption.textContent = `${current + 1} / ${links.length} — ${document.querySelector('#app-title').textContent}`;
  viewerPrevious.disabled = current === 0;
  viewerNext.disabled = current === links.length - 1;
}
controls.hidden = false;
previous.addEventListener('click', () => scrollGallery(-1));
next.addEventListener('click', () => scrollGallery(1));
gallery.addEventListener('scroll', updateControls, { passive: true });
window.addEventListener('resize', updateControls);
updateControls();
if (typeof dialog.showModal === 'function') {
  links.forEach((link, index) => link.addEventListener('click', event => {
    event.preventDefault();
    opener = link;
    showScreenshot(index);
    dialog.showModal();
  }));
  document.querySelector('#close-viewer').addEventListener('click', () => dialog.close());
  viewerPrevious.addEventListener('click', () => showScreenshot(current - 1));
  viewerNext.addEventListener('click', () => showScreenshot(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showScreenshot(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('click', event => {
    const bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => opener?.focus());
}
