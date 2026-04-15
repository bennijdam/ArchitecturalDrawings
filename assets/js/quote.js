/* Architectural Drawings — quote flow */
(() => {
  'use strict';

  const API_BASE = location.hostname === 'localhost'
    ? 'http://localhost:3001'
    : 'https://api.architecturaldrawings.co.uk';

  const form = document.getElementById('quoteForm');
  if (!form) return;

  const steps = Array.from(form.querySelectorAll('.quote-step'));
  const bars = document.querySelectorAll('.quote-progress-bar');
  const aside = document.getElementById('asideMessage');
  const summary = document.getElementById('quoteSummary');

  // Handle tier from query string
  const params = new URLSearchParams(window.location.search);
  if (params.get('tier')) {
    const tierSelect = form.querySelector('select[name="tier"]');
    if (tierSelect) tierSelect.value = params.get('tier');
  }

  let current = 1;

  // Service price map
  const servicePrices = {
    loft: { base: 1225, name: 'Loft Conversion' },
    'rear-ext': { base: 1225, name: 'Rear Extension' },
    'side-return': { base: 1225, name: 'Side Return Extension' },
    wraparound: { base: 1925, name: 'Wraparound Extension' },
    basement: { base: 2450, name: 'Basement Conversion' },
    mansard: { base: 1575, name: 'Mansard Roof' },
    'planning-only': { base: 840, name: 'Planning Drawings Only' },
    'buildingregs-only': { base: 840, name: 'Building Regs Only' },
    ldc: { base: 556, name: 'Lawful Development Certificate' },
    'flat-conv': { base: 2100, name: 'Flat Conversion' },
    hmo: { base: 2450, name: 'HMO Conversion' },
    other: { base: 0, name: 'Bespoke — to be quoted' }
  };

  const tierMultiplier = {
    essentials: 0.65,
    complete: 1.0,
    bespoke: 1.8
  };

  // Aside messages per step
  const asideMessages = {
    1: 'Tell us about your plan and we\'ll send a <em>free, fixed-fee quote</em> within the same working day.',
    2: 'We cover <em>everything</em> from a Certificate of Lawful Development to a basement conversion. Pick what fits.',
    3: 'Your postcode helps us <em>identify</em> Article 4 zones and conservation constraints before we quote.',
    4: 'We\'ll never share your details. <em>Expect a human reply</em> within the same working day.',
    5: 'Review your quote below. <em>Nothing is charged</em> — this just reserves a site-visit slot with a technologist.'
  };

  /* ---------- Navigation ---------- */
  const showStep = (n) => {
    steps.forEach((s) => s.classList.toggle('active', parseInt(s.dataset.step, 10) === n));
    bars.forEach((b) => {
      const barNum = parseInt(b.dataset.step, 10);
      b.classList.toggle('active', barNum === n);
      b.classList.toggle('done', barNum < n);
    });
    if (asideMessages[n] && aside) aside.innerHTML = asideMessages[n];
    current = n;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  /* ---------- Validation per step ---------- */
  const validateStep = (n) => {
    if (n === 1) {
      const chosen = form.querySelector('input[name="property"]:checked');
      if (!chosen) { alert('Please choose a property type.'); return false; }
    }
    if (n === 2) {
      const chosen = form.querySelector('input[name="service"]:checked');
      if (!chosen) { alert('Please choose a service.'); return false; }
    }
    if (n === 3) {
      const pc = form.querySelector('#q-postcode').value.trim();
      if (pc.length < 3) { alert('Please enter a valid UK postcode.'); form.querySelector('#q-postcode').focus(); return false; }
    }
    if (n === 4) {
      const name = form.querySelector('#q-name').value.trim();
      const email = form.querySelector('#q-email').value.trim();
      const consent = form.querySelector('input[name="consent"]').checked;
      if (!name) { alert('Please enter your name.'); form.querySelector('#q-name').focus(); return false; }
      if (!/^\S+@\S+\.\S+$/.test(email)) { alert('Please enter a valid email.'); form.querySelector('#q-email').focus(); return false; }
      if (!consent) { alert('Please tick the consent box to continue.'); return false; }
    }
    return true;
  };

  /* ---------- Selection UI ---------- */
  form.addEventListener('change', (e) => {
    if (e.target.matches('input[name="property"], input[name="service"]')) {
      // Update visual selected state
      const name = e.target.name;
      form.querySelectorAll(`input[name="${name}"]`).forEach((inp) => {
        inp.closest('.choice-card').classList.toggle('selected', inp.checked);
      });
    }
  });

  // Also respond to clicks on the labels themselves for clarity
  form.querySelectorAll('.choice-card').forEach((card) => {
    card.addEventListener('click', () => {
      const input = card.querySelector('input');
      if (input && !input.checked) {
        input.checked = true;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
  });

  /* ---------- Next / Prev ---------- */
  form.querySelectorAll('[data-next]').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (!validateStep(current)) return;
      const next = current + 1;
      if (next === 5) renderSummary();
      showStep(next);
    });
  });
  form.querySelectorAll('[data-prev]').forEach((btn) => {
    btn.addEventListener('click', () => showStep(Math.max(1, current - 1)));
  });

  /* ---------- Summary / Price calc ---------- */
  function renderSummary() {
    const property = form.querySelector('input[name="property"]:checked');
    const service = form.querySelector('input[name="service"]:checked');
    const tier = form.querySelector('#q-scope').value;
    const postcode = form.querySelector('#q-postcode').value.trim().toUpperCase();

    const svcKey = service ? service.value : 'other';
    const svcInfo = servicePrices[svcKey];
    const mult = tierMultiplier[tier] || 1;

    let price = Math.round((svcInfo.base * mult) / 5) * 5;
    if (svcInfo.base === 0) price = 0;

    const rows = [
      { label: 'Property', value: property ? property.value.replace('-', ' ').replace(/\b\w/g, c => c.toUpperCase()) : '—' },
      { label: 'Service', value: svcInfo.name },
      { label: 'Package tier', value: tier.charAt(0).toUpperCase() + tier.slice(1) },
      { label: 'Postcode', value: postcode || '—' },
      { label: '—line—', value: '' },
    ];

    summary.innerHTML = rows.map(r => {
      if (r.label === '—line—') return '<div style="height:1px;background:var(--line);margin:4px 0;"></div>';
      return `<div class="quote-summary-row"><span class="muted">${r.label}</span><strong>${r.value}</strong></div>`;
    }).join('') + (price > 0
        ? `<div class="quote-summary-row total"><span>Estimated fixed fee</span><strong>£${price.toLocaleString()} <span style="font-size:0.75rem;color:var(--ink-soft);font-family:var(--font-body);">+ VAT</span></strong></div>`
        : `<div class="quote-summary-row total"><span>Estimated fixed fee</span><strong class="serif" style="font-size:1.2rem;">Bespoke — we'll be in touch</strong></div>`);
  }

  /* ---------- Submit ---------- */
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Collect data
    const data = {
      property: form.querySelector('input[name="property"]:checked')?.value,
      service: form.querySelector('input[name="service"]:checked')?.value,
      tier: form.querySelector('#q-scope').value,
      timeline: form.querySelector('#q-timeline').value,
      postcode: form.querySelector('#q-postcode').value.trim(),
      notes: form.querySelector('#q-notes').value.trim(),
      name: form.querySelector('#q-name').value.trim(),
      email: form.querySelector('#q-email').value.trim(),
      phone: form.querySelector('#q-phone').value.trim(),
      createdAt: new Date().toISOString()
    };

    // Persist locally for demo continuity (in prod: POST /api/quotes)
    try {
      const quotes = JSON.parse(sessionStorage.getItem('ad_quotes') || '[]');
      quotes.push(data);
      sessionStorage.setItem('ad_quotes', JSON.stringify(quotes));
      sessionStorage.setItem('ad_last_quote', JSON.stringify(data));
    } catch (err) { /* storage may be disabled — silent */ }

    // POST to backend (if available)
    try {
      await fetch(`${API_BASE}/api/quotes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
    } catch (err) { /* backend optional in demo */ }

    showStep(6);
  });

  // Allow URL to jump directly
  if (params.get('step')) {
    const s = parseInt(params.get('step'), 10);
    if (s >= 1 && s <= 5) showStep(s);
  }

})();
