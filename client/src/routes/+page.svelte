<script>
    import Filled_button from "../ui/Filled_button.svelte";

    function onButtonClick() {
        console.log("button clicked")
    }
</script>

<!--<h1>Welcome to SvelteKit</h1>-->
<!--<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>-->
<Filled_button text="text" onClicked={onButtonClick}/>