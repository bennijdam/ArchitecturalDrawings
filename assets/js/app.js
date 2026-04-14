/* Architectural Drawings — main site interactions */
(() => {
  'use strict';

  /* ---------- Scroll-triggered reveals ---------- */
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('in'));
  }

  /* ---------- Nav scroll state ---------- */
  const nav = document.getElementById('nav');
  if (nav) {
    const onScroll = () => {
      nav.classList.toggle('scrolled', window.scrollY > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Mobile menu ---------- */
  const btnMenu = document.getElementById('btnMenu');
  if (btnMenu) {
    btnMenu.addEventListener('click', () => {
      // Simple mobile menu — show/hide via a classname on body
      document.body.classList.toggle('menu-open');
      const navLinks = document.querySelector('.nav-links');
      if (navLinks) {
        navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '64px';
        navLinks.style.left = '0';
        navLinks.style.right = '0';
        navLinks.style.background = 'var(--bg)';
        navLinks.style.flexDirection = 'column';
        navLinks.style.padding = '16px 24px';
        navLinks.style.borderBottom = '1px solid var(--line)';
      }
    });
  }

  /* ---------- FAQ accordion (details element behaves natively, but add smooth height) ---------- */
  // Using <details> native for accessibility; add class for CSS styling
  document.querySelectorAll('.faq-item').forEach((item) => {
    item.addEventListener('toggle', () => {
      item.classList.toggle('open', item.open);
    });
  });

  /* ---------- Search widget — enhance behavior ---------- */
  const searchForm = document.querySelector('.search-widget');
  if (searchForm) {
    const input = searchForm.querySelector('input[type="search"]');
    if (input) {
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') input.blur();
      });
    }
  }

  /* ---------- Smooth anchor scrolling with nav offset ---------- */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const id = anchor.getAttribute('href');
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const navHeight = nav ? nav.offsetHeight : 0;
      const y = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
      window.scrollTo({ top: y, behavior: 'smooth' });
    });
  });

  /* ---------- Progressive enhancement for picture sources ---------- */
  // Modern browsers handle AVIF natively via <picture>, no JS needed

})();
