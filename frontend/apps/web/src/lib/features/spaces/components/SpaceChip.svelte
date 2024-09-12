<!-- MIT License -->
<script lang="ts">
  import { getAppContext } from "$lib/core/AppContext";
  import { getColourClass } from "$lib/core/colours";

  export let space: {
    id: string;
    name: string;
    personal: boolean;
  };

  const { user } = getAppContext();
</script>

{#if space.personal}
  <div class="{getColourClass(user.id)} star">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="0"
      stroke="currentColor"
      class="size-5"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        fill="currentColor"
        d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z"
      />
    </svg>
  </div>
{:else}
  <div class="{getColourClass(space.id)} chip capitalize">
    {space.name.slice(0, 1)}
  </div>
{/if}

<style lang="postcss">
  .chip {
    @apply flex min-h-[1.6rem] min-w-[1.6rem]  items-center justify-center rounded-md bg-[var(--space-color)] text-white/80;
  }
  .star {
    @apply flex min-h-[1.6rem] min-w-[1.6rem]  items-center justify-center rounded-md bg-[var(--space-color-light)] text-[var(--space-color)];
  }
  .blue {
    --space-color: #1e2466;
    --space-color-light: #1e246622;
  }
  .green {
    --space-color: #173026;
    --space-color-light: #17302622;
  }
  .purple {
    --space-color: #5e2dbf;
    --space-color-light: #5e2dbf22;
  }
  .gold {
    --space-color: #5c5b32;
    --space-color-light: #5c5b3222;
  }
  .lightblue {
    --space-color: #104dd0;
    --space-color-light: #104dd022;
  }
</style>
