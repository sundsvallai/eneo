<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { page } from "$app/stores";
  import Cog from "$lib/components/icons/Cog.svelte";
  import IconAssistants from "$lib/components/icons/IconAssistants.svelte";
  import IconKnowledge from "$lib/components/icons/IconKnowledge.svelte";
  import IconServices from "$lib/components/icons/IconServices.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";

  const {
    state: { currentSpace }
  } = getSpacesManager();

  $: section = $page.url.pathname.split("/")[3] ?? "overview";
</script>

<nav class="layout-menu flex flex-grow flex-col gap-0.5 py-3">
  <a
    href="/spaces/{$currentSpace.routeId}"
    data-current={section === "overview" ? "page" : undefined}
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke-width="1.5"
      stroke="currentColor"
      class="size-6"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M7.5 3.75H6A2.25 2.25 0 0 0 3.75 6v1.5M16.5 3.75H18A2.25 2.25 0 0 1 20.25 6v1.5m0 9V18A2.25 2.25 0 0 1 18 20.25h-1.5m-9 0H6A2.25 2.25 0 0 1 3.75 18v-1.5M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
      />
    </svg>

    <span>Overview</span>
  </a>
  {#if $currentSpace.hasPermission("read", "assistant")}
    <a
      href="/spaces/{$currentSpace.routeId}/assistants"
      data-current={section === "assistants" ? "page" : undefined}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke-width="1.5"
        stroke="currentColor"
        class="size-6"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155"
        />
      </svg>

      <span>Assistants</span>
    </a>
  {/if}
  {#if $currentSpace.hasPermission("read", "service")}
    <a
      href="/spaces/{$currentSpace.routeId}/services"
      data-current={section === "services" ? "page" : undefined}
    >
      <IconServices></IconServices>

      <span>Services</span>
    </a>
  {/if}
  {#if $currentSpace.hasPermission("read", "website") || $currentSpace.hasPermission("read", "collection")}
    <a
      href="/spaces/{$currentSpace.routeId}/knowledge"
      data-current={section === "knowledge" ? "page" : undefined}
    >
      <IconKnowledge class="stroke-2"></IconKnowledge>
      <span>Knowledge</span>
    </a>
  {/if}
  {#if $currentSpace.hasPermission("read", "member")}
    <div class="my-2 border-b-[0.5px] border-black/15"></div>
    <!-- <div class="flex-grow"></div> -->
    <a
      href="/spaces/{$currentSpace.routeId}/members"
      data-current={section === "members" ? "page" : undefined}
    >
      <IconAssistants></IconAssistants>
      <span>Members</span>
    </a>
  {/if}
  {#if $currentSpace.hasPermission("edit", "space")}
    <a
      href="/spaces/{$currentSpace.routeId}/settings"
      data-current={section === "settings" ? "page" : undefined}
    >
      <Cog></Cog>
      <span>Settings</span>
    </a>
  {/if}
</nav>
