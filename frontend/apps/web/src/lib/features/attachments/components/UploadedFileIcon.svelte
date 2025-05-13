<script lang="ts">
  import { IconFile } from "@intric/icons/file";
  import { IconFileAudio } from "@intric/icons/file-audio";
  import { IconFileImage } from "@intric/icons/file-image";
  import { IconFileText } from "@intric/icons/file-text";
  import type { ClassValue } from "svelte/elements";

  const icons = {
    image: IconFileImage,
    audio: IconFileAudio,
    // We only support audio, but webm has video as mime type
    video: IconFileAudio,
    text: IconFileText,
    fallback: IconFile
  };

  type Props = {
    file?: { mimetype: string };
    class?: ClassValue;
  };

  const { file, class: cls }: Props = $props();
  const Icon = $derived.by(() => {
    if (!file) return icons.fallback;
    // (e.g., "image" from "image/jpeg")
    const generalType = file.mimetype.split("/")[0];
    // @ts-expect-error We dont care about index signature in this case
    return icons[generalType] || icons.fallback;
  });
</script>

<Icon class={cls}></Icon>
