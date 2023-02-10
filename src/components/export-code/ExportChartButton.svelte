<script lang="ts">
    import RightArrow from '../icons/RightArrow.svelte';
    import Tooltip from '../tooltip/Tooltip.svelte';
    import TooltipContent from '../tooltip/TooltipContent.svelte';
    import { getContext } from 'svelte';
    import type { Writable } from 'svelte/store';

    import { QUANT_CHART, CAT_CHART, TEMPORAL_CHART } from './ExportableCode';

    export let chartType: 'quant' | 'cat' | 'temporal';
    export let dfName: string;
    export let colName: string;
    export let exportOptions: {
        numBins?: number;
        shouldDisableMaxRows?: boolean;
    } = undefined;
    export let isIndex = false;

    const exportedCode: Writable<string> = getContext(
        'inlineprofiler:exportedCode'
    );

    function addVisCode() {
        let text: string;
        if (chartType == 'quant') {
            text = QUANT_CHART(
                dfName,
                colName,
                exportOptions?.numBins,
                isIndex
            );
        } else if (chartType == 'cat') {
            text = CAT_CHART(dfName, colName, 10, isIndex);
        } else {
            text = TEMPORAL_CHART(
                dfName,
                colName,
                exportOptions?.shouldDisableMaxRows,
                isIndex
            );
        }

        console.log(text);

        $exportedCode = text;

        // TODO add cell here
        // addCell('code', text);
    }
</script>

<div class="flex justify-end w-full">
    <Tooltip location="bottom" alignment="center" distance={8}>
        <button
            class="hover:bg-gray-100 text-gray-400 grid place-items-center rounded"
            style="width: 16px; height: 16px;"
            on:click={addVisCode}
        >
            <RightArrow size="16px" />
        </button>

        <TooltipContent slot="tooltip-content"
            >Export chart to code</TooltipContent
        >
    </Tooltip>
</div>
