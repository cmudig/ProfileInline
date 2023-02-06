<script lang="ts">
    import _ from 'lodash';
    import { createEventDispatcher } from 'svelte';

    import type { IDFProfileWState } from '../common/exchangeInterfaces';

    import CollapsibleCard from './nav/CollapsibleCard.svelte';
    import ColumnProfile from './ColumnProfile.svelte';
    import ExpanderButton from './nav/ExpanderButton.svelte';
    import Pin from './icons/Pin.svelte';
    import Tooltip from './tooltip/Tooltip.svelte';
    import TooltipContent from './tooltip/TooltipContent.svelte';
    import { formatInteger } from './utils/formatters';
    import { logger } from '../logger/Logger';

    export let dfName: string;
    export let dataframeProfile: IDFProfileWState;
    export let isInFocus = false;
    export let isPinned = false;

    console.log('In Dfprofile the dfName is: ', dfName);
    console.log('In Dfprofile the dataframeProfile is: ', dataframeProfile);

    // locals
    let previewView = 'summaries';
    $: warningMessage = _.isEmpty(dataframeProfile.warnings)
        ? ''
        : dataframeProfile.warnings.map(w => w.warnMsg).join(', ');

    // view variables
    let profileWidth: number;
    let expanded = true;
    let headerHover = false;

    // dispatches
    const dispatch = createEventDispatcher();

    function handlePin() {
        dispatch('message', {
            dfName
        });
    }

    function handleHeaderHover(event) {
        headerHover = event?.detail?.over;
    }

    function logAction(name: string) {
        logger.log(name, { dfName });
    }

    let baseClasses = 'grid place-items-center rounded hover:bg-gray-100 ';
</script>

<div>
    <CollapsibleCard
        bind:open={expanded}
        on:header-hover={handleHeaderHover}
        on:open={() => logAction('UI.ToggleDFOpen')}
        on:close={() => logAction('UI.ToggleDFClose')}
    >
        <div slot="header" class="dfprofile-header flex gap-1 items-center">
            <ExpanderButton rotated={expanded} />

            <div class="font-bold">
                {dfName}
            </div>

            <p class="grow">
                {formatInteger(dataframeProfile?.shape?.[0])} x {formatInteger(
                    dataframeProfile?.shape?.[1]
                )}
            </p>

            {#if isInFocus}
                <div class="focusIndicator justify-end" />
            {/if}
        </div>

        <div slot="header-no-collapse">
            <Tooltip location="right" alignment="center" distance={8}>
                <button
                    class={baseClasses +
                        (isPinned
                            ? 'text-black'
                            : headerHover
                            ? 'text-gray-400'
                            : 'text-transparent')}
                    style="width: 16px; height: 16px;"
                    on:click={handlePin}
                >
                    <Pin size="16px" />
                </button>

                <TooltipContent slot="tooltip-content">
                    {#if isPinned}
                        Unpin
                    {:else}
                        Pin
                    {/if}
                </TooltipContent>
            </Tooltip>
        </div>

        <div slot="body" class="dfprofile-body">
            <div bind:clientWidth={profileWidth} class="col-profiles">
                {#if !_.isEmpty(warningMessage)}
                    <div class="pl-2 pr-2 pb-2">
                        <span class="bg-amber-500 rounded-md p-[3px]"
                            >Warning
                        </span>
                        {warningMessage}
                    </div>
                {/if}

                {#if dataframeProfile?.shape?.[1] > 0}
                    {#each dataframeProfile?.profile as column (column.name)}
                        <ColumnProfile
                            example={column.example}
                            {dfName}
                            colName={column.name}
                            type={column.type}
                            summary={column.summary}
                            nullCount={column.nullCount}
                            containerWidth={profileWidth}
                            view={previewView}
                            totalRows={dataframeProfile?.shape?.[0]}
                            isIndex={column.isIndex}
                        />
                    {/each}
                {:else}
                    <p class="pl-8">No columns!</p>
                {/if}
            </div>
        </div>
    </CollapsibleCard>
</div>

<style global lang="postcss">
    /* TAILWIND stuff */
    @tailwind base;
    @tailwind components;
    @tailwind utilities;

    @layer base {
        h1,
        h2,
        h3,
        h4 {
            @apply font-semibold;
        }

        /* Override default from base since clashes with jupyter */
        input {
            color: black;
        }
    }

    .ͼ1 .cm-scroller {
        /* font-family: 'MD IO'; */
        font-size: 13px;
    }

    .stack-list > * + * {
        margin-top: var(--gap, 1rem);
    }

    .stack + .stack {
        margin-top: var(--gap, 1rem);
    }

    .button {
        padding: 0;
        margin: 0;
        padding: 0.5rem 1rem;
        font-weight: bold;
        background-color: black;
        color: white;
        border: none;
    }

    .small-action-button,
    .inspector-button {
        padding: 0;
        margin: 0;
        background: transparent;
        border: 1px solid transparent;
        font-size: 0.75rem;
        width: 1.5rem;
        height: 1.5rem;
        color: hsl(217, 5%, 60%);
        display: inline-grid;
        place-items: center;
    }

    .small-action-button:hover {
        background-color: hsl(217, 15%, 95%);
        cursor: pointer;
        color: black;
    }

    .small-action-button.selected {
        background-color: hsl(217, 15%, 85%);
        color: black;
    }

    .table-container {
        width: max-content;
    }

    .table-container table {
        font-size: 13px;
        text-align: right;
        hyphens: none;
        word-break: keep-all;
        min-width: 100%;
    }

    .table-container td,
    .table-container th {
        padding: 0px 0.5rem;
    }

    .table-container td {
        vertical-align: top;
        white-space: nowrap;
    }

    .table-container th {
        font-weight: 500;
        font-style: italic;
    }
    .hljs-punctuation {
        color: #bbb;
    }

    .hljs-attr {
        font-weight: 500;
    }

    .hljs-string,
    .hljs-number {
        color: hsl(217, 1%, 50%);
    }

    .gutter-indicator {
        width: 18px;
        display: grid;
        place-items: center;
        height: 18px;
    }

    .draggable:active {
        cursor: dragging;
    }

    .ͼ2 .cm-gutters {
        background-color: transparent;
        border-right: none;
    }

    .feedbackLink {
        @apply font-semibold;
        color: #616161;
    }

    .footerItem {
        @apply inline-block;
        @apply align-middle;
    }

    /* this component styles */
    .col-profiles {
        width: 100%;
    }

    .dfprofile-header {
        margin: 0;
        padding: 0.5em;
    }

    .dfprofile-body {
        display: flex;
    }

    .focusIndicator {
        height: 10px;
        width: 10px;
        background-color: #1976d2;
        border-radius: 2px;
    }
</style>
