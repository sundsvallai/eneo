<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import type { SpaceSparse } from "@intric/intric-js";
  import { Button, Dropdown } from "@intric/ui";
  import IconEdit from "$lib/components/icons/IconEdit.svelte";
  import IconEllipsis from "$lib/components/icons/IconEllipsis.svelte";

  export let space: SpaceSparse;
</script>

<Dropdown.Root>
  <Dropdown.Trigger let:trigger asFragment>
    <Button is={trigger} disabled={false} padding="icon">
      <IconEllipsis></IconEllipsis>
    </Button>
  </Dropdown.Trigger>
  <Dropdown.Menu let:item>
    <Button is={item} href="/spaces/{space.id}/settings" padding="icon-leading">
      <IconEdit size="small"></IconEdit>
      Edit</Button
    >
  </Dropdown.Menu>
</Dropdown.Root>
