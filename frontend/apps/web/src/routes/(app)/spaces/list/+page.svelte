<!-- MIT License -->

<script lang="ts">
  import { Page } from "$lib/components/layout";
  import CreateSpaceDialog from "$lib/features/spaces/components/CreateSpaceDialog.svelte";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import SpacesTable from "./SpacesTable.svelte";

  const {
    state: { accessibleSpaces }
  } = getSpacesManager();
</script>

<Page.Root>
  <Page.Header>
    <Page.Title>Your spaces</Page.Title>
    <CreateSpaceDialog includeTrigger={true} forwardToNewSpace={false}></CreateSpaceDialog>
  </Page.Header>

  <Page.Main>
    <SpacesTable spaces={accessibleSpaces}></SpacesTable>
  </Page.Main>
</Page.Root>
