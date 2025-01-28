<script lang="ts">
  // - ui - //
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
	import Button from '$lib/components/ui/button/button.svelte';

  // - form data - //
  let imageFile: File | null = null;
  let detectedObjects: any[] = [];
  let imageBase64 = '';
  let wastePercentage = 0;
  let wastePercentageColor = '';

  // - functions - //
  async function handleSubmit(event: Event) {
    event.preventDefault();
    if (!imageFile) return;

    const formData = new FormData();
    formData.append('file', imageFile);

    const response = await fetch('http://127.0.0.1:8000/api/detect', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    detectedObjects = data.objects;
    imageBase64 = data.image_base64;
    wastePercentage = data.waste_percentage;

    if(wastePercentage < 10) {
      wastePercentageColor = 'green';
    } else if(wastePercentage < 20) {
      wastePercentageColor = 'yellow';
    } else {
      wastePercentageColor = 'red';
    }
  }
</script>

<div class="w-screen h-screen bg-zinc-900 flex justify-center items-center flex-col text-zinc-200 antialiased">
  <h1 class="text-4xl">PROJETO III - JR3 FWD</h1>
  <!-- Form -->
  <form on:submit={handleSubmit} class="flex flex-row items-end gap-2 mt-4">
    <div class="grid w-full max-w-sm items-center gap-1.5">
      <Label for="image">Imagem</Label>
      <Input id="image" type="file" accept="image/*" on:change={(e) => imageFile = e.target.files[0]} class="text-zinc-900" />
    </div>
    <Button type="submit" variant="secondary">Detetar</Button>
  </form>
  
  <!-- Resultados -->
  <div class="flex flex-row gap-3 justify-center items-center w-full mt-4 px-8"> 
    <!-- Objetos -->
    <div class="left">
      {#if detectedObjects.length > 0}
        <h2 class="font-bold">Objetos detetados</h2>
        <code>
          {#each detectedObjects as obj}
            {obj.label} - {obj.confidence.toFixed(2)}<br/>
          {/each}
        </code>

        <h2 class="font-bold">Desperdício (%)</h2>
        <p class={wastePercentageColor}>{wastePercentage.toFixed(2)}%</p>
      {/if}

      
    </div>

    <!-- Imagem -->
    <div class="w-[23rem] h-[23rem]">
      {#if imageBase64}
        <img src={`data:image/jpeg;base64,${imageBase64}`} alt="Detected Image" />
      {/if}
    </div>
  </div> 
</div>
