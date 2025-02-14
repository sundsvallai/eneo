<script lang="ts">
  /** Current progress percentage (0-100) */
  export let progress: number;
</script>

<div
  class="flex h-2 w-full overflow-hidden rounded-full bg-tertiary"
  role="progressbar"
  aria-valuenow={progress}
  aria-valuemin="0"
  aria-valuemax="100"
>
  <div
    class="flex flex-col justify-center overflow-hidden whitespace-nowrap rounded-full text-center text-xs text-on-fill transition duration-500 {progress ===
    100
      ? 'bg-positive-default'
      : 'bg-accent-default'}"
    style="width: {progress}%"
  ></div>
</div>
