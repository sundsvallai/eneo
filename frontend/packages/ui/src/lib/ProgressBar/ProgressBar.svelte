<script lang="ts">
  /** Current progress percentage (0-100) */
  export let progress: number;
</script>

<div
  class="bg-tertiary flex h-2 w-full overflow-hidden rounded-full"
  role="progressbar"
  aria-valuenow={progress}
  aria-valuemin="0"
  aria-valuemax="100"
>
  <div
    class="text-on-fill flex flex-col justify-center overflow-hidden rounded-full text-center text-xs whitespace-nowrap transition duration-500 {progress ===
    100
      ? 'bg-positive-default'
      : 'bg-accent-default'}"
    style="width: {progress}%"
  ></div>
</div>
