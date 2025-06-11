<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { Page } from "$lib/components/layout/index.js";
  import { setSecurityContext } from "$lib/features/security-classifications/SecurityContext.js";
  import CompletionModelsTable from "./CompletionModelsTable.svelte";
  import EmbeddingModelsTable from "./EmbeddingModelsTable.svelte";
  import TranscriptionModelsTable from "./TranscriptionModelsTable.svelte";

  export let data;

  setSecurityContext(data.securityClassifications);
</script>

<svelte:head>
  <title>Eneo.ai – Admin – Models</title>
</svelte:head>

<Page.Root>
  <Page.Header>
    <Page.Title title="Models"></Page.Title>
    <Page.Tabbar>
      <Page.TabTrigger tab="completion_models">Completion models</Page.TabTrigger>
      <Page.TabTrigger tab="embedding_models">Embedding models</Page.TabTrigger>
      <Page.TabTrigger tab="transcription_models">Transcription models</Page.TabTrigger>
    </Page.Tabbar>
  </Page.Header>
  <Page.Main>
    <Page.Tab id="completion_models">
      <CompletionModelsTable completionModels={data.models.completionModels} />
    </Page.Tab>
    <Page.Tab id="embedding_models">
      <EmbeddingModelsTable embeddingModels={data.models.embeddingModels} />
    </Page.Tab>
    <Page.Tab id="transcription_models">
      <TranscriptionModelsTable transcriptionModels={data.models.transcriptionModels} />
    </Page.Tab>
  </Page.Main>
</Page.Root>
