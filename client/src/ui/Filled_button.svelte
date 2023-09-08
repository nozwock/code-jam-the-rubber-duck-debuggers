<script lang="ts">
   export let text: string;
   export let onClicked: () => void;
</script>

<style>
   .filledButton {
      background-color: #1c92ff;
      border-radius: 15px;
      padding: 15px;
      color: white;
      font-size: 18px;
      font-weight: bold;
      border: none;
   }
</style>

<button class="filledButton" on:click={onClicked}>
   {text}
</button>


