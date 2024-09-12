<script lang="ts">
  import type { CrawlRun } from "@intric/intric-js";
  import { Label } from "@intric/ui";

  export let crawl: CrawlRun;
  export let align: "start" | "end" | "center" = "start";

  let cls = "";
  export { cls as class };

  const successPages = (crawl.pages_crawled ?? 0) - (crawl.pages_failed ?? 0);
  const successFiles = (crawl.files_downloaded ?? 0) - (crawl.files_failed ?? 0);

  function totalLabel(): { label: string; color: Label.LabelColor } {
    let label = `Crawled ${crawl.pages_crawled} pages`;
    if (crawl.files_downloaded ?? 0 > 0) {
      label += ` and ${crawl.files_downloaded} files`;
    }
    return {
      color: "blue",
      label
    };
  }

  function failedLabel(): { label: string; color: Label.LabelColor } {
    let label = "";
    if (crawl.pages_failed) {
      label += ` ${crawl.pages_failed} pages`;
    }
    if (crawl.files_failed && crawl.pages_failed) {
      label += ` and `;
    }
    if (crawl.files_failed) {
      label += `${crawl.files_failed} files`;
    }
    label += " failed";
    return {
      color: "orange",
      label
    };
  }

  function successLabel(): { label: string; color: Label.LabelColor } {
    let label = "";
    if (successPages > 0) {
      label += ` ${successPages} pages`;
    }
    if (successPages && successFiles) {
      label += ` and `;
    }
    if (successFiles) {
      label += `${crawl.files_downloaded} files`;
    }
    label += " succeeded";
    return {
      color: "green",
      label
    };
  }

  function crawlStatus(): { label: string; color: Label.LabelColor } {
    if (crawl.status === "failed") {
      return {
        color: "orange",
        label: "Crawl failed"
      };
    } else {
      return {
        color: "blue",
        label: "Crawl still running..."
      };
    }
  }
</script>

<div class="flex w-full items-center gap-2 {cls}" style="justify-content: flex-{align}">
  {#if crawl.status === "complete"}
    <Label.Single capitalize={false} item={totalLabel()}></Label.Single>
    {#if successPages || successFiles}
      <Label.Single capitalize={false} item={successLabel()}></Label.Single>
    {/if}
    {#if crawl.pages_failed || crawl.files_failed}
      <Label.Single capitalize={false} item={failedLabel()}></Label.Single>
    {/if}
  {:else}
    <Label.Single capitalize={false} item={crawlStatus()}></Label.Single>
  {/if}
</div>
