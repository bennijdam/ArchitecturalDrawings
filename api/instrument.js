import * as Sentry from '@sentry/node';

const dsn = process.env.SENTRY_DSN;
export const sentryEnabled = Boolean(dsn);

if (sentryEnabled) {
  Sentry.init({
    dsn,
    environment: process.env.SENTRY_ENVIRONMENT || process.env.NODE_ENV || 'development',
    release: process.env.SENTRY_RELEASE,
    sendDefaultPii: process.env.SENTRY_SEND_DEFAULT_PII === 'true',
    tracesSampleRate: Number(process.env.SENTRY_TRACES_SAMPLE_RATE || 0.2),
    beforeSend(event) {
      if (event.request?.headers) {
        const headers = { ...event.request.headers };
        delete headers.authorization;
        delete headers.cookie;
        delete headers['x-api-key'];
        event.request.headers = headers;
      }
      return event;
    },
  });
}

export { Sentry };
