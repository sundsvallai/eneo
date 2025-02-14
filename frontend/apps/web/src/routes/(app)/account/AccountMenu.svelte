<script lang="ts">
  import { IconAssistant } from "@intric/icons/assistant";
  import { IconKey } from "@intric/icons/key";
  import { page } from "$app/stores";
  import type { ComponentType } from "svelte";
  import { Navigation } from "$lib/components/layout";

  let currentRoute = "";
  $: currentRoute = $page.url.pathname;

  const menuItems: {
    icon: ComponentType;
    label: string;
    url: string;
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

<Navigation.Menu>
  {#each menuItems as item}
    <Navigation.Link
      href={item.url}
      icon={item.icon}
      isActive={currentRoute === item.url}
      label={item.label}
    ></Navigation.Link>
  {/each}
</Navigation.Menu>
