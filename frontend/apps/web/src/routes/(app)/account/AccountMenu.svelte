<script lang="ts">
  import { page } from "$app/stores";
  import IconAssistant from "$lib/components/icons/IconAssistant.svelte";
  import type { ComponentType } from "svelte";
  import IconKey from "$lib/components/icons/IconKey.svelte";

  let currentRoute = "";
  $: currentRoute = $page.url.pathname;

  const menuItems: {
    icon: ComponentType;
    label: string;
    url: string;
    beta?: boolean;
  }[] = [
    {
      icon: IconAssistant,
      label: "My account",
      url: "/account"
    },
    {
      icon: IconKey,
      label: "API keys",
      url: "/account/api-keys"
    }
  ];
</script>

<nav class="layout-menu flex flex-grow flex-col gap-0.5 py-3">
  {#each menuItems as item}
    <a href={item.url} data-current={currentRoute === item.url ? "page" : undefined}>
      <svelte:component this={item.icon}></svelte:component>
      <span class="hidden md:block">{item.label}</span>
      {#if item.beta}
        <span
          class="hidden rounded-md border border-purple-600 px-1 py-0.5 text-xs font-normal text-purple-600 md:block"
          >Beta</span
        >
      {/if}
    </a>
  {/each}
</nav>
