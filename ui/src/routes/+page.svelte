<script lang="ts">
  // - ui - //
	import Button from '$lib/components/ui/button/button.svelte';
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Checkbox } from "$lib/components/ui/checkbox/index.js";
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
  let currentCommit = getCommitHash() || 'loading...';

  async function getCommitHash() {
    const response = await fetch('https://api.github.com/repos/Xurape/PROJ3-FWD/commits');
    const data = await response.json();
    return data[0].sha;
  }

  // - functions - //
  async function handleSubmit(event: Event) {
    event.preventDefault();
    if (!imageFile) return;

    isLoading = true;
    const formData = new FormData();
    formData.append('file', imageFile);

    toast.loading('Processing image...');

    // const response = await fetch(`https://jr3-api.joaopferreira.me/api/detect`, {
    const response = await fetch(`http://localhost:8000/api/detect`, {
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

<div class="w-screen h-[100vh] bg-zinc-900 flex justify-center items-center flex-col text-zinc-200 antialiased px-8 md:px-48">
  <h1 class="text-4xl text-center">Food Waste Detection in Canteen Plates</h1>
  <!-- Form -->
  <form on:submit={handleSubmit} class="flex flex-row items-end gap-2 mt-4">
    <div class="grid w-full max-w-sm items-center gap-1.5">
      <Label for="image">Image (.jpg, .jpeg, .png)</Label>
      <Input id="image" type="file" accept="image/*" on:change={(e) => imageFile = e.target.files[0]} class="text-zinc-900" />
    </div>
    <Button type="submit" variant="secondary">Detect</Button>
  </form>
  
  <!-- Resultados -->
  <div class="flex flex-col md:flex-row gap-4 md:gap-24 justify-center items-center mt-8 px-8 border border-dashed border-zinc-500 rounded-xl w-full !mx-4 md:h-[35rem]"> 
    {#if isLoading}
      <img src={spinner} class="w-64 h-64" />
    {:else}
      <!-- Objetos -->  
      <div class="left">
        {#if detectedObjects.length > 0}
          <h2 class="font-bold hidden md:block">Detected objects</h2>
          <code class="hidden md:block"> 
            {#each detectedObjects as obj}
              {obj.label} - {obj.confidence.toFixed(2)}<br/>
            {/each}
          </code>

          <h2 class="font-bold mt-3">Waste (%)</h2>
          <p class={wastePercentageColor}>{wastePercentage.toFixed(2)}%</p>
        {/if} 
      </div>

      <!-- Imagem -->
      <div class="md:w-[23rem] md:h-[30rem] mb-4">
        {#if imageBase64}
          <img src={`data:image/jpeg;base64,${imageBase64}`} alt="Detected Image" class="w-[23rem] h-[30rem]"/>
        {/if}
      </div>
    {/if}
  </div> 

  <div id="footer" class="absolute bottom-7 md:bottom-5 w-full text-center text-xs text-gray-500">
    <p>current git commit: <a href={"https://github.com/xurape/PROJ3-FWD/commit/" + currentCommit} target="_blank" rel="nofollow" class="text-yellow-600 underline">{currentCommit}</a></p>
  </div>
</div>
