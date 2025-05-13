<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import MemberChip from "./MemberChip.svelte";

  export let members: { id: string; email: string; role: string }[] = [];
</script>

{#if members.length > 0}
  <div class="flex">
    {#each members.slice(0, 3) as member (member.id)}
      <MemberChip {member}></MemberChip>
    {/each}
    {#if members.length > 3}
      <div class="ml-2 flex items-center justify-center">
        +{members.length - 3} more
      </div>
    {/if}
  </div>
{/if}
