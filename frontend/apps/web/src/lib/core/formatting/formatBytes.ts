/**
 * Format a size attribute in bytes as human-readable file size, e.g. `1024` will return `"1 KiB"`
 * Returns "- Bytes" for negative values
 */
export function formatBytes(bytes: number, decimals = 0) {
  if (bytes < 0) return "- Bytes";
  if (!+bytes) return "0 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${(bytes / Math.pow(k, i)).toFixed(dm)} ${sizes[i]}`;
}
