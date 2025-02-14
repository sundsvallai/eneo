<script lang="ts">
  import { IconAttachment } from "@intric/icons/attachment";

  export let files: { name: string }[];
</script>

{#if files.length > 0}
  <div class="flex w-full flex-wrap items-center justify-end gap-2">
    {#each files as file}
      <div
        class="group flex items-center gap-3.5 rounded-md border border-default py-1.5 pl-1.5 pr-6 hover:bg-hover-dimmer"
      >
        <div
          class="flex min-h-12 min-w-12 items-center justify-center rounded-md bg-accent-default"
        >
          <IconAttachment class="text-on-fill" />
        </div>
        <div>
          <p class="line-clamp-1 group-hover:line-clamp-none">
            {file.name}
          </p>
          <p class="text-sm text-secondary">
            {file.name.split(".")[file.name.split(".").length - 1].toUpperCase()}
          </p>
        </div>
      </div>
    {/each}
  </div>
{/if}
