<script lang="ts">
  import type { WebsiteSparse } from "@intric/intric-js";
  import { Label } from "@intric/ui";

  export let updateInterval: WebsiteSparse["update_interval"];

  const intervalInfo: Record<string, { label: string; color: Label.LabelColor; tooltip?: string }> =
    {
      weekly: {
        color: "green",
        label: "Weekly"
      },
      never: {
        color: "gray",
        label: "Never"
      },
      error: {
        color: "orange",
        label: "Not found"
      }
    };
</script>

<Label.Single item={intervalInfo[updateInterval ?? "error"]}></Label.Single>
