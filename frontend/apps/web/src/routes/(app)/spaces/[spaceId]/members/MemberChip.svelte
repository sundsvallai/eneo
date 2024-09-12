<!-- MIT License -->

<script lang="ts">
  import { getColourClass } from "$lib/core/colours";
  import { Tooltip } from "@intric/ui";

  export let member:
    | {
        id: string;
        username: string;
      }
    | {
        label: string;
      };
</script>

{#if "username" in member}
  <Tooltip text={member.username} placement="top">
    <div class="{getColourClass(member.id)} chip capitalize">
      {member.username.slice(0, 1)}
    </div>
  </Tooltip>
{:else}
  <div class="white chip">{member.label}</div>
{/if}

<style lang="postcss">
  .chip {
    @apply -ml-2 flex h-9 w-9 items-center justify-center rounded-full border-2 border-white shadow hover:z-30 hover:shadow-lg;
  }
  .blue {
    @apply bg-[#1e2466] text-white/80;
  }
  .green {
    @apply bg-[#173026] text-white/80;
  }
  .purple {
    @apply bg-[#5e2dbf] text-white/80;
  }
  .gold {
    @apply bg-[#5c5b32] text-white/80;
  }
  .lightblue {
    @apply bg-[#104dd0] text-white/80;
  }
  .white {
    @apply bg-stone-800 text-center text-sm text-white;
  }
</style>
