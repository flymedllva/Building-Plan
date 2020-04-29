<script>

    import {mapMode, mapFloorLevel, mapPath, mapOpenObject, mapOpenSearchMenu} from '../store.js';
    import {flyAnimation} from '../animation'

    import MapText from "./MapText.svelte";

    export let level;
    export let layer;

    async function selectLayer() {
        if ($mapMode === 'view_building') {
            await mapFloorLevel.updateLevel(level);
            await mapMode.updateMode('view_floor');
        }
    }

    async function selectObject(object) {
        if ($mapMode  === 'view_floor') {
            await mapOpenObject.updateObject(
                    Object.assign(object, layer.markers[object.marker], {"level": level})
            );
            await mapOpenSearchMenu.isOpen()
        }
    }

</script>

<div on:click={selectLayer} in:flyAnimation={{ z: 1000, duration: 600, level: level }}
     class="level"
     style="{'transform: translateZ(' + (level * 10 - 10) +'vmin);'}
           {$mapMode === 'view_floor' ? $mapFloorLevel === level ? 'transform: translateZ(15vmin) rotate3d(0,0,1,20deg)'
           : level > $mapFloorLevel ? 'transform: translateZ(' + (level * 10 * 2.5) + 'vmin); opacity: 0;'
           : level < $mapFloorLevel ? 'transform: translateZ(' + -(level * 10 * 2.5) + 'vmin); opacity: 0;'
           : '' : ''}">
    <svg viewBox="0 0 1200 800" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
        {#each layer.objects as item}
            {#if item.type === 'polygon'}
                <polygon points="{item.points}" class="map__ground {item.id}" />
            {:else if item.type === 'rect'}
                <rect on:click={selectObject(item)} x={item.x} y={item.y} width={item.width} height={item.height} class="map__space {item.id}"/>
                {#if $mapMode === 'view_floor' && item.marker}
                    <MapText item="{item}" marker="{layer.markers[item.marker]}"/>
                {/if}
            {:else if item.type === 'ellipse'}
                <ellipse cx={item.cx} cy={item.cy} rx={item.rx} ry={item.ry} class="map__tree {item.id}" />
            {:else if item.type === 'path'}
                <path d="{item.d}" class="map__space {item.id}" />
            {:else if item.type === 'line'}
                <line class="line--active" x1={item.x1} y1={item.y1} x2={item.x2} y2={item.y2} stroke-width="8" />
            {/if}
        {/each}
        {#each layer.routes as item}
            {#if item.type === 'line' && $mapPath.has(item.id)}
                <line class="line {item.id}" x1={item.x1} x2={item.x2} y1={item.y1} y2={item.y2} stroke-width="8" />
            {/if}
        {/each}
        {#each layer.intermediates as item}
            {#if $mapMode === 'view_floor' && item.type === 'entrance'}
                <line class="map_entrance {item.id}" x1={item.x1} y1={item.y1} x2={item.x2} y2={item.y2} stroke-width="6" />
<!--            {:else if item.type === 'point'}-->
<!--                <circle class="{item.id}" cx={item.cx} cy={item.cy} r=6 fill="red"/>-->
            {/if}
        {/each}

    </svg>
</div>

<style>

    /* Levels map */

    .level {
        position: relative;
        width: 100%;
        height: 100%;
        cursor: pointer;
        pointer-events: auto;
        -webkit-transition: opacity 1s, -webkit-transform 1s;
        transition: opacity 1s, transform 1s;
        -webkit-transition-timing-function: cubic-bezier(0.7, 0, 0.3, 1);
        transition-timing-function: cubic-bezier(0.7, 0, 0.3, 1);
        -webkit-transform-style: preserve-3d;
        transform-style: preserve-3d;
    }

    .level::after {
        font-size: 2.5vmin;
        line-height: 0;
        position: absolute;
        z-index: 100;
        top: -2em;
        left: 3.5em;
        white-space: nowrap;
        color: #7d7d86;
        -webkit-transform: rotateZ(45deg) rotateX(-70deg) translateZ(5vmin);
        transform: rotateZ(45deg) rotateX(-70deg) translateZ(5vmin);
        -webkit-transition: -webkit-transform 1s, color 0.3s;
        transition: transform 1s, color 0.3s;
        -webkit-transition-timing-function: cubic-bezier(0.7, 0, 0.3, 1);
        transition-timing-function: cubic-bezier(0.7, 0, 0.3, 1);
    }


    .level:not(:first-child) {
        position: absolute;
        top: 0;
        left: 0;
    }

    /* Level map */

    .map_entrance {
        stroke: #626262;
    }

    .map__outline {
        -webkit-transition: fill 0.3s;
        transition: fill 0.3s;
        fill: #bbb;
    }

    .map__space {
        -webkit-transition: fill-opacity 0.8s;
        transition: fill-opacity 0.8s;
        fill: #bdbdbd;
        fill-opacity: 0.6;
    }

    .map__ground {
        fill: #d7d7dc;
    }


    /* Lines */

    .line {
        stroke: black;
    }

</style>
