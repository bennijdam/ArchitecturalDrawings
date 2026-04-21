/**
 * Email template system — Architectural Drawings London
 * Design: ultra-minimal premium, dark navy header, blueprint blue accent.
 * All layouts are table-based for Outlook compatibility.
 * Inline styles only — no external CSS, no CSS variables.
 */

const BRAND = {
  name: 'Architectural Drawings',
  tagline: 'MCIAT Chartered · London',
  url: process.env.ALLOWED_ORIGIN || 'https://www.architecturaldrawings.uk',
  email: 'hello@architecturaldrawings.uk',
  address: '86–90 Paul Street, London EC2A 4NE',
  accent: '#2563EB',
  accentDeep: '#1D4ED8',
  ink: '#0B1222',
  inkSoft: '#3B4F72',
  inkSofter: '#56688A',
  bg: '#F5F8FF',
  bgDeep: '#0A0F1E',
  surface: '#FFFFFF',
  success: '#47845A',
};

/* ── Shared building blocks ─────────────────────────────────────────── */

function logoHtml() {
  return `
    <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto 0 0;">
      <tr>
        <td style="background:#2563EB;border-radius:8px;width:32px;height:32px;text-align:center;vertical-align:middle;">
          <span style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;font-weight:700;color:#ffffff;line-height:32px;">A</span>
        </td>
        <td style="padding-left:10px;vertical-align:middle;">
          <span style="font-family:Georgia,'Times New Roman',serif;font-size:17px;font-weight:400;color:#ffffff;letter-spacing:-0.02em;">Architectural</span>
          <span style="font-family:Georgia,'Times New Roman',serif;font-size:17px;font-weight:400;color:#2563EB;font-style:italic;margin-left:5px;">Drawings</span>
        </td>
      </tr>
    </table>`;
}

function headerHtml(title, subtitle) {
  return `
  <!-- Header -->
  <tr>
    <td style="background:linear-gradient(160deg,#142040 0%,#0A0F1E 100%);padding:40px 48px 36px;border-radius:16px 16px 0 0;">
      ${logoHtml()}
      <div style="margin-top:32px;">
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#2563EB;margin:0 0 10px;">Architectural Drawings · London</p>
        <h1 style="font-family:Georgia,'Times New Roman',serif;font-size:28px;font-weight:400;color:#ffffff;margin:0;line-height:1.15;letter-spacing:-0.02em;">${title}</h1>
        ${subtitle ? `<p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:rgba(255,255,255,0.55);margin:10px 0 0;line-height:1.5;">${subtitle}</p>` : ''}
      </div>
    </td>
  </tr>`;
}

function bodyStart() {
  return `
  <!-- Body card -->
  <tr>
    <td style="background:#ffffff;padding:40px 48px 8px;">`;
}

function bodyEnd() {
  return `
    </td>
  </tr>`;
}

function divider() {
  return `<div style="border-top:1px solid rgba(11,18,34,0.08);margin:28px 0;"></div>`;
}

function ctaButton(text, url, style = 'primary') {
  const bg = style === 'primary'
    ? 'linear-gradient(135deg,#1a2744 0%,#0B1222 100%)'
    : 'linear-gradient(135deg,#3b82f6 0%,#2563EB 100%)';
  const color = '#ffffff';
  return `
    <table cellpadding="0" cellspacing="0" border="0" style="margin:28px auto 0;width:auto;">
      <tr>
        <td style="background:${bg};border-radius:999px;padding:16px 32px;text-align:center;">
          <a href="${url}" style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;font-weight:600;color:${color};text-decoration:none;white-space:nowrap;display:inline-block;">${text}</a>
        </td>
      </tr>
    </table>`;
}

function ctaButtonFull(text, url, style = 'primary') {
  const bg = style === 'primary'
    ? 'linear-gradient(135deg,#1a2744 0%,#0B1222 100%)'
    : 'linear-gradient(135deg,#3b82f6 0%,#2563EB 100%)';
  return `
    <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin:28px 0 0;">
      <tr>
        <td style="background:${bg};border-radius:999px;padding:18px 32px;text-align:center;">
          <a href="${url}" style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:16px;font-weight:600;color:#ffffff;text-decoration:none;display:block;">${text}</a>
        </td>
      </tr>
    </table>`;
}

function infoRow(label, value) {
  return `
    <tr>
      <td style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;padding:9px 0;border-bottom:1px solid rgba(11,18,34,0.06);width:40%;vertical-align:top;">${label}</td>
      <td style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px;font-weight:500;color:#0B1222;padding:9px 0 9px 16px;border-bottom:1px solid rgba(11,18,34,0.06);vertical-align:top;">${value || '—'}</td>
    </tr>`;
}

function infoTable(rows) {
  return `
    <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin:20px 0;">
      ${rows.map(([label, value]) => infoRow(label, value)).join('')}
    </table>`;
}

function highlightBox(text, subtext) {
  return `
    <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin:24px 0;">
      <tr>
        <td style="background:#EBF0FF;border-radius:12px;padding:24px;text-align:center;border:1px solid rgba(37,99,235,0.12);">
          <div style="font-family:Georgia,'Times New Roman',serif;font-size:36px;font-weight:400;color:#2563EB;letter-spacing:-0.02em;line-height:1;">${text}</div>
          ${subtext ? `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin-top:8px;">${subtext}</div>` : ''}
        </td>
      </tr>
    </table>`;
}

function footerHtml() {
  return `
  <!-- Footer -->
  <tr>
    <td style="background:#0A0F1E;padding:32px 48px;border-radius:0 0 16px 16px;">
      <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:12px;color:rgba(255,255,255,0.35);margin:0 0 8px;line-height:1.6;">
        <strong style="color:rgba(255,255,255,0.6);">Architectural Drawings Ltd</strong><br>
        ${BRAND.address}<br>
        <a href="mailto:${BRAND.email}" style="color:rgba(255,255,255,0.4);text-decoration:none;">${BRAND.email}</a>
      </p>
      <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:11px;color:rgba(255,255,255,0.2);margin:16px 0 0;line-height:1.5;">
        Registered in England No. 14872049 · MCIAT Chartered · ICO Registered<br>
        © ${new Date().getFullYear()} Architectural Drawings Ltd. All rights reserved.
      </p>
    </td>
  </tr>`;
}

function wrap(innerRows) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="color-scheme" content="light" />
  <meta name="supported-color-schemes" content="light" />
  <!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
  <style>
    @media only screen and (max-width:600px) {
      .email-wrapper { padding: 16px !important; }
      .email-card td { padding-left: 24px !important; padding-right: 24px !important; }
    }
  </style>
</head>
<body style="margin:0;padding:0;background-color:#EBF0FB;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#EBF0FB;">
    <tr>
      <td class="email-wrapper" align="center" style="padding:40px 16px;">
        <table class="email-card" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:580px;border-radius:16px;overflow:hidden;box-shadow:0 8px 40px rgba(11,18,34,0.12),0 40px 100px rgba(11,18,34,0.08);">
          ${innerRows}
        </table>
      </td>
    </tr>
  </table>
</body>
</html>`;
}

/* ── Individual email templates ─────────────────────────────────────── */

export function passwordResetEmail({ name, resetUrl }) {
  const firstName = (name || 'there').split(' ')[0];
  return {
    subject: 'Reset your password — Architectural Drawings',
    html: wrap(`
      ${headerHtml('Reset your<br>password.', 'Your reset link is valid for 1 hour.')}
      ${bodyStart()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:16px;color:#0B1222;margin:0 0 16px;line-height:1.6;">Hi ${firstName},</p>
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:#3B4F72;margin:0 0 8px;line-height:1.6;">
          We received a request to reset the password for your Architectural Drawings account.
          Click below to set a new password.
        </p>
        ${ctaButtonFull('Reset my password', resetUrl, 'blue')}
        ${divider()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin:0 0 8px;line-height:1.6;">
          Or copy this link into your browser:
        </p>
        <p style="font-family:'Courier New',Courier,monospace;font-size:12px;color:#2563EB;margin:0;word-break:break-all;background:#EBF0FF;padding:12px 16px;border-radius:8px;">${resetUrl}</p>
        ${divider()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin:0;line-height:1.6;">
          If you didn't request this, you can safely ignore this email. Your password won't change.
        </p>
        <div style="height:40px;"></div>
      ${bodyEnd()}
      ${footerHtml()}
    `),
    text: `Hi ${firstName},\n\nReset your Architectural Drawings password here:\n\n${resetUrl}\n\nThis link expires in 1 hour. If you didn't request this, ignore this email.\n\nArchitectural Drawings London\n${BRAND.address}`,
  };
}

export function passwordChangedEmail({ name }) {
  const firstName = (name || 'there').split(' ')[0];
  return {
    subject: 'Your password has been changed — Architectural Drawings',
    html: wrap(`
      ${headerHtml('Password<br>updated.', 'Your account is secure.')}
      ${bodyStart()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:16px;color:#0B1222;margin:0 0 16px;line-height:1.6;">Hi ${firstName},</p>
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:#3B4F72;margin:0 0 20px;line-height:1.6;">
          Your Architectural Drawings account password was successfully changed.
          You can now sign in with your new password.
        </p>
        <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin:0 0 24px;">
          <tr>
            <td style="background:#EBF0FF;border-radius:12px;padding:20px 24px;border-left:3px solid #2563EB;">
              <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;font-weight:600;color:#0B1222;margin:0 0 4px;">Wasn't you?</p>
              <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#3B4F72;margin:0;line-height:1.5;">
                If you didn't make this change, contact us immediately at
                <a href="mailto:${BRAND.email}" style="color:#2563EB;text-decoration:none;">${BRAND.email}</a>.
              </p>
            </td>
          </tr>
        </table>
        ${ctaButton('Sign in to your portal', `${BRAND.url}/portal/login.html`)}
        <div style="height:40px;"></div>
      ${bodyEnd()}
      ${footerHtml()}
    `),
    text: `Hi ${firstName},\n\nYour Architectural Drawings password was changed successfully.\n\nIf this wasn't you, contact us: ${BRAND.email}\n\nArchitectural Drawings London`,
  };
}

export function welcomeEmail({ name, email }) {
  const firstName = (name || 'there').split(' ')[0];
  return {
    subject: `Welcome to Architectural Drawings, ${firstName}`,
    html: wrap(`
      ${headerHtml(`Welcome,<br>${firstName}.`, 'Your portal is ready.')}
      ${bodyStart()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:#3B4F72;margin:0 0 24px;line-height:1.6;">
          Your Architectural Drawings account has been created. From your portal you can track
          projects, upload documents, review drawings, and pay in instalments — all in one place.
        </p>

        <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin-bottom:8px;">
          <tr>
            <td style="background:#F5F8FF;border-radius:12px;padding:20px 24px;">
              <table cellpadding="0" cellspacing="0" border="0" style="width:100%;">
                <tr>
                  <td style="width:36px;vertical-align:top;padding-right:14px;padding-top:2px;">
                    <div style="width:28px;height:28px;background:#EBF0FF;border-radius:8px;text-align:center;line-height:28px;">
                      <span style="font-size:14px;">📋</span>
                    </div>
                  </td>
                  <td>
                    <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px;font-weight:600;color:#0B1222;margin:0 0 3px;">Request a quote</p>
                    <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin:0;line-height:1.5;">Fixed fees from £840. Answer 5 questions and get an instant price.</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr><td style="height:8px;"></td></tr>
          <tr>
            <td style="background:#F5F8FF;border-radius:12px;padding:20px 24px;">
              <table cellpadding="0" cellspacing="0" border="0" style="width:100%;">
                <tr>
                  <td style="width:36px;vertical-align:top;padding-right:14px;padding-top:2px;">
                    <div style="width:28px;height:28px;background:#EBF0FF;border-radius:8px;text-align:center;line-height:28px;">
                      <span style="font-size:14px;">📁</span>
                    </div>
                  </td>
                  <td>
                    <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px;font-weight:600;color:#0B1222;margin:0 0 3px;">Upload your documents</p>
                    <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin:0;line-height:1.5;">Share existing plans, deeds, or photos securely through your portal.</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr><td style="height:8px;"></td></tr>
          <tr>
            <td style="background:#F5F8FF;border-radius:12px;padding:20px 24px;">
              <table cellpadding="0" cellspacing="0" border="0" style="width:100%;">
                <tr>
                  <td style="width:36px;vertical-align:top;padding-right:14px;padding-top:2px;">
                    <div style="width:28px;height:28px;background:#EBF0FF;border-radius:8px;text-align:center;line-height:28px;">
                      <span style="font-size:14px;">✅</span>
                    </div>
                  </td>
                  <td>
                    <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px;font-weight:600;color:#0B1222;margin:0 0 3px;">Track approvals in real time</p>
                    <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin:0;line-height:1.5;">See planning application status and council decisions the moment they land.</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>

        ${ctaButtonFull('Open my portal', `${BRAND.url}/portal/dashboard.html`, 'blue')}
        ${divider()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:12px;color:#56688A;margin:0;line-height:1.6;">
          Signed in as <strong style="color:#0B1222;">${email}</strong> ·
          <a href="mailto:${BRAND.email}" style="color:#2563EB;text-decoration:none;">Get help</a>
        </p>
        <div style="height:40px;"></div>
      ${bodyEnd()}
      ${footerHtml()}
    `),
    text: `Welcome to Architectural Drawings, ${firstName}!\n\nYour portal is ready: ${BRAND.url}/portal/dashboard.html\n\nFixed-fee planning drawings, building regulations and loft conversions across all 33 London boroughs.\n\nArchitectural Drawings London\n${BRAND.address}`,
  };
}

export function quoteConfirmationEmail({ name, service, tier, postcode, quoteId }) {
  const firstName = (name || 'there').split(' ')[0];
  const serviceLabel = service ? service.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) : 'Your service';
  const tierLabel = tier ? tier.charAt(0).toUpperCase() + tier.slice(1) : null;
  return {
    subject: `We've received your quote request — Architectural Drawings`,
    html: wrap(`
      ${headerHtml('Quote<br>received.', "We\u2019ll be in touch within 1 working day.")}
      ${bodyStart()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:16px;color:#0B1222;margin:0 0 16px;line-height:1.6;">Hi ${firstName},</p>
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:#3B4F72;margin:0 0 4px;line-height:1.6;">
          Thank you for your quote request. Our chartered technologists will review your
          details and contact you within one working day to confirm scope and next steps.
        </p>
        ${infoTable([
          ['Service', serviceLabel],
          ['Package', tierLabel],
          ['Postcode', postcode],
          ['Reference', quoteId ? `#${quoteId}` : null],
        ])}
        <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin:0 0 4px;">
          <tr>
            <td style="background:#EBF0FF;border-radius:12px;padding:20px 24px;border-left:3px solid #2563EB;">
              <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;font-weight:600;color:#0B1222;margin:0 0 6px;">What happens next</p>
              <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#3B4F72;margin:0;line-height:1.6;">
                1. We'll call or email to confirm your project scope.<br>
                2. We'll schedule your site survey (60–90 min, laser-measured).<br>
                3. First drawings delivered within 10 working days of survey.
              </p>
            </td>
          </tr>
        </table>
        ${divider()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin:0;line-height:1.6;">
          Questions? Reply to this email or call
          <a href="tel:02079460000" style="color:#2563EB;text-decoration:none;">020 7946 0000</a>.
        </p>
        <div style="height:40px;"></div>
      ${bodyEnd()}
      ${footerHtml()}
    `),
    text: `Hi ${firstName},\n\nWe've received your quote request for ${serviceLabel} in ${postcode}.\n\nWe'll be in touch within 1 working day.\n\nRef: #${quoteId || '—'}\n\nArchitectural Drawings London\n${BRAND.address}`,
  };
}

export function quoteOpsEmail({ name, email, phone, service, tier, property, postcode, timeline, notes, quoteId }) {
  const serviceLabel = service ? service.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) : '—';
  const tierLabel = tier ? tier.charAt(0).toUpperCase() + tier.slice(1) : '—';
  return {
    subject: `[Quote #${quoteId}] ${name} · ${serviceLabel} · ${postcode}`,
    html: wrap(`
      ${headerHtml(`New quote<br>request.`, `${serviceLabel} · ${postcode}`)}
      ${bodyStart()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:#3B4F72;margin:0 0 4px;line-height:1.6;">
          A new quote was submitted via the website.
        </p>
        ${infoTable([
          ['Reference', `#${quoteId}`],
          ['Name', name],
          ['Email', `<a href="mailto:${email}" style="color:#2563EB;text-decoration:none;">${email}</a>`],
          ['Phone', phone ? `<a href="tel:${phone}" style="color:#2563EB;text-decoration:none;">${phone}</a>` : null],
          ['Service', serviceLabel],
          ['Package', tierLabel],
          ['Property type', property],
          ['Postcode', postcode],
          ['Timeline', timeline],
        ])}
        ${notes ? `
        <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin-top:4px;">
          <tr>
            <td style="background:#F5F8FF;border-radius:12px;padding:16px 20px;">
              <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#56688A;margin:0 0 8px;">Notes from client</p>
              <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:14px;color:#0B1222;margin:0;line-height:1.6;">${notes}</p>
            </td>
          </tr>
        </table>` : ''}
        ${ctaButton('View in admin', `${BRAND.url}/portal/dashboard.html`)}
        <div style="height:40px;"></div>
      ${bodyEnd()}
      ${footerHtml()}
    `),
    text: `New quote #${quoteId}\n\nName: ${name}\nEmail: ${email}\nPhone: ${phone || '—'}\nService: ${serviceLabel}\nPackage: ${tierLabel}\nProperty: ${property}\nPostcode: ${postcode}\nTimeline: ${timeline}\nNotes: ${notes || '—'}`,
  };
}

export function paymentConfirmationEmail({ name, amountGbp, projectTitle, paymentId, receiptUrl }) {
  const firstName = (name || 'there').split(' ')[0];
  const formatted = amountGbp
    ? `£${Number(amountGbp).toLocaleString('en-GB', { minimumFractionDigits: 2 })}`
    : '—';
  return {
    subject: `Payment confirmed — Architectural Drawings`,
    html: wrap(`
      ${headerHtml('Payment<br>confirmed.', 'Thank you — your project is progressing.')}
      ${bodyStart()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:16px;color:#0B1222;margin:0 0 16px;line-height:1.6;">Hi ${firstName},</p>
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:#3B4F72;margin:0 0 4px;line-height:1.6;">
          We've received your payment. Your project is progressing and your technologist
          will be in touch with your next milestone shortly.
        </p>
        ${highlightBox(formatted, projectTitle ? `for &ldquo;${projectTitle}&rdquo;` : 'payment received')}
        ${infoTable([
          ['Payment ref', paymentId ? `#${paymentId}` : null],
          ['Project', projectTitle],
          ['Date', new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })],
        ])}
        ${receiptUrl ? ctaButton('View receipt', receiptUrl) : ''}
        ${ctaButton('Open my portal', `${BRAND.url}/portal/dashboard.html`, 'blue')}
        ${divider()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin:0;line-height:1.6;">
          Keep this email as your record. For queries email
          <a href="mailto:${BRAND.email}" style="color:#2563EB;text-decoration:none;">${BRAND.email}</a>.
        </p>
        <div style="height:40px;"></div>
      ${bodyEnd()}
      ${footerHtml()}
    `),
    text: `Hi ${firstName},\n\nPayment of ${formatted} confirmed for "${projectTitle}".\n\nRef: #${paymentId || '—'}\n\nView your portal: ${BRAND.url}/portal/dashboard.html\n\nArchitectural Drawings London`,
  };
}

export function callbackOpsEmail({ name, phone, callWhen, topic, sourceIp, referrer, requestPath, userAgent }) {
  return {
    subject: `[Callback] ${name} — ${callWhen || 'ASAP'}`,
    html: wrap(`
      ${headerHtml('Callback<br>request.', callWhen ? `Requested for: ${callWhen}` : 'As soon as possible')}
      ${bodyStart()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:#3B4F72;margin:0 0 4px;line-height:1.6;">
          A callback was requested via the website.
        </p>
        ${infoTable([
          ['Name', name],
          ['Phone', `<a href="tel:${phone}" style="color:#2563EB;text-decoration:none;">${phone}</a>`],
          ['When', callWhen || 'As soon as possible'],
          ['Topic', topic],
          ['Received', new Date().toLocaleString('en-GB', { timeZone: 'Europe/London' })],
        ])}
        ${divider()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:11px;color:#56688A;margin:0;line-height:1.7;">
          <strong style="color:#3B4F72;">Source IP:</strong> ${sourceIp || 'Unknown'}<br>
          <strong style="color:#3B4F72;">Referrer:</strong> ${referrer || 'Direct'}<br>
          <strong style="color:#3B4F72;">Path:</strong> ${requestPath || '—'}<br>
          <strong style="color:#3B4F72;">User agent:</strong> ${userAgent || '—'}
        </p>
        <div style="height:40px;"></div>
      ${bodyEnd()}
      ${footerHtml()}
    `),
    text: `Callback request\n\nName: ${name}\nPhone: ${phone}\nWhen: ${callWhen || 'ASAP'}\nTopic: ${topic || '—'}\n\nIP: ${sourceIp}\nReferrer: ${referrer}\nPath: ${requestPath}`,
  };
}

export function drawingReadyEmail({ name, projectTitle, portalUrl }) {
  const firstName = (name || 'there').split(' ')[0];
  return {
    subject: `Your drawings are ready — Architectural Drawings`,
    html: wrap(`
      ${headerHtml('Your drawings<br>are ready.', 'Review and approve in your portal.')}
      ${bodyStart()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:16px;color:#0B1222;margin:0 0 16px;line-height:1.6;">Hi ${firstName},</p>
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:15px;color:#3B4F72;margin:0 0 20px;line-height:1.6;">
          The first draft drawings for <strong style="color:#0B1222;">${projectTitle || 'your project'}</strong> have been
          uploaded to your portal and are ready for your review.
        </p>
        <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin-bottom:24px;">
          <tr>
            <td style="background:#F5F8FF;border-radius:12px;padding:20px 24px;border-left:3px solid #47845A;">
              <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;font-weight:600;color:#0B1222;margin:0 0 6px;">Next steps</p>
              <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#3B4F72;margin:0;line-height:1.6;">
                1. Open your portal and review the drawings.<br>
                2. Leave comments or mark as approved.<br>
                3. We'll incorporate any changes within 3 working days — unlimited revisions included.
              </p>
            </td>
          </tr>
        </table>
        ${ctaButtonFull('Review my drawings', portalUrl || `${BRAND.url}/portal/dashboard.html`, 'blue')}
        ${divider()}
        <p style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;font-size:13px;color:#56688A;margin:0;line-height:1.6;">
          Once approved, we'll proceed to planning submission. Questions?
          <a href="mailto:${BRAND.email}" style="color:#2563EB;text-decoration:none;">Reply to this email</a>.
        </p>
        <div style="height:40px;"></div>
      ${bodyEnd()}
      ${footerHtml()}
    `),
    text: `Hi ${firstName},\n\nYour first draft drawings for "${projectTitle}" are ready to review.\n\nOpen your portal: ${portalUrl || BRAND.url + '/portal/dashboard.html'}\n\nLeave any comments and we'll update within 3 working days.\n\nArchitectural Drawings London`,
  };
}
