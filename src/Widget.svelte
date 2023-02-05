<script lang="ts">
  import DFProfile from './components/DFProfile.svelte';
  import { dfProfile } from './stores';
</script>

<DFProfile
  dfName={$dfProfile.dfName}
  dataframeProfile={$dfProfile}
  isInFocus={false}
  isPinned={$dfProfile.isPinned}
/>
