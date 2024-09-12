<script lang="ts">
  import IconSession from "$lib/components/icons/IconSession.svelte";
  import type { AssistantSession } from "@intric/intric-js";
  import { Button } from "@intric/ui";

  export let session: Omit<AssistantSession, "messages">;
  export let selectSession: (session: Omit<AssistantSession, "messages">) => void;
</script>

<Button
  padding="icon-leading"
  on:click={() => {
    selectSession(session);
  }}
  class="max-w-full"
>
  <IconSession class="min-w-6 text-stone-300 group-hover:text-stone-600"></IconSession>
  <span class="w-full truncate overflow-ellipsis">
    {session.name}
  </span>
</Button>
