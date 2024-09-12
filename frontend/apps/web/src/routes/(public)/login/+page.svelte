<script lang="ts">
  import { page } from "$app/stores";
  import { enhance } from "$app/forms";
  import { Button, Input } from "@intric/ui";
  import { goto } from "$app/navigation";
  import IntricLogo from "$lib/components/icons/IntricLogo.svelte";

  export let data;
  let loginFailed = false;

  let isAwaitingLoginResponse = false;
  $: message = $page.url.searchParams.get("message") ?? null;
</script>

<svelte:head>
  <title>Intric.ai – Login</title>
</svelte:head>

<!-- <div class="absolute bottom-2 h-[1px] w-full bg-stone-300"></div> -->

<div class="relative flex h-[100vh] w-[100vw] items-center justify-center">
  <div class="box w-[400px] justify-center">
    <h1 class="flex justify-center">
      <IntricLogo class="h-16 w-20  text-blue-700"></IntricLogo>
      <span class="hidden">Intric</span>
    </h1>

    <div aria-live="polite">
      {#if message === "logout"}
        <div class="mb-2 flex flex-col gap-3 bg-green-50 p-4 text-green-600 shadow-lg">
          Successfully logged out!
        </div>{/if}
      {#if message === "expired"}
        <div class="mb-2 flex flex-col gap-3 bg-amber-50 p-4 text-amber-600 shadow-lg">
          Session expired. Please login again.
        </div>{/if}
      {#if message === "oicderror"}
        <div class="mb-2 flex flex-col gap-3 bg-red-50 p-4 text-red-600 shadow-lg">
          The selected login method was not successful. Please use a different login method or try
          again later.
        </div>{/if}
    </div>

    <form
      method="POST"
      class="flex flex-col gap-3 border-stone-200 bg-white p-4"
      action="?/login"
      use:enhance={() => {
        isAwaitingLoginResponse = true;

        return async ({ result }) => {
          if (result.type === "redirect") {
            goto(result.location);
          } else {
            isAwaitingLoginResponse = false;
            message = null;
            loginFailed = true;
          }
        };
      }}
    >
      <input type="text" hidden value={$page.url.searchParams.get("next") ?? ""} name="next" />

      {#if loginFailed}
        <div class=" rounded-lg bg-red-50 p-4 text-red-600">
          Incorrect credentials. Please provide a valid username and a valid password.
        </div>{/if}

      <Input.Text
        value=""
        name="email"
        autocomplete="username"
        type="email"
        required
        labelClass="hidden"
        placeholder="Email"
      >
        Email
      </Input.Text>

      <Input.Text
        value=""
        name="password"
        autocomplete="current-password"
        type="password"
        required
        labelClass="hidden"
        placeholder="Password"
      >
        Password
      </Input.Text>

      <Button type="submit" disabled={isAwaitingLoginResponse} variant="primary">
        {#if isAwaitingLoginResponse}
          Logging in...
        {:else}
          Login
        {/if}
      </Button>
      {#if data.mobilityguardLink}
        <div class="flex items-center justify-center gap-4 text-xs text-stone-400">
          <div class="flex-grow border-b border-stone-200"></div>
          MORE LOGIN METHODS
          <div class="flex-grow border-b border-stone-200"></div>
        </div>
        <Button
          variant="primary"
          href={data.mobilityguardLink}
          class="!border-black !bg-black hover:!bg-blue-800">Login with MobilityGuard</Button
        >
      {/if}
    </form>
  </div>
</div>

<style>
  form {
    box-shadow: 0px 8px 20px 4px rgba(0, 0, 0, 0.1);
    border: 0.5px solid rgba(54, 54, 54, 0.3);
  }
</style>
