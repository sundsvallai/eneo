<script lang="ts">
  import { type Tokens } from "marked";
  import RenderToken from "./RenderToken.svelte";

  export let token: Tokens.Table;
</script>

<table>
  <thead>
    <tr>
      {#each token.header as cell (cell)}
        <th scope="col" style={cell.align ? `text-align: ${cell.align};` : undefined}>
          <RenderToken token={cell.tokens} />
        </th>
      {/each}
    </tr>
  </thead>
  <tbody>
    {#each token.rows as row (row)}
      <tr>
        {#each row as cell (cell)}
          <td style={cell.align ? `text-align: ${cell.align};` : undefined}>
            <RenderToken token={cell.tokens} />
          </td>
        {/each}
      </tr>
    {/each}
  </tbody>
</table>
