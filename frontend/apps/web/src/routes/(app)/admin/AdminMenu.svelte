<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { page } from "$app/stores";
  import IconAssistants from "$lib/components/icons/IconAssistants.svelte";
  import IconAssistant from "$lib/components/icons/IconAssistant.svelte";
  import IconLibrary from "$lib/components/icons/IconLibrary.svelte";
  import type { ComponentType } from "svelte";
  import IconThumb from "$lib/components/icons/IconThumb.svelte";
  import IconCPU from "$lib/components/icons/IconCPU.svelte";
  import Bulb from "$lib/components/icons/Bulb.svelte";

  let currentRoute = "";
  $: currentRoute = $page.url.pathname;

  const menuItems: {
    icon: ComponentType;
    label: string;
    url: string;
    beta?: boolean;
  }[] = [
    {
      icon: IconLibrary,
      label: "Organisation",
      url: "/admin"
    },
    {
      icon: IconCPU,
      label: "Models",
      url: "/admin/models"
    },
    {
      icon: Bulb,
      label: "Insights",
      url: "/admin/insights",
      beta: true
    },
    {
      icon: IconAssistant,
      label: "Users",
      url: "/admin/users"
    },
    {
      icon: IconAssistants,
      label: "User groups",
      url: "/admin/user-groups"
    },
    {
      icon: IconThumb,
      label: "Roles",
      url: "/admin/roles"
    }
  ];

  function isSelected(url: string, currentRoute: string) {
    url = url.replaceAll("/admin", "");
    currentRoute = currentRoute.replaceAll("/admin", "");
    if (url === "") return currentRoute === "";
    return currentRoute.startsWith(url);
  }
</script>

<nav class="layout-menu flex flex-grow flex-col gap-0.5 py-3">
  {#each menuItems as item}
    <a href={item.url} data-current={isSelected(item.url, currentRoute) ? "page" : undefined}>
      <svelte:component this={item.icon}></svelte:component>
      <span class="hidden md:block">{item.label}</span>
      {#if item.beta}
        <span
          class="hidden rounded-md border border-purple-600 px-1 py-0.5 text-xs font-normal !tracking-normal text-purple-600 md:block"
          >Beta</span
        >
      {/if}
    </a>
  {/each}
</nav>
