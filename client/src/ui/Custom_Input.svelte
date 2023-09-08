<script lang="ts">
    type OnSubmitFunction= (text: string) => void

    export let text: string;
    export let placeholder: string;
    export let onSubmit:OnSubmitFunction = (text: string)=>null;
    
    function onKeyDown(e:KeyboardEvent) {
        if (e.key == "Enter"){
            onSubmit(text)
        }
    }
</script>

<style>
    .input{
        border-radius: 10px;
        padding: 15px;
        font-size: 16px;
    }
</style>

<input class="input" bind:value={text} placeholder={placeholder} on:keydown={onKeyDown}/>