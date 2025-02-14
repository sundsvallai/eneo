<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { IconAssistant } from "@intric/icons/assistant";
  import { IconAssistants } from "@intric/icons/assistants";
  import { IconThumb } from "@intric/icons/thumb";
  import { IconLibrary } from "@intric/icons/library";
  import { IconCPU } from "@intric/icons/CPU";
  import { IconBulb } from "@intric/icons/bulb";
  import { page } from "$app/stores";
  import type { ComponentType } from "svelte";
  import { getAppContext } from "$lib/core/AppContext";
  import { Navigation } from "$lib/components/layout";
  import { IconStorage } from "@intric/icons/storage";

  let currentRoute = "";
  $: currentRoute = $page.url.pathname;

  const { featureFlags } = getAppContext();

  const userPages = featureFlags.newAuth
    ? [
        {
          icon: IconAssistant,
          label: "Users",
          url: "/admin/users"
        }
      ]
    : [
        {
          icon: IconAssistant,
          label: "Users",
          url: "/admin/legacy/users"
        },
        {
          icon: IconAssistants,
          label: "User groups",
          url: "/admin/legacy/user-groups"
        },
        {
          icon: IconThumb,
          label: "Roles",
          url: "/admin/legacy/roles"
        }
      ];

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
      icon: IconBulb,
      label: "Insights",
      url: "/admin/insights",
      beta: true
    },
    ...userPages,
    {
      icon: IconStorage,
      label: "Storage",
      url: "/admin/storage"
    }
  ];

  function isSelected(url: string, currentRoute: string) {
    url = url.replaceAll("/admin", "");
    currentRoute = currentRoute.replaceAll("/admin", "");
    if (url === "") return currentRoute === "";
    return currentRoute.startsWith(url);
  }
</script>

<Navigation.Menu>
  {#each menuItems as item}
    <Navigation.Link
      href={item.url}
      isActive={isSelected(item.url, currentRoute)}
      icon={item.icon}
      label={item.label}
    >
      {#if item.beta}
        <span
          class="hidden rounded-md border border-[var(--beta-indicator)] px-1 py-0.5 text-xs font-normal !tracking-normal text-[var(--beta-indicator)] md:block"
          >Beta</span
        >
      {/if}
    </Navigation.Link>
  {/each}
</Navigation.Menu>
