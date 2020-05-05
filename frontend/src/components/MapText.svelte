<script>

    import { fade } from 'svelte/transition';

    export let item;
    export let marker;

</script>

<text in:fade="{{ delay: 920, duration: 400 }}" out:fade="{{ delay: 0, duration: 150 }}"
      x={item.x + 20}
      y={item.y + (item.height / 2) + 6}
      class="text">
    {marker.title}
</text>

<style>
    .text {
        font: bold 2em sans-serif;
        user-select: none;
    }
</style>
