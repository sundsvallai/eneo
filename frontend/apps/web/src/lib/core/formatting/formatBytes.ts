/**
 * Format a size attribute in bytes as human-readable file size, e.g. `1024` will return `"1 KiB"`
 * If a negavtive number is sent in, it will take the absolute
 */
export function formatBytes(bytes: number, decimals = 0) {
  bytes = Math.abs(bytes);
  if (!+bytes) return "0 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}
