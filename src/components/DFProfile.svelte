<script lang="ts">
    import _ from 'lodash';
    import type { IDFProfileWState } from '../common/exchangeInterfaces';
    import ColumnProfile from './ColumnProfile.svelte';
    import { formatInteger } from './utils/formatters';

    export let dfName: string;
    export let dataframeProfile: IDFProfileWState;
    export let isInFocus = false; // not used in inline profiler but needed for consistency
    export let isPinned = false;

    // locals
    let previewView = 'summaries';
    $: warningMessage = _.isEmpty(dataframeProfile.warnings)
        ? ''
        : dataframeProfile.warnings.map(w => w.warnMsg).join(', ');

    // view variables
    let profileWidth = 750;

    /**
     * Svelte container binding not working on initial load (sets to 0), but works on window resize or any re-re-render
     *  so we default to the max width until a resize
     * @param inputWidth the width of the container
     */
    function binWidth(inputWidth: number) {
        if (inputWidth <= 0) {
            return 750;
        }

        return inputWidth;
    }
</script>

<div class="inlineprofiler-base-wrapper">
    <div class="dfprofile-header flex gap-1 items-center">
        <div class="font-bold">
            {dfName}
        </div>

        <p class="grow">
            {formatInteger(dataframeProfile?.shape?.[0])} x {formatInteger(
                dataframeProfile?.shape?.[1]
            )}
        </p>
    </div>

    <div class="dfprofile-body" bind:clientWidth={profileWidth}>
        <div class="col-profiles">
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
                        containerWidth={binWidth(profileWidth)}
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

    .focusIndicator {
        height: 10px;
        width: 10px;
        background-color: #1976d2;
        border-radius: 2px;
    }

    .inlineprofiler-base-wrapper {
        max-width: 750px;
    }
</style>
