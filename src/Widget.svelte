<script lang="ts">
    import { setContext } from 'svelte';
    import DFProfile from './components/DFProfile.svelte';
    import type { IDFProfileWState } from './common/exchangeInterfaces';
    import { WidgetWritable } from './stores';

    export let model;

    const dfProfile = WidgetWritable<IDFProfileWState>(
        'dfProfile',
        {
            profile: [],
            shape: [0, 0],
            dfName: 'test',
            lastUpdatedTime: 0,
            isPinned: false,
            warnings: []
        },
        model
    );

    const exportedCode = WidgetWritable<string>('exportedCode', '', model);

    setContext('inlineprofiler:exportedCode', exportedCode);
</script>

<DFProfile
    dfName={$dfProfile.dfName}
    dataframeProfile={$dfProfile}
    isInFocus={false}
    isPinned={$dfProfile.isPinned}
/>
