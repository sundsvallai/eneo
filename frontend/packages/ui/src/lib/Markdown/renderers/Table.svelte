<script lang="ts">
  import { type Tokens } from "marked";
  import RenderToken from "./RenderToken.svelte";

  export let token: Tokens.Table;
</script>

<table>
  <thead>
    <tr>
      {#each token.header as cell}
        <th scope="col">
          {#each cell.tokens as children}
            <RenderToken token={children} />
          {/each}
        </th>
      {/each}
    </tr>
  </thead>
  <tbody>
    {#each token.rows as row}
      <tr>
        {#each row as cell}
          <td>
            {#each cell.tokens as children}
              <RenderToken token={children} />
            {/each}
          </td>
        {/each}
      </tr>
    {/each}
  </tbody>
</table>
