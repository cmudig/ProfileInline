<script lang="ts">
  import DFProfile from './components/DFProfile.svelte';
  import { dfProfile } from './stores';
</script>

<div class="divider" />

<DFProfile
  dfName={$dfProfile.dfName}
  dataframeProfile={$dfProfile.profile}
  shape={$dfProfile.shape}
  isInFocus={false}
  isPinned={$dfProfile.isPinned}
/>

<style>
  .divider {
    height: 50px;
    background-color: red;
  }
</style>
