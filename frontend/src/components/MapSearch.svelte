<script>

    import {slide, fade} from 'svelte/transition';
    import {mapFromPoint, mapToPoint, mapPath, mapOpenObject, mapOpenSearchMenu, mapFloorLevel, mapMode} from '../store.js';
    import {serverURL} from '../constants.js'

    export let filteredLayers = [];
    export let layers = [];

    let searchTerm = "";

    async function findPath() {
        if ($mapFromPoint && $mapToPoint) {
            const res = await fetch(serverURL + '/route' + '/building_1' + '/' + $mapFromPoint.id + '/' + $mapToPoint.id);
            await mapPath.updatePaths(await res.json());
        }
    }

    async function fromHereSelectObject() {
        await mapFromPoint.updatePoint($mapOpenObject)
        await mapOpenObject.deleteObject()
        await findPath()
    }

    async function hereSelectObject() {
        await mapToPoint.updatePoint($mapOpenObject)
        await mapOpenObject.deleteObject()
        await findPath()
    }

    async function closeSelectObject() {
        await mapOpenObject.deleteObject()
    }

    async function findSelectedObject(selectedObject) {
        searchTerm = "";
        layers.some(function(item) {
            let found = false;
            item.objects.some(function (object) {
                if (selectedObject.id === object.marker) {
                    found = true
                    mapOpenObject.updateObject(Object.assign({}, selectedObject, object, {"level": item.id}));
                    mapOpenSearchMenu.isOpen()
                    if ($mapMode === 'view_building' || $mapMode ==='view_floor') {
                        mapFloorLevel.updateLevel(item.id);
                        mapMode.updateMode('view_floor');
                    }
                }
            })
            if (found) return true
        });
    }

    $: filteredList = Object.keys(filteredLayers).reduce(function(r, e) {
        if (!filteredLayers[e].title.toLowerCase().indexOf(searchTerm.toLowerCase()))
            r.push(Object.assign(filteredLayers[e], {"id": e}))
        return r;
    }, [])


</script>

<div class="search_container">
    {#if $mapOpenObject}
        <div in:fade|local class="search_object_box">
            <div on:click={closeSelectObject} class="search_close_button"></div>
            <h1>
                {$mapOpenObject.title}</h1>
            <span>
                {"Этаж " + $mapOpenObject.level}
            </span>
            <p>
                {$mapOpenObject.description}
            </p>
            <div class="search_select_button_box">
                <button on:click={fromHereSelectObject} class="search_select_button">Отсюда</button>
                <button on:click={hereSelectObject} class="search_select_button">Сюда</button>
            </div>
            {#if $mapOpenObject.site}
                <a class="search_select_link_button" href="{'http://' + $mapOpenObject.site}">Перейти на сайт</a>
            {/if}
        </div>
    {:else}
        <div class="search_route_box">
            {#if $mapFromPoint || $mapToPoint}
                <div transition:fade|local>
                    <p class="search_route_p">Отсюда</p>
                    {#if $mapFromPoint}
                        <button class="search_select_route_button">{$mapFromPoint.title}</button>
                    {:else}
                        <button class="search_select_route_button_inactive">Выберите место</button>
                    {/if}
                </div>
                <div transition:fade|local>
                    <p class="search_route_p">Сюда</p>
                    {#if $mapToPoint}
                        <button class="search_select_route_button">{$mapToPoint.title}</button>
                    {:else}
                        <button class="search_select_route_button_inactive">Выберите место</button>
                    {/if}
                </div>
            {/if}
            <div in:fade|local>
                <p class="search_route_p">Поиск</p>
                <input class="search_button" placeholder="Магнит" bind:value={searchTerm} />
                <ul class="filter_item">
                    {#each filteredList as item}
                        <li on:click={findSelectedObject(item)}>{item.title}</li>
                    {/each}
                </ul>
            </div>
        </div>
    {/if}



</div>

<style>
    .filter_item {
        list-style-type: square;
        padding-left: 20px;
    }
    .filter_item li {
        margin-bottom: 8px;
        cursor: pointer;
    }
    .search_button {
        background-color: #515158;
        border: none;
        color: rgb(185, 185, 185);
        padding: 15px 0;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        width: 100%;
        outline:none;
    }

    .search_container {
        margin-left: 1em;
        margin-right: 1em;
    }

    .search_container h1 {
        font-size: 2.4em;
        margin-bottom: 0;
    }

    .search_route_p {
        margin-bottom: 2px;
        font-weight: 600;
        font-size: 1.2em;
    }

    .search_select_button {
        background-color: #515158;
        border: none;
        color: white;
        padding: 15px 0;
        font-size: 16px;
        cursor: pointer;
        width: 100%;
        transition: color .2s ease-out, background .2s ease-in-out;
    }

    .search_select_button:hover {
        background-color: #717171;
    }

    .search_select_link_button {
        background-color: #515158;
        border: none;
        color: white;
        padding: 15px 0;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin-top: 8px;
        cursor: pointer;
        width: 100%;
        transition: color .2s ease-out, background .2s ease-in-out;
    }

    .search_select_link_button:hover {
        background-color: #717171;
    }

    .search_select_button_box {
        display: grid;
        grid-template-columns: 50% 50%;
    }

    .search_select_route_button {
        background-color: #515158;
        border: none;
        color: white;
        padding: 15px 0;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        width: 100%;
    }

    .search_select_route_button_inactive {
        background-color: #515158;
        border: none;
        color: rgb(185, 185, 185);
        padding: 15px 0;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        width: 100%;
    }

    .search_close_button {
        position: absolute;
        right: 32px;
        top: 32px;
        width: 32px;
        height: 32px;
        opacity: 0.3;
        cursor: pointer;
    }

    .search_close_button:hover {
        opacity: 1;
    }
    .search_close_button:before, .search_close_button:after {
        position: absolute;
        left: 15px;
        content: ' ';
        height: 33px;
        width: 2px;
        background-color: #333;
    }

    .search_close_button:before {
        transform: rotate(45deg);
    }

    .search_close_button:after {
        transform: rotate(-45deg);
    }


</style>
