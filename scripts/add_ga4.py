from pathlib import Path
import re

ROOT = Path(r"c:\Users\ASUS\Desktop\ArchitecturalDrawings\architectural-drawings")
MEASUREMENT_ID = "G-77CQ2PWJM4"

SNIPPET = f'''<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
window.gtag = window.gtag || gtag;
gtag('js', new Date());
gtag('config', '{MEASUREMENT_ID}', {{
  anonymize_ip: true,
  page_title: document.title,
  page_location: window.location.href
}});

(() => {{
  const track = (name, params = {{}}) => {{
    try {{
      gtag('event', name, params);
    }} catch (err) {{}}
  }};

  let quoteStarted = false;

  document.addEventListener('focusin', (e) => {{
    const el = e.target;
    if (!(el instanceof Element)) return;
    const form = el.closest('form');
    if (!form) return;

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
      track('contact_click', {{
        contact_type: /^tel:/i.test(href) ? 'phone' : 'email',
        page_path: pagePath
      }});
    }}

    if (/\.(pdf|docx?|xlsx?|zip)(\?|#|$)/i.test(href)) {{
      const fileName = href.split('/').pop()?.split('?')[0] || 'download';
      track('file_download', {{ file_name: fileName, page_path: pagePath }});
    }}
  }}, true);
}})();
</script>'''

pattern = re.compile(r'<!-- Google Analytics 4 -->.*?</script>\s*</script>', re.S)
changed = 0
checked = 0

for html_file in ROOT.rglob('*.html'):
    if 'api' in html_file.parts:
        continue
    checked += 1
    content = html_file.read_text(encoding='utf-8')
    original = content

    if 'googletagmanager.com/gtag/js?id=' in content:
        content = re.sub(
            r'<!-- Google Analytics 4 -->.*?</script>\s*</script>',
            SNIPPET,
            content,
            flags=re.S,
        )
    elif '</head>' in content:
        content = content.replace('</head>', SNIPPET + '\n</head>', 1)

    if content != original:
        html_file.write_text(content, encoding='utf-8')
        changed += 1

print(f'Checked {{checked}} HTML files; updated {{changed}} files.')
