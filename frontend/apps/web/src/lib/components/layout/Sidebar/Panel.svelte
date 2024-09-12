<script lang="ts">
  import { Button } from "../../../../../../../packages/ui/dist/Button";
  import { getSidebar } from "./ctx";
  export let id: string;
  export let title: string;

  const {
    elements: { content },
    states: { value }
  } = getSidebar();
</script>

<div {...$content(id)} use:content class="panel w-[30vw] min-w-80 bg-white">
  <div class="flex h-full flex-col overflow-y-auto overflow-x-hidden border-l border-stone-300">
    <div
      class="sticky top-0 flex items-center justify-between gap-2 border-b border-stone-300 bg-white/80 pl-4 pr-3 backdrop-blur-md"
    >
      <h2
        class="border-y-[0.25rem] border-transparent border-b-blue-600 px-2.5 pb-[0.9rem] pt-4 font-medium tracking-[0.01rem]"
      >
        {title}
      </h2>
      <Button
        label="Close panel"
        on:click={() => {
          $value = id;
        }}
        padding="icon"
        ><svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="1.5"
          stroke="currentColor"
          class="h-6 w-6"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
        </svg></Button
      >
    </div>
    <div class="flex-grow">
      <slot />
    </div>
  </div>
</div>

<style>
  .panel {
    view-transition-name: sidebar;
  }
</style>
