<script lang="ts">
  import { IconArrowUpToLine } from "@intric/icons/arrow-up-to-line";
  import { Button } from "@intric/ui";
  import { page } from "$app/stores";
  import { getAppContext, initAppContext } from "$lib/core/AppContext";
  import JobManagerDropdown from "$lib/features/jobs/components/JobManagerDropdownButton.svelte";
  import { initJobManager } from "$lib/features/jobs/JobManager";
  import ProfileMenu from "./ProfileMenu.svelte";
  import { initIntric } from "$lib/core/Intric";
  import { initIntricSocket } from "$lib/core/IntricSocket";
  import { PageLoadBar } from "$lib/components/layout";
  import { browser } from "$app/environment";
  import { onDestroy } from "svelte";
  import IntricWordMark from "$lib/assets/IntricWordMark.svelte";
  import { IconIntric } from "@intric/icons/intric";

  export let data;

  initIntric(data);
  initAppContext(data);
  initJobManager(data);
  const socket = initIntricSocket(data);

  // Open the socket connection
  // While it would be more intuitive to use onMount to open the socket, onMounts are executed form the bottom up
  // e.g. will run in child components first. This would mean the socket is not yet open when trying to subscribe in a child.
  if (browser) socket.connect();
  onDestroy(() => {
    // Socket needs to be disconnected so it can be garbage collected during HMR
    socket.disconnect();
  });

  const {
    user,
    state: { showHeader }
  } = getAppContext();

  $: contentLink = $page.url.pathname + "#content";
  $: currentRoute = $page.url.pathname;
</script>

<a
  href={contentLink}
  class="absolute left-1 top-1 z-50 h-0 w-0 overflow-hidden rounded-lg bg-primary font-medium text-accent-stronger shadow-lg focus:block focus:h-auto focus:w-auto"
  ><span class="block p-2">Jump to content</span></a
>

<PageLoadBar color="var(--accent-default)" displayThresholdMs={200} />

<div
  class="fixed inset-0 z-[100] h-3"
  on:pointerenter={() => {
    $showHeader = true;
  }}
></div>

<div class="fixed inset-x-0 h-[8.275rem] bg-tertiary transition-all duration-700 ease-in-out"></div>

<div
  class="mx-auto flex min-h-[100svh] w-full max-w-[2000px] flex-col bg-secondary p-0 md:px-4 md:pt-3"
>
  <header
    class:max-h-0={!$showHeader}
    class:max-h-14={$showHeader}
    class="z-10 box-border flex items-start overflow-clip rounded-t-sm border-stronger bg-secondary transition-all duration-500 ease-in-out"
  >
    <div
      class="group flex h-[3.25rem] min-w-[3.85rem] items-center justify-between border-r-[0.5px] border-default pl-6 pr-3 hover:bg-accent-dimmer md:w-[17rem] md:min-w-[17rem]"
    >
      <a href="/">
        <IntricWordMark class="hidden h-[3rem] w-[3.5rem] text-brand-intric md:block"
        ></IntricWordMark>
        <IconIntric class="-ml-0.5 block text-brand-intric md:hidden"></IconIntric>
      </a>
      <Button
        unstyled
        class="hidden h-9 w-9 items-center justify-center rounded-lg text-lg text-accent-stronger hover:bg-hover-default md:group-hover:flex"
        on:click={() => {
          $showHeader = false;
        }}
      >
        <IconArrowUpToLine />
      </Button>
    </div>
    <nav class="flex h-[3.25rem] w-full overflow-x-auto">
      <a
        href="/spaces/personal/chat"
        data-current={currentRoute.startsWith("/spaces/personal") ? "page" : undefined}>Personal</a
      >
      <a
        href="/spaces/list"
        data-current={currentRoute.startsWith("/spaces") &&
        !currentRoute.startsWith("/spaces/personal")
          ? "page"
          : undefined}>Spaces</a
      >

      <div aria-hidden="true" class="flex-grow"></div>

      <!-- Toggle -->
      {#if user.hasPermission("admin")}
        <a href="/admin" data-current={currentRoute.startsWith("/admin") ? "page" : undefined}
          >Admin</a
        >
      {/if}

      <JobManagerDropdown></JobManagerDropdown>
      <div class="subtle-border h-[3.25rem] w-[0.5px]"></div>
      <ProfileMenu></ProfileMenu>
    </nav>
  </header>

  <main class="border-box relative z-10 flex-grow overflow-clip bg-primary transition-all">
    <slot />
  </main>
</div>

<style lang="postcss">
  nav a {
    @apply flex h-[3.25rem] items-center px-8 pt-0.5 text-[0.9rem] tracking-[0.01rem] text-secondary hover:bg-accent-dimmer hover:font-medium hover:tracking-normal hover:text-brand-intric;
  }

  nav a[data-current="page"] {
    @apply font-medium tracking-normal text-brand-intric;
    background: rgba(from var(--background-hover-default) r g b / 0.1);
  }

  main {
    border: 0.5px solid var(--border-stronger);
    border-top: 0px;
    border-bottom: 0px;
    box-shadow:
      0px 18px 12px 2px rgba(0, 0, 0, 0.12),
      0px 0px 14px 2px rgba(0, 0, 0, 0.09);
  }

  header {
    box-shadow: 0px 14px 12px 2px rgba(0, 0, 0, 0.1);
    border: 0.5px solid var(--border-stronger);
    border-bottom: 0px;
  }

  .subtle-border {
    background: linear-gradient(0deg, var(--border-default) 0%, transparent 100%);
  }
</style>
