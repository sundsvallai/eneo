import { browser } from "$app/environment";
import { createClassContext } from "$lib/core/helpers/createClassContext";
import { SvelteMap } from "svelte/reactivity";

const DISCOVER_TIMEOUT_MS = 1000;
const PLACEHOLDER_DATA =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='currentColor' class='size-6 text-secondary'%3E%3Cpath d='M21.721 12.752a9.711 9.711 0 0 0-.945-5.003 12.754 12.754 0 0 1-4.339 2.708 18.991 18.991 0 0 1-.214 4.772 17.165 17.165 0 0 0 5.498-2.477ZM14.634 15.55a17.324 17.324 0 0 0 .332-4.647c-.952.227-1.945.347-2.966.347-1.021 0-2.014-.12-2.966-.347a17.515 17.515 0 0 0 .332 4.647 17.385 17.385 0 0 0 5.268 0ZM9.772 17.119a18.963 18.963 0 0 0 4.456 0A17.182 17.182 0 0 1 12 21.724a17.18 17.18 0 0 1-2.228-4.605ZM7.777 15.23a18.87 18.87 0 0 1-.214-4.774 12.753 12.753 0 0 1-4.34-2.708 9.711 9.711 0 0 0-.944 5.004 17.165 17.165 0 0 0 5.498 2.477ZM21.356 14.752a9.765 9.765 0 0 1-7.478 6.817 18.64 18.64 0 0 0 1.988-4.718 18.627 18.627 0 0 0 5.49-2.098ZM2.644 14.752c1.682.971 3.53 1.688 5.49 2.099a18.64 18.64 0 0 0 1.988 4.718 9.765 9.765 0 0 1-7.478-6.816ZM13.878 2.43a9.755 9.755 0 0 1 6.116 3.986 11.267 11.267 0 0 1-3.746 2.504 18.63 18.63 0 0 0-2.37-6.49ZM12 2.276a17.152 17.152 0 0 1 2.805 7.121c-.897.23-1.837.353-2.805.353-.968 0-1.908-.122-2.805-.353A17.151 17.151 0 0 1 12 2.276ZM10.122 2.43a18.629 18.629 0 0 0-2.37 6.49 11.266 11.266 0 0 1-3.746-2.504 9.754 9.754 0 0 1 6.116-3.985Z' /%3E%3C/svg%3E%0A";

/** We cache generated Favicon URLs to not constantly regenerate them */
class FaviconUrlService {
  #faviconUrls = new SvelteMap<string, string>();
  #queuedHosts = new Set<string>();

  getFavicon(url: string) {
    if (!browser) return PLACEHOLDER_DATA;

    const parsedUrl = new URL(url);
    const faviconUrl = this.#faviconUrls.get(parsedUrl.hostname);
    if (faviconUrl) {
      return faviconUrl;
    }

    if (!this.#queuedHosts.has(parsedUrl.hostname)) {
      this.#queuedHosts.add(parsedUrl.hostname);

      // getFavicon() is called from within a template_effect, so we need to make sure any potentially state
      // modifying functions run after the whole effect has finsihed, otherwise we risk an infinite loop.
      setTimeout(() => {
        this.#discoverFaviconURL(parsedUrl);
      }, 1);
    }

    return PLACEHOLDER_DATA;
  }

  #discoverFaviconURL(url: URL) {
    const possibleFaviconUrls = [
      "/favicon.ico",
      "/favicon.png",
      "/favicon.svg",
      "/favicon.gif",
      "/favicon.jpg",
      "/favicon.jpeg"
    ];

    let currentIdx = 0;
    const img = new Image();

    const cleanUp = () => {
      this.#queuedHosts.delete(url.hostname);
      img.onload = null;
      img.onerror = null;
      clearTimeout(cancelTimeout);
    };

    const cancelCurrentTry = () => {
      img.onerror?.(new ErrorEvent("Request timed out"));
    };

    img.onload = () => {
      this.#faviconUrls.set(url.hostname, img.src);
      cleanUp();
    };

    img.onerror = () => {
      // try next one
      currentIdx += 1;
      if (currentIdx < possibleFaviconUrls.length) {
        img.src = url.origin + possibleFaviconUrls[currentIdx];
        // Reset timeout for next attempt
        clearTimeout(cancelTimeout);
        cancelTimeout = setTimeout(cancelCurrentTry, DISCOVER_TIMEOUT_MS);
      } else {
        cleanUp();
      }
    };

    let cancelTimeout = setTimeout(cancelCurrentTry, DISCOVER_TIMEOUT_MS);
    img.src = url.origin + possibleFaviconUrls[currentIdx];
  }
}

export const [getFaviconUrlService, initFaviconUrlService] = createClassContext(
  "Image url",
  FaviconUrlService
);
