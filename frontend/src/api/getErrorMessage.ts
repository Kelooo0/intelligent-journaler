export function getErrorMessage(message: string, fallback: string): string {
  if (message) {
    try {
      const parsed_message = JSON.parse(message);
      const detail = parsed_message.detail;

      if (typeof detail === "string") {
        return parsed_message.detail;
      }
      if (Array.isArray(detail)) {
        const msg = detail[0].msg;

        if (typeof msg === "string") {
          return msg;
        }
      }
    } catch {
      return fallback;
    }
  }
  return fallback;
}
