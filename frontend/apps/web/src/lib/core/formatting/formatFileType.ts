export function formatFileType(type: string): string {
  const mimetype = type.split(";")[0];
  return mimetype.split("/").pop()?.split(".").pop()?.toUpperCase() ?? "";
}
