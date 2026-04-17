from pathlib import Path
import re

ROOT = Path(r"c:\Users\ASUS\Desktop\ArchitecturalDrawings\architectural-drawings")
MEASUREMENT_ID = "G-77CQ2PWJM4"

SNIPPET = f'''<!-- Google Analytics 4 (standardized) -->
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
window.gtag = window.gtag || gtag;
gtag('js', new Date());
gtag('config', '{MEASUREMENT_ID}', {{
  anonymize_ip: true,
  allow_google_signals: false,
  page_title: document.title,
  page_location: window.location.href,
  send_page_view: true
}});

(() => {{
  const track = (name, params = {{}}) => {{
    try {{
      gtag('event', name, params);
    }} catch (err) {{}}
  }};

  const startedForms = new Set();
  const scrollMilestones = new Set();
  const scrollTargets = [25, 50, 75, 90];

  let quoteStarted = false;
  let rafScheduled = false;

  setTimeout(() => {{
    track('session_engaged_30s', {{
      page_path: window.location.pathname,
      page_title: document.title
    }});
  }}, 30000);

  const handleScroll = () => {{
    rafScheduled = false;
    const doc = document.documentElement;
    const maxScroll = Math.max(1, (doc.scrollHeight || 0) - window.innerHeight);
    const pct = Math.round((window.scrollY / maxScroll) * 100);
    scrollTargets.forEach((target) => {{
      if (pct >= target && !scrollMilestones.has(target)) {{
        scrollMilestones.add(target);
        track('scroll_depth', {{
          percent_scrolled: target,
          page_path: window.location.pathname
        }});
      }}
    }});
  }};

  window.addEventListener('scroll', () => {{
    if (rafScheduled) return;
    rafScheduled = true;
    window.requestAnimationFrame(handleScroll);
  }}, {{ passive: true }});

  document.addEventListener('focusin', (e) => {{
    const el = e.target;
    if (!(el instanceof Element)) return;
    const form = el.closest('form');
    if (!form) return;

    const formId = form.id || form.getAttribute('name') || 'form';
    if (!startedForms.has(formId)) {{
      startedForms.add(formId);
      track('form_start', {{
        form_id: formId,
        page_path: window.location.pathname
      }});
    }}

    if (form.id === 'quoteForm' && !quoteStarted) {{
      quoteStarted = true;
      track('quote_form_start', {{
        form_id: 'quoteForm',
        page_path: window.location.pathname
      }});
    }}
  }}, true);

  document.addEventListener('submit', (e) => {{
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;

    const pagePath = window.location.pathname;
    const formId = form.id || form.getAttribute('name') || 'form';

    track('form_submit', {{ form_id: formId, page_path: pagePath }});

    if (formId === 'quoteForm') {{
      const service = form.querySelector('input[name="service"]:checked')?.value || '';
      const tier = form.querySelector('#q-scope')?.value || form.querySelector('[name="tier"]')?.value || '';
      track('generate_lead', {{ form_id: formId, page_path: pagePath, service, tier }});
      track('quote_submit', {{ form_id: formId, page_path: pagePath, service, tier }});
      return;
    }}

    const queryInput = form.querySelector('input[name="q"], input[type="search"]');
    if (queryInput && queryInput.value.trim()) {{
      track('search', {{ search_term: queryInput.value.trim(), page_path: pagePath }});
    }}

    if (/login/i.test(pagePath) || /login/i.test(formId)) {{
      track('login', {{ method: 'email', page_path: pagePath }});
      return;
    }}

    if (/register|signup|sign-up/i.test(pagePath) || /register|signup|sign-up/i.test(formId)) {{
      track('sign_up', {{ method: 'email', page_path: pagePath }});
    }}
  }}, true);

  document.addEventListener('change', (e) => {{
    const el = e.target;
    if (!(el instanceof Element)) return;

    const inQuoteForm = !!el.closest('#quoteForm');
    if (!inQuoteForm) return;

    if (el.matches('input[name="property"], input[name="service"], #q-scope, #q-timeline')) {{
      track('quote_option_select', {{
        field: el.getAttribute('name') || el.getAttribute('id') || 'unknown',
        value: (el.value || '').toString().slice(0, 80),
        page_path: window.location.pathname
      }});
    }}
  }}, true);

  document.addEventListener('click', (e) => {{
    const el = e.target;
    if (!(el instanceof Element)) return;

    const trigger = el.closest('a,button');
    if (!trigger) return;

    const text = (trigger.textContent || trigger.getAttribute('aria-label') || '')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 100);
    const href = trigger.getAttribute('href') || '';
    const pagePath = window.location.pathname;
    const combined = `${{text}} ${{href}}`.toLowerCase();

    if (combined.includes('quote') || combined.includes('reserve my slot') || combined.includes('free quote')) {{
      track('cta_click', {{ cta_text: text || 'quote_cta', cta_target: href || pagePath, page_path: pagePath }});
    }}

    if (/^mailto:/i.test(href) || /^tel:/i.test(href)) {{
      const contactType = /^tel:/i.test(href) ? 'phone' : 'email';
      track('contact_click', {{
        contact_type: contactType,
        page_path: pagePath
      }});
      track(contactType === 'phone' ? 'phone_click' : 'email_click', {{
        event_category: 'contact',
        event_label: href.replace(/^mailto:|^tel:/i, ''),
        page_path: pagePath
      }});
    }}

    if (/\.(pdf|docx?|xlsx?|zip)(\?|#|$)/i.test(href)) {{
      const fileName = href.split('/').pop()?.split('?')[0] || 'download';
      track('file_download', {{ file_name: fileName, page_path: pagePath }});
    }}

    if (/^https?:\/\//i.test(href)) {{
      try {{
        const url = new URL(href, window.location.href);
        if (url.hostname !== window.location.hostname) {{
          track('outbound_click', {{
            link_domain: url.hostname,
            link_url: url.href,
            page_path: pagePath
          }});
        }}
      }} catch (_err) {{}}
    }}
  }}, true);
}})();
</script>'''

PAIR_PATTERN = re.compile(
    r'(?:<!--\s*Google Analytics 4(?: \(standardized\))?\s*-->\s*)?'
    r'<script[^>]*src=["\']https://www\.googletagmanager\.com/gtag/js\?id=[^"\']+["\'][^>]*></script>\s*'
    r'<script>.*?</script>',
    re.S | re.I,
)
changed = 0
checked = 0

for html_file in ROOT.rglob('*.html'):
    if 'api' in html_file.parts or 'node_modules' in html_file.parts:
        continue
    checked += 1
    content = html_file.read_text(encoding='utf-8')
    original = content

    if 'googletagmanager.com/gtag/js?id=' in content:
      content = PAIR_PATTERN.sub(lambda _m: SNIPPET, content, count=1)
    elif '</head>' in content:
        content = content.replace('</head>', SNIPPET + '\n</head>', 1)

    if content != original:
        html_file.write_text(content, encoding='utf-8')
        changed += 1

print(f'Checked {checked} HTML files; updated {changed} files.')
