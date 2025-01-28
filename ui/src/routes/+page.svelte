<script lang="ts">
  import { onMount } from 'svelte';
  let imageFile: File | null = null;
  let detectedObjects: any[] = [];
  let imageBase64 = '';

  async function handleSubmit(event: Event) {
    event.preventDefault();
    if (!imageFile) return;

    const formData = new FormData();
    formData.append('file', imageFile);

    const response = await fetch('/api/detect', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    detectedObjects = data.objects;
    imageBase64 = data.image_base64;
  }
</script>

<h1>Upload an Image for Detection</h1>
<form on:submit={handleSubmit}>
  <input type="file" accept="image/*" on:change={(e) => imageFile = e.target.files[0]} />
  <button type="submit">Upload</button>
</form>

{#if detectedObjects.length > 0}
  <h2>Detected Objects</h2>
  <ul>
    {#each detectedObjects as obj}
      <li>{obj.label} - {obj.confidence.toFixed(2)}</li>
    {/each}
  </ul>
{/if}

{#if imageBase64}
  <h2>Image with Detections</h2>
  <!-- svelte-ignore a11y_img_redundant_alt -->
  <img src={`data:image/jpeg;base64,${imageBase64}`} alt="Detected Image" />
{/if}