#!/usr/bin/env python3
"""Add live chat widget placeholder to all HTML pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WIDGET = '''<!-- chat-widget -->
<div id="chatWidget" style="position:fixed;left:1.25rem;bottom:1.25rem;z-index:85;">
  <button id="chatToggle" aria-label="Chat with us" style="width:52px;height:52px;border-radius:50%;background:var(--ink);color:var(--bg);display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);border:0;cursor:pointer;transition:transform 0.3s var(--ease);">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  </button>
  <div id="chatPanel" style="display:none;position:absolute;bottom:64px;left:0;width:320px;background:var(--surface);border-radius:var(--r-lg);box-shadow:var(--shadow-lg);overflow:hidden;">
    <div style="background:var(--ink);color:var(--bg);padding:16px 20px;">
      <div style="font-weight:600;font-size:0.95rem;">Chat with us</div>
      <div style="font-size:0.78rem;color:rgba(250,250,247,0.6);margin-top:2px;">Typically replies in under 5 minutes</div>
    </div>
    <div style="padding:20px;">
      <div style="background:var(--bg-2);border-radius:var(--r-md);padding:14px 16px;font-size:0.9rem;color:var(--ink-soft);margin-bottom:16px;">Hi! How can we help with your project? Ask us about planning, costs, or timescales.</div>
      <form id="chatForm" style="display:flex;gap:8px;">
        <input type="text" placeholder="Type a message..." required style="flex:1;padding:10px 14px;border:1px solid var(--line);border-radius:var(--r-full);font-size:0.88rem;" />
        <button type="submit" style="width:38px;height:38px;border-radius:50%;background:var(--accent);color:#fff;border:0;cursor:pointer;display:grid;place-items:center;"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg></button>
      </form>
    </div>
  </div>
</div>
<script>(function(){var t=document.getElementById('chatToggle'),p=document.getElementById('chatPanel'),f=document.getElementById('chatForm');if(t&&p){t.addEventListener('click',function(){p.style.display=p.style.display==='none'?'block':'none';});}if(f){f.addEventListener('submit',function(e){e.preventDefault();f.innerHTML='<p style="color:var(--success);font-size:0.9rem;padding:8px;">Thanks! We&rsquo;ll reply shortly.</p>';});}})();</script>
'''

EXCLUDE_DIRS = {'portal', 'api', 'node_modules', '__pycache__'}

updated = 0
skipped = 0

for f in ROOT.rglob('*.html'):
    if any(p in EXCLUDE_DIRS for p in f.parts):
        continue
    text = f.read_text(encoding='utf-8')
    if 'chat-widget' in text:
        skipped += 1
        continue
    # Insert before </body>
    if '</body>' not in text:
        continue
    text = text.replace('</body>', WIDGET + '\n</body>', 1)
    f.write_text(text, encoding='utf-8')
    updated += 1

print(f'[OK] Added chat widget to {updated} pages (skipped {skipped} already-widgeted)')
