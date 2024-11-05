<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->
<script lang="ts">
  import IconUpload from "$lib/components/icons/IconUpload.svelte";
  import { getAppContext } from "$lib/core/AppContext";
  import { getFileUploadManager } from "$lib/features/file-uploads/FileUploadManager";
  import { Tooltip } from "@intric/ui";

  let filesToUpload: FileList;
  let fileInput: HTMLInputElement | null;
  export let imagesAllowed: boolean = false;

  const {
    state: { uploads },
    queueUploads
  } = getFileUploadManager();

  const { limits } = getAppContext();
  const allMimeTypes = limits.attachments.formats.map((format) => format.mimetype);
  const acceptedMimeTypes = imagesAllowed
    ? allMimeTypes
    : limits.attachments.formats.filter((format) => format.vision).map((format) => format.mimetype);
  const maxFiles = limits.attachments.max_in_question;

  function getMaxSizeForMimeType(mimeType: string): number | undefined {
    const format = limits.attachments.formats.find((format) => format.mimetype === mimeType);
    return format ? format.size : undefined;
  }

  function validateFiles(files: FileList) {
    if (files.length + $uploads.length > maxFiles) {
      alert(`You can only upload ${maxFiles} files at a time`);
      return false;
    }

    for (const file of files) {
      const acceptedFileType = acceptedMimeTypes.some((type) => file.type.includes(type));
      if (!acceptedFileType) {
        alert(`File type ${file.type} is not supported`);
        return false;
      }
      const maxSize = getMaxSizeForMimeType(file.type);
      if (maxSize !== undefined && file.size > maxSize) {
        alert(
          `File ${file.name} is too large. Maximum size is ${maxSize} bytes while ${file.name} is ${file.size} bytes.`
        );
        return false;
      }
    }

    return true;
  }

  function uploadFiles() {
    if (!filesToUpload) return;
    const filesArray = Array.from(filesToUpload);
    if (!validateFiles(filesToUpload)) return;
    queueUploads(filesArray);
    if (fileInput) {
      fileInput = null;
    }
  }
</script>

<Tooltip text={`Upload ${imagesAllowed ? "documents or images" : "documents"}`}>
  <div class="flex h-full items-center">
    <input
      type="file"
      accept={acceptedMimeTypes.join()}
      bind:this={fileInput}
      bind:files={filesToUpload}
      class="hidden"
      multiple
      id="fileInput"
      on:change={uploadFiles}
    />
    <label
      for="fileInput"
      class="rounded-lg border border-stone-100 bg-stone-100 p-2 text-lg hover:cursor-pointer hover:bg-stone-300"
      ><IconUpload class="!h-7 !w-7 stroke-black" /></label
    >
  </div>
</Tooltip>
