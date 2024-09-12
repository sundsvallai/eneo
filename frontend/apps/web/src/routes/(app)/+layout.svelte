<script lang="ts">
  import { page } from "$app/stores";
  import IconIntric from "$lib/components/icons/IconIntric.svelte";
  import IntricLogo from "$lib/components/icons/IntricLogo.svelte";
  import { getAppContext, initAppContext } from "$lib/core/AppContext";
  import JobManagerDropdown from "$lib/features/jobs/components/JobManagerDropdownButton.svelte";
  import { initJobManager } from "$lib/features/jobs/JobManager";
  import { Button } from "@intric/ui";
  import ProfileMenu from "./ProfileMenu.svelte";
  import { ProgressBar } from "@prgm/sveltekit-progress-bar";
  import { initIntric } from "$lib/core/Intric";

  export let data;

  initIntric(data);
  initAppContext(data);
  // Requires initIntric() to be called before
  initJobManager();

  const { user, showHeader } = getAppContext();

  $: contentLink = $page.url.pathname + "#content";
  $: currentRoute = $page.url.pathname;
</script>

<a
  href={contentLink}
  class="absolute left-1 top-1 z-50 h-0 w-0 overflow-hidden rounded-lg bg-white font-medium text-blue-700 shadow-lg focus:block focus:h-auto focus:w-auto"
  ><span class="block p-2">Jump to content</span></a
>

<ProgressBar color="#3662e3" displayThresholdMs={200} />

<div
  class="fixed inset-0 z-[100] h-3"
  on:pointerenter={() => {
    $showHeader = true;
  }}
></div>

<div class="mx-auto flex min-h-[100svh] w-full max-w-[2000px] flex-col p-0 md:px-4 md:pt-3">
  <header
    class:max-h-0={!$showHeader}
    class:max-h-14={$showHeader}
    class="box-border flex items-start overflow-clip rounded-t-sm border-black/30 bg-[#f2efeb] transition-all duration-500 ease-in-out"
  >
    <div
      class="group flex h-[3.25rem] min-w-[3.85rem] items-center justify-between border-r-[0.5px] border-black/10 pl-6 pr-3 hover:bg-blue-100 md:w-[17rem] md:min-w-[17rem]"
    >
      <a href="/"
        ><IntricLogo class="hidden h-[3rem] w-[3.5rem] text-blue-700 md:block"></IntricLogo>
        <IconIntric class="ml-0.5 block text-blue-700 md:hidden"></IconIntric>
      </a>
      <Button
        unstyled
        class="hidden h-9 w-9 items-center justify-center rounded-lg text-lg  text-blue-700 hover:bg-blue-700/10 md:group-hover:flex"
        on:click={() => {
          $showHeader = false;
        }}
        ><svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.7"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="te h-5 w-5"
          ><path d="M5 3h14" /><path d="m18 13-6-6-6 6" /><path d="M12 7v14" /></svg
        ></Button
      >
    </div>
    <nav class="flex h-[3.25rem] w-full overflow-x-auto">
      <a
        href="/spaces/personal"
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
      {#if user.hasPermission("admin")}
        <a href="/admin" data-current={currentRoute.startsWith("/admin") ? "page" : undefined}
          >Admin</a
        >
      {/if}

      <JobManagerDropdown></JobManagerDropdown>
      <div class="h-[3.25rem] w-[0.5px] bg-gradient-to-b from-black/0 to-black/15"></div>
      <ProfileMenu></ProfileMenu>
    </nav>
  </header>

  <main class="border-box relative z-10 flex-grow overflow-clip bg-white transition-all">
    <slot />
  </main>
</div>

<style lang="postcss">
  nav a {
    @apply flex h-[3.25rem] items-center px-8 pt-0.5 text-[0.9rem] tracking-[0.01rem] text-black/60 hover:bg-blue-100 hover:font-medium hover:tracking-normal hover:text-blue-800;
  }

  nav a[data-current="page"] {
    @apply bg-[#00000009] font-medium tracking-normal text-blue-700;
  }

  main {
    border: 0.5px solid rgba(54, 54, 54, 0.4);
    border-top: 0px;
    border-bottom: 0px;
    box-shadow:
      0px 18px 4px 2px rgba(0, 0, 0, 0.1),
      0px 0px 10px 2px rgba(0, 0, 0, 0.05);
  }

  header {
    box-shadow: 0px 14px 4px 2px rgba(0, 0, 0, 0.1);
    border: 0.5px solid rgba(54, 54, 54, 0.4);
    border-top: 0.5px solid rgba(54, 54, 54, 0.3);
    border-bottom: 0px;
  }
</style>
