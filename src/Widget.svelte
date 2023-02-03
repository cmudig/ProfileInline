<script lang="ts">
  import { value } from './stores';

  let localValue = $value;
</script>

<p>The value is {$value}</p>
<p>Hello world!!!!!!!</p>
<p>is this working</p>

<input bind:value={localValue} />
<button on:click={() => value.set(localValue)}>Set Value</button>
