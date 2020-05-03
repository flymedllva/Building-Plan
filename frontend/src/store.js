import { writable } from 'svelte/store';


function mapModeCreate() {
    const { subscribe, set } = writable('view_building');

    return {
        subscribe,
        updateMode: async (newMode) => set(newMode),
    };
}

function mapFloorLevelCreate() {
    const { subscribe, set, update } = writable(null);

    return {
        subscribe,
        increment: () => update(n => n + 1),
        decrement: () => update(n => n - 1),
        updateLevel: async (level) => set(level),
    };
}


function mapChoiceFromPointCreate() {
    const { subscribe, set } = writable(null);

    return {
        subscribe,
        updatePoint: async (point) => set(point),
    };
}

function mapChoiceToPointCreate() {
    const { subscribe, set } = writable(null);

    return {
        subscribe,
        updatePoint: async (point) => set(point),
    };
}

function mapPathCreate() {
    const { subscribe, set } = writable(new Set());

    return {
        subscribe,
        updatePaths: async (paths) => set(new Set(paths)),
        deletePaths: async () => set(new Set())
    };
}

function mapOpenObjectCreate() {
    const { subscribe, set } = writable(null);

    return {
        subscribe,
        updateObject: async (newObject) => set(newObject),
        deleteObject: async () => set(null)
    };
}

function mapOpenSearchMenuCreate() {
    const { subscribe, set } = writable(false);

    return {
        subscribe,
        isOpen: async () => set(true),
        isClose: async () => set(false)
    };
}

export const mapMode = mapModeCreate();
export const mapFloorLevel = mapFloorLevelCreate();
export const mapFromPoint = mapChoiceFromPointCreate();
export const mapToPoint = mapChoiceToPointCreate();
export const mapPath = mapPathCreate();
export const mapOpenObject = mapOpenObjectCreate();
export const mapOpenSearchMenu = mapOpenSearchMenuCreate();
