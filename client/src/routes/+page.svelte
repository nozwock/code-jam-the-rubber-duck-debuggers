<script lang="ts">
    import Filled_button from "../ui/Filled_button.svelte";
    import Custom_Input from "../ui/Custom_Input.svelte";

    let text = "";

    function onButtonClick() {
        console.log("button clicked");
    }

    function onSubmitInput(text: string){
        console.log(text)
    }
</script>

<!--<h1>Welcome to SvelteKit</h1>-->
<!--<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>-->

<Custom_Input text={text} placeholder="PLACEHOLDER" onSubmit={onSubmitInput}/>
<Filled_button text="text" onClicked={onButtonClick}/>