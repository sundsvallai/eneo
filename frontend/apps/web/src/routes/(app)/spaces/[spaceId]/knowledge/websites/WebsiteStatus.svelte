<script lang="ts">
  import type { WebsiteSparse } from "@intric/intric-js";
  import { Label } from "@intric/ui";
  import dayjs from "dayjs";
  import relativeTime from "dayjs/plugin/relativeTime";
  import utc from "dayjs/plugin/utc";
  dayjs.extend(relativeTime);
  dayjs.extend(utc);

  export let website: WebsiteSparse;
  /* TODO colours */
  function statusInfo(): { label: string; color: Label.LabelColor; tooltip?: string } {
    switch (website.latest_crawl?.status) {
      case "complete": {
        const completed = dayjs(website.latest_crawl?.finished_at);
        const label = `Synced ${dayjs().to(completed)}`;
        return {
          color: dayjs().diff(completed, "days") < 10 ? "green" : "yellow",
          label,
          tooltip: `Synced on ${completed.format("YYYY-MM-DD HH:mm")}`
        };
      }
      case "in progress":
        return {
          color: "yellow",
          label: "Sync in progress",
          tooltip: `Started on ${dayjs(website.latest_crawl?.created_at).format("YYYY-MM-DD HH:mm")}`
        };
      case "failed":
        return {
          color: "orange",
          label: "Sync failed"
        };
      case "not found":
        return {
          color: "orange",
          label: "Sync failed"
        };
      case "queued":
        return {
          color: "blue",
          label: "Queued"
        };
    }
    return {
      color: "orange",
      label: "error"
    };
  }
</script>

<Label.Single item={statusInfo()}></Label.Single>
