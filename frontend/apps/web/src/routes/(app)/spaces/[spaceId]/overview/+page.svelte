<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import MembersList from "../members/MembersList.svelte";
  import { getAppContext } from "$lib/core/AppContext";
  import { Page } from "$lib/components/layout";

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const {
    state: { userInfo }
  } = getAppContext();
</script>

<svelte:head>
  <title>Intric.ai – {$currentSpace.personal ? "Personal" : $currentSpace.name} – Overview</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Overview"></Page.Title>
    <MembersList></MembersList>
  </Page.Header>

  <Page.Main>
    <div class="flex flex-grow flex-col overflow-y-auto pl-2 pr-4 pt-4">
      <div class="flex items-center justify-start gap-4 pb-4">
        <h1 class="text-[2rem] font-extrabold text-primary">
          {$currentSpace.personal ? `Hi, ${$userInfo.firstName}!` : $currentSpace.name}
        </h1>
      </div>
      {#if $currentSpace.personal}
        <p class="min-h-20 max-w-[70ch] text-primary">
          You can build and experiment with your own AI applications in your personal space.
        </p>
      {:else}
        <p class="min-h-20">{$currentSpace.description ?? `Welcome to ${$currentSpace.name}`}</p>
      {/if}
      <!-- <div class="flex-grow"></div> -->

      <div class="grid gap-4 pb-4 pt-4 md:grid-cols-3">
        {#if $currentSpace.hasPermission("read", "assistant")}
          <a href="/spaces/{$currentSpace.routeId}/assistants" class="tile">
            <h3 class="font-mono text-sm uppercase text-primary">Assistants</h3>
            <div class="flex-grow"></div>
            <div class="self-end text-[4rem] font-bold text-primary">
              {$currentSpace.applications.assistants.length}
            </div>
          </a>
        {/if}
        {#if $currentSpace.hasPermission("read", "app")}
          <a href="/spaces/{$currentSpace.routeId}/apps" class="tile">
            <h3 class="font-mono text-sm uppercase text-primary">Apps</h3>
            <div class="flex-grow"></div>
            <div class="self-end text-[4rem] font-bold text-primary">
              {$currentSpace.applications.apps.length}
            </div>
          </a>
        {/if}
        {#if $currentSpace.hasPermission("read", "service")}
          <a href="/spaces/{$currentSpace.routeId}/services" class="tile">
            <h3 class="font-mono text-sm uppercase text-primary">Services</h3>
            <div class="flex-grow"></div>
            <div class="self-end text-[4rem] font-bold text-primary">
              {$currentSpace.applications.services.length}
            </div>
          </a>
        {/if}
        {#if $currentSpace.hasPermission("read", "collection")}
          <a href="/spaces/{$currentSpace.routeId}/knowledge?tab=collections" class="tile">
            <h3 class="font-mono text-sm uppercase text-primary">Collections</h3>
            <div class="flex-grow"></div>

            <div class="self-end text-[4rem] font-bold text-primary">
              {$currentSpace.knowledge.groups.length}
            </div>
          </a>
        {/if}
        {#if $currentSpace.hasPermission("read", "website")}
          <a href="/spaces/{$currentSpace.routeId}/knowledge?tab=websites" class="tile">
            <h3 class="font-mono text-sm uppercase text-primary">Websites</h3>
            <div class="flex-grow"></div>

            <div class="self-end text-[4rem] font-bold text-primary">
              {$currentSpace.knowledge.websites.length}
            </div>
          </a>
        {/if}
        {#if $currentSpace.hasPermission("read", "member")}
          <a href="/spaces/{$currentSpace.routeId}/members" class="tile">
            <h3 class="font-mono text-sm uppercase text-primary">Members</h3>
            <div class="flex-grow"></div>

            <div class="self-end text-[4rem] font-bold text-primary">
              {$currentSpace.members.length}
            </div>
          </a>
        {/if}
      </div>
    </div>
  </Page.Main>
</Page.Root>

<style lang="postcss">
  .tile {
    @apply flex min-h-64 cursor-pointer flex-col border-t border-default bg-hover-dimmer px-4 py-2 hover:bg-hover-default;
  }
</style>
