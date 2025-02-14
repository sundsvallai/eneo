<script lang="ts">
  import type { InfoBlob } from "@intric/intric-js";
  import { Markdown } from "@intric/ui";
  import MessageIntricInfoBlob from "./MessageIntricInfoBlob.svelte";

  export let contents: string;
  export let references: InfoBlob[];
</script>

<div class="prose relative text-lg">
  <span class="sr-only">Answer:</span>
  <Markdown
    source={contents}
    customRenderers={{
      inref: {
        references,
        component: MessageIntricInfoBlob
      }
    }}
  />
</div>
