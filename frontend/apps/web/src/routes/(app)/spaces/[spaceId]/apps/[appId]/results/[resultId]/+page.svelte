<script lang="ts">
  import { Page } from "$lib/components/layout";
  import { IconFile } from "@intric/icons/file";
  import { IconCopy } from "@intric/icons/copy";
  import { IconDownload } from "@intric/icons/download";
  import { IconLoadingSpinner } from "@intric/icons/loading-spinner";
  import { IconPrint } from "@intric/icons/print";
  import { Button, Markdown } from "@intric/ui";
  import { getSpacesManager } from "$lib/features/spaces/SpacesManager";
  import dayjs from "dayjs";
  import utc from "dayjs/plugin/utc";
  import { getResultTitle } from "$lib/features/apps/getResultTitle.js";
  import AppResultStatus from "$lib/features/apps/components/AppResultStatus.svelte";
  import { onMount } from "svelte";
  import { getIntricSocket } from "$lib/core/IntricSocket.js";
  dayjs.extend(utc);

  export let data;

  const {
    state: { currentSpace }
  } = getSpacesManager();

  const { subscribe } = getIntricSocket();

  let result = data.result;
  const resultTitle = getResultTitle(result);

  async function downloadAsText() {
    if (!result.output) {
      alert("Not output to save!");
      return;
    }
    const file = new Blob([result.output], { type: "application/octet-stream;charset=utf-8" });
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

  let printElement: HTMLDivElement;
  function print() {
    const printNode = printElement.cloneNode(true);
    document.body.appendChild(printNode);
    document.body.classList.add("print-mode");
    window.print();
    document.body.classList.remove("print-mode");
    document.body.removeChild(printNode);
  }

  let copyButtonText = "Copy response";
  function copyText() {
    if (result.output) {
      navigator.clipboard.writeText(result.output);
      copyButtonText = "Copied!";
      setTimeout(() => {
        copyButtonText = "Copy response";
      }, 2000);
    } else {
      alert("This run did not generate any copyable output.");
    }
  }

  $: isRunComplete = !(result.status === "in progress" || result.status === "queued");

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
    >Intric.ai – {data.currentSpace.personal ? "Personal" : data.currentSpace.name} – {data.app
      .name}</title
  >
</svelte:head>

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
    <div class="flex items-start justify-center gap-8 p-8">
      <div
        class=" prose relative w-full max-w-[100ch] rounded-sm border border-default bg-primary px-20 py-10 text-lg shadow-lg"
      >
        <div class="printable-document py-4" bind:this={printElement}>
          {#if isRunComplete}
            {#if result.output}
              <Markdown source={result.output}></Markdown>
            {:else}
              <div class="flex h-[50vh] items-center justify-center gap-2">
                <span class="text-secondary"> This run did not generate any output.</span>
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
        <div class="flex flex-col gap-3 rounded-lg border border-default bg-primary p-4 shadow-lg">
          <div class="flex items-center justify-between border-b border-dimmer">
            <span>Started:</span><span class="font-mono text-sm"
              >{dayjs(result.created_at).format("YYYY-MM-DD HH:mm")}</span
            >
          </div>
          {#if isRunComplete}
            <div class="flex items-center justify-between border-b border-dimmer">
              <span>Finished:</span><span class="font-mono text-sm"
                >{dayjs(result.finished_at).format("YYYY-MM-DD HH:mm")}</span
              >
            </div>
          {/if}
          <AppResultStatus run={result} variant="full"></AppResultStatus>

          {#each result.input.files as file}
            <div
              class="flex items-center gap-2 rounded-lg border border-default bg-primary px-4 py-3 shadow"
            >
              <IconFile class="min-w-6" />
              <span
                class="line-clamp-1 overflow-hidden overflow-ellipsis break-words hover:line-clamp-5"
              >
                {file.name}
              </span>
            </div>
          {/each}
        </div>
        {#if isRunComplete && result.output}
          <div class="flex flex-col gap-2 px-4">
            <Button variant="primary" on:click={copyText}><IconCopy />{copyButtonText}</Button>
            <Button on:click={downloadAsText}><IconDownload />Download raw text</Button>
            <Button on:click={print}>
              <IconPrint size="md" />
              Print / Save as PDF</Button
            >
          </div>
        {/if}
      </div>
    </div>
  </Page.Main>
</Page.Root>
