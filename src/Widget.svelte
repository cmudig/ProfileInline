<script lang="ts">
    import DFProfile from './components/DFProfile.svelte';
    import type { Writable } from 'svelte/store';
    import type { IDFProfileWState } from './common/exchangeInterfaces';

    export let dfProfileStore: Writable<IDFProfileWState>;
</script>

<DFProfile
    dfName={$dfProfileStore.dfName}
    dataframeProfile={$dfProfileStore}
    isInFocus={false}
    isPinned={$dfProfileStore.isPinned}
/>
