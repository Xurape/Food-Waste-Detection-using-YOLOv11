<script lang="ts">
  // - ui - //
	import Button from '$lib/components/ui/button/button.svelte';
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Toaster } from "$lib/components/ui/sonner";
	import { toast } from "svelte-sonner";
  import spinner from '$lib/assets/image/loading.svg';

  // - form data - //
  let imageFile: File | null = null;
  let detectedObjects: any[] = [];
  let imageBase64 = '';
  let wastePercentage = 0;
  let wastePercentageColor = '';
  let isLoading = false;

  // - functions - //
  async function handleSubmit(event: Event) {
    event.preventDefault();
    if (!imageFile) return;

    const formData = new FormData();
    formData.append('file', imageFile);

    toast.loading('Processing image...');
    isLoading = true;

    const response = await fetch('https://jr3-api.joaopferreira.me/api/detect', {
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

    toast.success('The image was successfuly processed!');
    isLoading = false;
  }
</script>

<Toaster richColors />

<div class="w-screen h-screen bg-zinc-900 flex justify-center items-center flex-col text-zinc-200 antialiased">
  <h1 class="text-4xl">PROJECT III - Food waste detection in canteen plates</h1>
  <!-- Form -->
  <form on:submit={handleSubmit} class="flex flex-row items-end gap-2 mt-4">
    <div class="grid w-full max-w-sm items-center gap-1.5">
      <Label for="image">Image</Label>
      <Input id="image" type="file" accept="image/*" on:change={(e) => imageFile = e.target.files[0]} class="text-zinc-900" />
    </div>
    <Button type="submit" variant="secondary">Detect</Button>
  </form>
  
  <!-- Resultados -->
  <div class="flex flex-row gap-24 justify-center items-center mt-8 px-8 border border-dashed border-zinc-500 rounded-xl w-[calc(100%-40rem)] h-[35rem]"> 
    {#if isLoading}
      <img src={spinner} class="w-64 h-64" />
    {:else}
      <!-- Objetos -->  
      <div class="left">
        {#if detectedObjects.length > 0}
          <h2 class="font-bold">Detected objects</h2>
          <code>
            {#each detectedObjects as obj}
              {obj.label} - {obj.confidence.toFixed(2)}<br/>
            {/each}
          </code>

          <h2 class="font-bold mt-3">Waste (%)</h2>
          <p class={wastePercentageColor}>{wastePercentage.toFixed(2)}%</p>
        {/if} 
      </div>

      <!-- Imagem -->
      <div class="w-[23rem] h-[30rem]">
        {#if imageBase64}
          <img src={`data:image/jpeg;base64,${imageBase64}`} alt="Detected Image" />
        {/if}
      </div>
    {/if}
  </div> 
</div>
