<script>
	import Map from "./components/Map.svelte"
	import {serverURL} from "./constants"

	let mapURL = serverURL + '/building_1'

</script>

<Map mapURL="{mapURL}"/>

<style>

	:global(*),
	:global(*::after),
	:global(*::before) {
		-webkit-box-sizing: border-box;
		box-sizing: border-box;
	}

	:global(body) {
		font-family: 'Avenir Next', Avenir, 'Helvetica Neue', Helvetica, Arial, sans-serif;
		color: #515158;
		background: #f0f0f0;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		margin: 0;
	}

	:global(a) {
		text-decoration: none;
		color: #aaa;
		outline: none;
		transition:.5s;
	}

	:global(a:hover),
	:global(button:hover) {
		color: #515158;
		outline: none;
	}

	:global(a:focus),
	:global(button:focus) {
		outline: none;
	}

</style>
