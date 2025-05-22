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
  import { Navigation } from "$lib/components/layout";
  import { IconUsage } from "@intric/icons/usage";
  import { IconKey } from "@intric/icons/key";
  let currentRoute = "";
  $: currentRoute = $page.url.pathname;

  function isSelected(url: string, currentRoute: string) {
    url = url.replaceAll("/admin", "");
    currentRoute = currentRoute.replaceAll("/admin", "");
    if (url === "") return currentRoute === "";
    return currentRoute.startsWith(url);
  }
</script>

<Navigation.Menu>
  <Navigation.Link
    href="/admin"
    isActive={isSelected("/admin", currentRoute)}
    icon={IconLibrary}
    label="Organisation"
  />

  <div class="border-default my-2 border-b-[0.5px]"></div>
  <Navigation.Link
    href="/admin/models"
    isActive={isSelected("/admin/models", currentRoute)}
    icon={IconCPU}
    label="Models"
  />
  <Navigation.Link
    href="/admin/security-classifications"
    isActive={isSelected("/admin/security-classifications", currentRoute)}
    icon={IconKey}
    label="Security"
  />
  <div class="border-default my-2 border-b-[0.5px]"></div>
  <Navigation.Link
    href="/admin/usage"
    isActive={isSelected("/admin/usage", currentRoute)}
    icon={IconUsage}
    label="Usage"
  />
  <Navigation.Link
    href="/admin/insights"
    isActive={isSelected("/admin/insights", currentRoute)}
    icon={IconBulb}
    label="Insights"
  >
    <span
      class="hidden rounded-md border border-[var(--beta-indicator)] px-1 py-0.5 text-xs font-normal !tracking-normal text-[var(--beta-indicator)] md:block"
      >Beta</span
    >
  </Navigation.Link>
  <div class="border-default my-2 border-b-[0.5px]"></div>
  <Navigation.Link
    href="/admin/legacy/users"
    isActive={isSelected("/admin/legacy/users", currentRoute)}
    icon={IconAssistant}
    label="Users"
  />
  <Navigation.Link
    href="/admin/legacy/user-groups"
    isActive={isSelected("/admin/legacy/user-groups", currentRoute)}
    icon={IconAssistants}
    label="User groups"
  />
  <Navigation.Link
    href="/admin/legacy/roles"
    isActive={isSelected("/admin/legacy/roles", currentRoute)}
    icon={IconThumb}
    label="Roles"
  />
</Navigation.Menu>
