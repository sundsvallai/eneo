export function formatWebsiteName(website: { url: string; name?: string | null }) {
  if (website.name) {
    return website.name;
  }

  const shortenedUrl = website.url.split("//")[1];
  return shortenedUrl ?? website.url;
}
