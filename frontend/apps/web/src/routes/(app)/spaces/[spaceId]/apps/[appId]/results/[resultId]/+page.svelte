<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { IconCopy } from "@intric/icons/copy";
  import { IconDownload } from "@intric/icons/download";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
  import { IconPrint } from "@intric/icons/print";
  import { Button, Markdown, Tooltip } from "@intric/ui";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import dayjs from "dayjs";
  import utc from "dayjs/plugin/utc";
  import { getResultTitle } from "$lib/features/apps/getResultTitle.js";
  import AppResultStatus from "$lib/features/apps/components/AppResultStatus.svelte";
  import { onMount } from "svelte";
  import { getIntricSocket } from "$lib/core/IntricSocket.js";
  import Tabbar from "$lib/components/layout/Page/Tabbar.svelte";
  import TabTrigger from "$lib/components/layout/Page/TabTrigger.svelte";
  import Tab from "$lib/components/layout/Page/Tab.svelte";
  import UploadedFileIcon from "$lib/features/attachments/components/UploadedFileIcon.svelte";
  import type { UploadedFile } from "@intric/intric-js";
  import { getAttachmentUrlService } from "$lib/features/attachments/AttachmentUrlService.svelte.js";
  import { getIntric } from "$lib/core/Intric.js";
  import { browser } from "$app/environment";
  dayjs.extend(utc);

  const { data } = $props();

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const { subscribe } = getIntricSocket();
  const intric = getIntric();

  const attachmentUrlService = getAttachmentUrlService();

  let result = $state(data.result);
  const resultTitle = $derived(getResultTitle(result));

  async function downloadAsText(text?: string | null) {
    if (!text) {
      alert("Not output to save!");
      return;
    }
    const file = new Blob([text], { type: "application/octet-stream;charset=utf-8" });
    const suggestedName =
      data.app.name + dayjs(result.created_at).format(" YYYY-MM-DD HH:mm") + ".txt";
    if (window.showSaveFilePicker) {
      const handle = await window.showSaveFilePicker({ suggestedName });
      const writable = await handle.createWritable();
      await writable.write(file);
      writable.close();
    } else {
      const a = document.createElement("a");
      a.download = suggestedName;
      a.href = URL.createObjectURL(file);
      a.click();
      setTimeout(function () {
        URL.revokeObjectURL(a.href);
      }, 1500);
    }
  }

  // We should subscribe to this specific app here somewhere

  let printElement = $state<HTMLDivElement>();
  function print() {
    if (!printElement) return;
    const printNode = printElement.cloneNode(true);
    document.body.appendChild(printNode);
    document.body.classList.add("print-mode");
    window.print();
    document.body.classList.remove("print-mode");
    document.body.removeChild(printNode);
  }

  function copyText(text?: string | null) {
    if (text) {
      navigator.clipboard.writeText(text);
      setTimeout(() => {}, 2000);
    } else {
      alert("This run did not generate any copyable output.");
    }
  }

  const isRunComplete = $derived(!(result.status === "in progress" || result.status === "queued"));

  function isTranscribedFile(file: UploadedFile): file is UploadedFile & { transcription: string } {
    return file.transcription !== null && file.transcription !== undefined;
  }

  let transcribedFiles = $derived.by(() => {
    if (!result.output) return [];
    return result.input.files.filter((file) => isTranscribedFile(file));
  });

  onMount(() => {
    if (isRunComplete) return;

    const unsubscriber = subscribe("app_run_updates", async (update) => {
      if (update.id === data.result.id) {
        result = await data.intric.apps.runs.get(result);
      }
    });

    // There is a bit of an edge case where the run is still "queued" when the load function runs
    // and switches to "in progress" just before the websocket handler is registered. This makes us
    // miss a crucial update; as a work around we always poll once more in case we missed sth.
    if (result.status === "queued") {
      data.intric.apps.runs.get(result).then((updatedResult) => {
        result = updatedResult;
      });
    }

    return unsubscriber;
  });
</script>

<svelte:head>
  <title
    >Eneo.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – {data.app
      .name}</title
  >
</svelte:head>

{#snippet formattedResult()}
  {#if result.output}
    {@render downloadButtons("output", result.output)}
    <Markdown source={result.output}></Markdown>
  {:else}
    <div class="flex items-center justify-center gap-2">
      <span class="text-secondary"> This run did not generate any output.</span>
    </div>
  {/if}
{/snippet}

{#snippet downloadButtons(type: "output" | "transcription", text?: string)}
  <div
    class="hidden-in-print border-default bg-primary absolute -right-[5.5rem] z-10 flex flex-col gap-1 rounded-lg border p-1 shadow"
  >
    <Tooltip text="Print / Save {type} as PDF" placement="left">
      <Button on:click={print} padding="icon">
        <IconPrint size="md" />
      </Button>
    </Tooltip>

    <Tooltip text="Download {type} as raw text" placement="left">
      <Button on:click={() => downloadAsText(text)} padding="icon"><IconDownload /></Button>
    </Tooltip>

    <Tooltip text="Copy {type}" placement="left">
      <Button on:click={() => copyText(text)} padding="icon"><IconCopy /></Button>
    </Tooltip>
  </div>
{/snippet}

<Page.Root>
  <Page.Header>
    <Page.Title
      parent={{
        title: "Back",
        href: `/spaces/${$currentSpace.routeId}/apps/${data.app.id}`
      }}
      title={resultTitle}
    ></Page.Title>

    <Page.Flex>
      <Button href="/spaces/{$currentSpace.routeId}/apps/{data.app.id}/edit" class="!line-clamp-1"
        >Edit</Button
      >
      <Button
        variant="primary"
        class="!line-clamp-1"
        href="/spaces/{$currentSpace.routeId}/apps/{data.app.id}">New run</Button
      >
    </Page.Flex>
  </Page.Header>

  <Page.Main>
    <div class="flex items-start justify-center gap-16 p-8">
      <div
        class=" prose border-default bg-primary relative min-h-72 w-full max-w-[90ch] rounded-sm border px-16 py-8 text-lg shadow-lg"
      >
        <div class="printable-document relative flex flex-col py-4" bind:this={printElement}>
          {#if isRunComplete}
            {#if transcribedFiles.length > 0}
              <div class="hidden-in-print -mt-2 h-20">
                <Tabbar>
                  <TabTrigger tab="results">Results</TabTrigger>
                  <TabTrigger tab="transcription">Transcription</TabTrigger>
                </Tabbar>
              </div>
              <Tab id="results">
                {@render formattedResult()}
              </Tab>
              <Tab id="transcription">
                <div class="flex flex-col gap-8">
                  {#each transcribedFiles as file (file.id)}
                    {@const url = attachmentUrlService.getUrl(file)}
                    {@render downloadButtons("transcription", file.transcription)}

                    <div class="border-stronger bg-secondary rounded-xl border print:border-none">
                      {#if url}
                        <div
                          class="hidden-in-print border-stronger bg-primary -m-[1px] rounded-xl border p-2 shadow"
                        >
                          <div class="flex items-center justify-between gap-4 px-1 pb-2">
                            <div class="flex gap-2">
                              <UploadedFileIcon {file}></UploadedFileIcon>
                              {file.name}
                            </div>
                            <Button href={url}>
                              <IconDownload></IconDownload>
                              Download</Button
                            >
                          </div>
                          <audio
                            controls
                            src={url}
                            class="border-stronger h-8 w-full rounded-full border shadow-sm"
                          ></audio>
                        </div>
                      {/if}
                      <div class="p-4">
                        <Markdown source={file.transcription}></Markdown>
                      </div>
                    </div>
                  {/each}
                </div>
              </Tab>
            {:else if result.output}
              {@render formattedResult()}
              <!-- Need to check for browser as we make a fetch request in the await -->
            {:else if browser && result.status === "failed" && result.input.files.length > 0}
              <div class="flex flex-grow flex-col items-center justify-center gap-2">
                <span class="py-2">
                  This app run failed. Here is a list of the files you uploaded:
                </span>

                {#each result.input.files as file (file.id)}
                  {#await intric.files.url({ id: file.id, download: true }) then fileUrl}
                    <Button href={fileUrl} class="outlined no-underline"
                      ><IconDownload></IconDownload>Download "{file.name}"</Button
                    >
                  {/await}
                {/each}
              </div>
            {:else}
              <div class="flex flex-grow flex-col items-center justify-center gap-2">
                <span class="py-2"> This app run did not generate any outputs. </span>
              </div>
            {/if}
          {:else}
            <div class="flex h-[50vh] flex-col items-center justify-center gap-2">
              <IconLoadingSpinner class="animate-spin" />
              <span class="text-secondary">Your result is being generated.</span>
            </div>
          {/if}
        </div>
      </div>
      <div class="sticky top-8 flex min-w-[26ch] flex-col gap-4">
        <div class="flex flex-col gap-3 pt-2">
          <div class="border-dimmer flex items-center justify-between border-b">
            <span>Started:</span><span class="font-mono text-sm"
              >{dayjs(result.created_at).format("YYYY-MM-DD HH:mm")}</span
            >
          </div>
          {#if isRunComplete}
            <div class="border-dimmer flex items-center justify-between border-b">
              <span>Finished:</span><span class="font-mono text-sm"
                >{dayjs(result.finished_at).format("YYYY-MM-DD HH:mm")}</span
              >
            </div>
          {/if}
          <AppResultStatus run={result} variant="full"></AppResultStatus>

          {#each result.input.files as file (file.id)}
            <div
              class="border-default bg-primary flex items-center gap-2 rounded-lg border px-4 py-3 shadow"
            >
              <UploadedFileIcon class="min-w-6" {file} />
              <span
                class="line-clamp-1 overflow-hidden break-words overflow-ellipsis hover:line-clamp-5"
              >
                {file.name}
              </span>
            </div>
          {/each}
        </div>
      </div>
    </div>
  </Page.Main>
</Page.Root>
