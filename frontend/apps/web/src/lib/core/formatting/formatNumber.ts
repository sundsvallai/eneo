/**
 * Format a number with either comma separators for thousands (full format)
 * or with appropriate suffix (K, M, B, T) for compact format
 *
 * @param num The number to format
 * @param options Formatting options: "full" (comma separators, default) or "compact" (K, M, B, T)
 * @param decimals Number of decimal places to include (only used in compact format)
 * @returns Formatted string representation of the number
 */
export function formatNumber(
  num: number,
  options: "compact" | "full" = "full",
  decimals = 0
): string {
  // Handle NaN
  if (isNaN(num)) return "0";

  // Handle zero
  if (num === 0) return "0";

  // Handle negative numbers
  if (num < 0) return "-" + formatNumber(-num, options, decimals);

  if (options === "full") {
    // Full format: comma-separated thousands
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  } else {
    // Compact format: K, M, B, T suffixes
    const k = 1000;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["", "K", "M", "B", "T"];

    const i = Math.floor(Math.log(num) / Math.log(k));

    // If number is less than 1000, don't use a suffix
    if (i === 0) return num.toString();

    // Otherwise format with appropriate suffix
    return `${(num / Math.pow(k, i)).toFixed(dm)}${sizes[i]}`;
  }
}
