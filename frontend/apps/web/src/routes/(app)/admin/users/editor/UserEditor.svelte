<!--
    Copyright (c) 2024 Sundsvalls Kommun

    Licensed under the MIT License.
-->

<script lang="ts">
  import { invalidate } from "$app/navigation";
  import SelectRole from "./SelectRole.svelte";
  import { makeEditable } from "$lib/core/editable";
  import { type Role, type UserGroup } from "@intric/intric-js";
  import { Dialog, Button, Input } from "@intric/ui";
  import SelectUserGroups from "./SelectUserGroups.svelte";
  import { getIntric } from "$lib/core/Intric";
  import { getAdminUserCtx } from "../ctx";

  const intric = getIntric();

  const { defaultRoles, customRoles, userGroups } = getAdminUserCtx();

  const createEmptyUser = () => {
    return {
      id: "",
      email: "",
      username: "",
      predefined_roles: [],
      roles: [],
      user_groups: []
    };
  };

  export let mode: "update" | "create" = "create";

  export let user: {
    id: string;
    username: string;
    email: string;
    predefined_roles: Role[];
    roles: Role[];
    user_groups: UserGroup[];
  } = createEmptyUser();

  let userPassword = "";
  let userRoles = user.predefined_roles.concat(user.roles);
  let defaultRolesIds = defaultRoles.flatMap((role) => role.id);

  let editableUser = makeEditable(user);

  let showDialog: Dialog.OpenState;

  function getRolesUpdate() {
    const updatedRoles = userRoles.reduce(
      (prev, curr) => {
        if (defaultRolesIds.includes(curr.id)) {
          prev.predefined_roles.push(curr);
        } else {
          prev.roles.push(curr);
        }
        return prev;
      },
      {
        roles: [] as Role[],
        predefined_roles: [] as Role[]
      }
    );
    return updatedRoles;
  }

  async function updateUser() {
    const update = {
      ...editableUser.getEdits(),
      password: userPassword === "" ? undefined : userPassword,
      ...getRolesUpdate()
    };
    try {
      await intric.users.update({
        user,
        update
      });
      invalidate("admin:users:load");
      // Invalidate does not update the user and userPassword values in this component, so we need to update
      user = editableUser;
      userPassword = "";
      $showDialog = false;
    } catch (e) {
      alert(e);
    }
  }

  async function createUser() {
    if (editableUser.username === "" || editableUser.email === "" || userPassword === "") {
      return;
    }
    const newUser = { ...editableUser, password: userPassword, ...getRolesUpdate() };
    try {
      await intric.users.create(newUser);
      editableUser.updateWithValue(createEmptyUser());
      userPassword = "";
      invalidate("admin:users:load");
      $showDialog = false;
    } catch (e) {
      alert(e);
    }
  }
</script>

<Dialog.Root bind:isOpen={showDialog}>
  {#if mode === "create"}
    <Dialog.Trigger asFragment let:trigger>
      <Button variant="primary" is={trigger}>Create user</Button>
    </Dialog.Trigger>
  {:else}
    <Dialog.Trigger asFragment let:trigger>
      <Button is={trigger}>Edit</Button>
    </Dialog.Trigger>
  {/if}

  <Dialog.Content form wide>
    {#if mode === "create"}
      <Dialog.Title>Create a new user</Dialog.Title>
      <Dialog.Description hidden>Create a new user</Dialog.Description>
    {:else}
      <Dialog.Title>Edit user</Dialog.Title>
      <Dialog.Description hidden>Edit the selected user</Dialog.Description>
    {/if}

    <Dialog.Section>
      <div class="hover:bg-stone-50">
        <Input.Text
          bind:value={editableUser.username}
          required
          class="border-stone-100 px-4 py-4  {mode === 'create' ? 'border-b' : ''}"
        >
          <div class="flex items-baseline justify-between">
            Username<span class="px-2 text-[0.9rem] font-normal text-stone-400"
              >A unique username without spaces</span
            >
          </div></Input.Text
        >

        {#if mode === "update"}
          <p class="border-b border-stone-100 pb-4 pl-6 pr-4 text-sm text-stone-600">
            Hint: Changing the username requires this user to logout and login again.
          </p>
        {/if}
      </div>

      <Input.Text
        bind:value={editableUser.email}
        type="email"
        required
        class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50">Email</Input.Text
      >

      <Input.Text
        bind:value={userPassword}
        minlength="7"
        maxlength="100"
        required={mode === "create"}
        type="password"
        autocomplete="off"
        class="border-b border-stone-100 px-4 py-4 hover:bg-stone-50"
      >
        <div class="flex items-baseline justify-between">
          Password<span class="px-2 text-[0.9rem] font-normal text-stone-400"
            >Needs to be at least 7 characters long</span
          >
        </div></Input.Text
      >

      <SelectRole {customRoles} {defaultRoles} bind:value={userRoles}></SelectRole>

      {#if mode === "update"}
        <SelectUserGroups bind:selectedGroups={editableUser.user_groups} {userGroups} {user}
        ></SelectUserGroups>
      {/if}
    </Dialog.Section>

    <Dialog.Controls let:close>
      <Button is={close}>Cancel</Button>
      {#if mode === "create"}
        <Button variant="primary" on:click={createUser} type="submit">Create user</Button>
      {:else}
        <Button variant="primary" on:click={updateUser}>Save changes</Button>
      {/if}
    </Dialog.Controls>
  </Dialog.Content>
</Dialog.Root>
