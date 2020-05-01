<script>

    import {mapFromPoint, mapToPoint, mapPath, mapOpenObject} from '../store.js';
    import {serverURL} from '../constants.js'

    export let filteredLayers = [];

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

    $: filteredList = Object.keys(filteredLayers).reduce(function(r, e) {
        if (!filteredLayers[e].title.toLowerCase().indexOf(searchTerm.toLowerCase()))
            r.push(Object.assign(filteredLayers[e], {"id": e}))
        return r;
    }, [])

</script>

<div class="search_container">
    {#if $mapOpenObject}
        <div class="search_object_box">
            <div on:click={closeSelectObject} class="search_close_button"></div>
            <h1>
                {$mapOpenObject.title}</h1>
            <span>
                {$mapOpenObject.level + "-й этаж"}
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
            <p class="search_route_p">Отсюда</p>
            {#if $mapFromPoint}
                <button class="search_select_route_button">{$mapFromPoint.title}</button>
            {:else}
                <button class="search_select_route_button_inactive">Выберите место на карте</button>
            {/if}
            <p class="search_route_p">Сюда</p>
            {#if $mapToPoint}
                <button class="search_select_route_button">{$mapToPoint.title}</button>
            {:else}
                <button class="search_select_route_button_inactive">Выберите место на карте</button>
            {/if}
        {#if $mapFromPoint && $mapToPoint}
            <p>Путь займет 23 минуты</p>
        {/if}
        </div>
    {/if}

    Поиск: <input bind:value={searchTerm} />
    {#each filteredList as item}
        <p>
            {item.title}
        </p>
    {:else}
        <p>Не найдено</p>
    {/each}

</div>

<style>
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
