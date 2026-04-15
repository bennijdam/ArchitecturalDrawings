import * as Sentry from '@sentry/node';

const dsn = process.env.SENTRY_DSN;
export const sentryEnabled = Boolean(dsn);

if (sentryEnabled) {
  Sentry.init({
    dsn,
    sendDefaultPii: true,
    tracesSampleRate: Number(process.env.SENTRY_TRACES_SAMPLE_RATE || 0.2),
  });
}

export { Sentry };
