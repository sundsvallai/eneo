<script lang="ts">
  import { page } from "$app/stores";
  import { enhance } from "$app/forms";
  import { Button, Input } from "@intric/ui";
  import { goto } from "$app/navigation";
  import { browser } from "$app/environment";
  import { LoadingScreen } from "$lib/components/layout";
  import IntricWordMark from "$lib/assets/IntricWordMark.svelte";

  export let data;
  let loginFailed = false;
  let isAwaitingLoginResponse = false;

  $: message = $page.url.searchParams.get("message") ?? null;
  $: showUsernameAndPassword = $page.url?.searchParams.get("showUsernameAndPassword");

  // We don't redirect on the server so we can render a loader/spinner during the redirection period
  if (data.zitadelLink && browser) {
    window.location.href = data.zitadelLink;
  }
</script>

<svelte:head>
  <title>Intric.ai – Login</title>
</svelte:head>

{#if data.zitadelLink}
  <LoadingScreen />
{:else}
  <div class="relative flex h-[100vh] w-[100vw] items-center justify-center">
    <div class="box w-[400px] justify-center">
      <h1 class="flex justify-center">
        <IntricWordMark class="h-16 w-20 text-brand-intric" />
        <span class="sr-only">Intric</span>
      </h1>

      <div aria-live="polite">
        {#if message === "logout"}
          <div
            class="mb-2 flex flex-col gap-3 bg-positive-dimmer p-4 text-positive-default shadow-lg"
          >
            Successfully logged out!
          </div>{/if}
        {#if message === "expired"}
          <div
            class="mb-2 flex flex-col gap-3 bg-warning-dimmer p-4 text-warning-default shadow-lg"
          >
            Session expired. Please login again.
          </div>{/if}
        {#if message === "mobilityguard_login_error"}
          <div
            class="mb-2 flex flex-col gap-3 bg-negative-dimmer p-4 text-negative-default shadow-lg"
          >
            The selected login method was not successful. Please use a different login method or try
            again later.
          </div>{/if}
      </div>

      <form
        method="POST"
        class="flex flex-col gap-3 border-default bg-primary p-4"
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
          <div class="label-negative rounded-lg bg-label-dimmer p-4 text-label-stronger">
            Incorrect credentials. Please provide a valid username and a valid password.
          </div>
        {/if}

        {#if showUsernameAndPassword || !data.mobilityguardLink}
          <Input.Text
            label="Email"
            value=""
            name="email"
            autocomplete="username"
            type="email"
            required
            hiddenLabel={true}
            placeholder="Email"
          ></Input.Text>

          <Input.Text
            label="Password"
            value=""
            name="password"
            autocomplete="current-password"
            type="password"
            required
            hiddenLabel={true}
            placeholder="Password"
          ></Input.Text>

          <Button type="submit" disabled={isAwaitingLoginResponse} variant="primary">
            {#if isAwaitingLoginResponse}
              Logging in...
            {:else}
              Login
            {/if}
          </Button>
        {:else}
          <Button variant="primary" href={data.mobilityguardLink}>Login</Button>
        {/if}
      </form>
    </div>
    <div class="absolute bottom-10 mt-12 flex justify-center">
      {#if showUsernameAndPassword && data.mobilityguardLink}
        <Button variant="outlined" class="text-secondary" href="/login?">Hide Login Fields</Button>
      {:else if data.mobilityguardLink}
        <Button
          variant="outlined"
          class="text-secondary"
          href="/login?showUsernameAndPassword=true"
        >
          Show Login Fields
        </Button>
      {/if}
    </div>
  </div>
{/if}

<style>
  form {
    box-shadow: 0px 8px 20px 4px rgba(0, 0, 0, 0.1);
    border: 0.5px solid rgba(54, 54, 54, 0.3);
  }
</style>
