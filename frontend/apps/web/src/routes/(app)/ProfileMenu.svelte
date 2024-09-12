<script>
  import { Button } from "@intric/ui";
  import { createDropdownMenu } from "@melt-ui/svelte";
  import { fly, fade } from "svelte/transition";
  import IconAssistant from "../../lib/components/icons/IconAssistant.svelte";
  import IconKey from "../../lib/components/icons/IconKey.svelte";

  const {
    elements: { menu, item, trigger, overlay, arrow },
    states: { open }
  } = createDropdownMenu({
    positioning: {
      fitViewport: true,
      flip: true,
      placement: "bottom",
      overflowPadding: 16
    },
    forceVisible: true,
    loop: true,
    preventScroll: false,
    arrowSize: 12
  });
</script>

<Button
  is={[$trigger]}
  unstyled
  label="Account and settings"
  class="relative flex h-[3.25rem] !min-w-[3.5rem] items-center justify-center  text-black/60 hover:bg-blue-100 hover:text-blue-700"
>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
    stroke-width="1.4"
    stroke="currentColor"
    class="h-7 w-7 min-w-7"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
    />
  </svg>
</Button>
{#if $open}
  <div
    {...$overlay}
    use:overlay
    class="fixed inset-0 z-[40] bg-black/15"
    transition:fade={{ duration: 200 }}
  />
  <div
    {...$menu}
    use:menu
    in:fly={{ y: -15, duration: 100 }}
    out:fly={{ y: -5, duration: 200 }}
    class="items absolute z-[50] flex min-w-[15rem] -translate-y-[0.75rem] flex-col rounded-sm border-b border-black/40 bg-white p-3 shadow-md"
  >
    <p
      class="border-b border-black/10 px-6 pb-2.5 pt-1 font-mono text-[0.85rem] font-medium tracking-[0.015rem] text-black/85"
    >
      Settings
    </p>
    <Button
      unstyled
      is={[$item]}
      href="/account"
      padding="icon-leading"
      class="group relative flex h-[3.5rem] w-full items-center justify-start gap-3 border-b border-black/10 pl-5 pr-4 last-of-type:border-b-0 hover:bg-blue-100 hover:text-blue-800"
    >
      <IconAssistant></IconAssistant>
      My account</Button
    ><Button
      is={[$item]}
      unstyled
      href="/account/api-keys"
      padding="icon-leading"
      class="group relative flex h-[3.5rem] w-full items-center justify-start gap-3 border-b border-black/10 pl-5 pr-4 last-of-type:border-b-0 hover:bg-blue-100 hover:text-blue-800"
    >
      <IconKey></IconKey>
      My API keys</Button
    >
    <Button
      unstyled
      destructive
      is={[$item]}
      href="/logout"
      class="mt-3 flex !justify-center gap-2 rounded-lg border border-black/10  bg-white  !py-2  focus:outline-offset-4 focus:ring-offset-4"
      ><svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="mx-0.5 h-6 w-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9"
        />
      </svg>Logout</Button
    >

    <div {...$arrow} use:arrow class="!z-10 border-black/35" />
  </div>
{/if}

<style>
  .items {
    box-shadow:
      0px 10px 20px -10px rgba(0, 0, 0, 0.5),
      0px 30px 50px 0px rgba(0, 0, 0, 0.2);
  }
</style>
