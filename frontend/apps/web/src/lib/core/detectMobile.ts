const mobileRegex1 = new RegExp("/Mobile|iP(hone|od|ad)|Android|BlackBerry|IEMobile/");
export function detectMobile(userAgent: string): boolean {
  return mobileRegex1.test(userAgent);
}
