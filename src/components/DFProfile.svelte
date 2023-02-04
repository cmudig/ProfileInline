<script lang="ts">
  export let dfName: string;
  export let shape: number[];
  export let dataframeProfile: any[];

  //   wont need
  export let isInFocus = false;
  export let isPinned;
</script>

<div>
  This dataframe has name {dfName}.
</div>
<div>
  It has a shape of {shape}
</div>
<div>
  The profile is {JSON.stringify(dataframeProfile)}
</div>
