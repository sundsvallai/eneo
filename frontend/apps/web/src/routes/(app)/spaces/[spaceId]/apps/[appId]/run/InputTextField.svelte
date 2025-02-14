<script lang="ts">
  export let description: string | null | undefined;
  export let value: string | null;
  let text: string;
  let textarea: HTMLTextAreaElement;

  function calculateTextAreaHeight() {
    textarea.style.height = "";
    const scrollHeight = Math.min(textarea.scrollHeight, 250);
    textarea.style.height = scrollHeight > 45 ? scrollHeight + "px" : "auto";
    textarea.style.overflowY = scrollHeight === 250 ? "auto" : "hidden";
  }
</script>

<div
  class="flex max-h-[40vh] min-w-[50ch] max-w-[80ch] flex-col justify-center rounded-[1.2rem] border border-stronger bg-secondary p-0.5 shadow-xl"
>
  <textarea
    aria-label="Enter your question here"
    bind:this={textarea}
    bind:value={text}
    on:input={() => {
      calculateTextAreaHeight();
      if (text) {
        value = text;
      } else {
        value = null;
      }
    }}
    name="textinput"
    placeholder={description ?? "Enter text here..."}
    rows="4"
    class="flex-grow resize-none overflow-y-auto rounded-[1rem] border border-default bg-primary px-6 py-3 text-lg placeholder:text-secondary"
  ></textarea>
</div>
