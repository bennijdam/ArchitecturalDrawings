export function getEmailMessageId(result) {
  return result?.data?.id || result?.id || null;
}

export function logEmailSent(eventName, details, result) {
  const emailMessageId = getEmailMessageId(result);
  console.info(`[${eventName}]`, JSON.stringify({
    ...details,
    emailMessageId,
  }));
  return emailMessageId;
}