<script lang="ts">
  import { page } from "$app/stores";
  import { IconFeedback } from "@intric/icons/feedback";

  let cls: string = "";
  export { cls as class };
</script>

<nav class="{cls} flex flex-grow flex-col gap-0.5 py-3">
  <slot />
  {#if $page.data.feedbackFormUrl}
    <div class="flex-grow justify-end"></div>
    <a
      href={$page.data.feedbackFormUrl}
      target="_blank"
      rel="noreferrer"
      class="relative flex items-center justify-center gap-3 px-[1.45rem] py-2.5 tracking-[0.008rem] text-muted hover:bg-hover-default hover:font-medium hover:tracking-normal hover:text-primary"
    >
      <span>Send Feedback</span>
      <IconFeedback />
    </a>
  {/if}
</nav>
