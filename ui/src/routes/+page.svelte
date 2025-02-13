<script lang="ts">
  // - ui - //
  import Button from '$lib/components/ui/button/button.svelte';
  import { Input } from "$lib/components/ui/input/index.js";
  import { Label } from "$lib/components/ui/label/index.js";
  import { Checkbox } from "$lib/components/ui/checkbox/index.js";
  import { Toaster } from "$lib/components/ui/sonner";
  import { toast } from "svelte-sonner";
  import spinner from '$lib/assets/image/loading.svg';
  import { onMount } from 'svelte';
  import * as Tabs from "$lib/components/ui/tabs";
  import { Math } from 'mathjax-svelte';

  // - form data - //
  let imageFile: File | null = null;
  let detectedObjects: any[] = [];
  let imageBase64 = '';
  let clusteringImageBase64 = '';
  let wastePercentage = 0;
  let wastePercentageColor = '';
  let food_area = 0;
  let plate_area = 0;
  let garbage_area = 0;
  let isLoading = false;
  let currentCommit = 'loading...';

  async function getCommitHash() {
    const response = await fetch('https://api.github.com/repos/Xurape/PROJ3-FWD/commits');
    const data = await response.json();
    return data[0].sha;
  }

  // to use later
  //onMount(async () => {
    //currentCommit = await getCommitHash();
  //});

  // - functions - //
  async function handleSubmit(event: Event) {
    event.preventDefault();
    if (!imageFile) return;

    isLoading = true;
    const formData = new FormData();
    formData.append('file', imageFile);

    toast.loading('Processing image...');

    const response = await fetch(`https://jr3-api.joaopferreira.me/api/detect`, {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    if (response.status !== 200) {
      detectedObjects = [];
      imageBase64 = '';
      clusteringImageBase64 = '';
      wastePercentage = 0;
      food_area = 0;
      plate_area = 0;
      garbage_area = 0;

      toast.error(data.error || 'An error occurred while processing the image.');
      isLoading = false;
      return;
    }

    detectedObjects = data.objects;
    imageBase64 = data.image_base64;
    clusteringImageBase64 = data.clustering_image_base64;
    wastePercentage = data.waste_percentage;
    food_area = data.food_area;
    plate_area = data.plate_area;
    garbage_area = data.garbage_area;

    if(wastePercentage < 10) {
      wastePercentageColor = 'green';
    } else if(wastePercentage < 20) {
      wastePercentageColor = 'yellow';
    } else {
      wastePercentageColor = 'red';
    }

    toast.success('The image was successfully processed!');
    isLoading = false;
  }

  // - math - //
  $: formula = `W = \\frac{\\text{FoodArea}}{\\text{PlateArea} - \\text{GarbageArea}} \\times 100`;
  $: currentFormula = food_area && plate_area
    ? `W = \\frac{${food_area.toFixed(2)}}{${plate_area.toFixed(2)} - ${garbage_area.toFixed(2)}} \\times 100`
    : formula;
  $: combinedFormula = food_area && plate_area 
    ? `W = \\frac{\\text{FoodArea}}{\\text{PlateArea} - \\text{GarbageArea}} \\times 100 = \\frac{${food_area.toFixed(2)}}{${plate_area.toFixed(2)} - ${garbage_area.toFixed(2)}} \\times 100 = ${wastePercentage.toFixed(2)}`
    : formula;
</script>

<Toaster richColors />

<div class="w-screen h-[100vh] bg-zinc-900 flex justify-center items-center flex-col text-zinc-200 antialiased px-8 md:px-48">
  <h1 class="text-4xl text-center mt-10">Food Waste Detection in Canteen Plates</h1>
  <!-- Form -->
  <form on:submit={handleSubmit} class="flex flex-row items-end gap-2 mt-4">
    <div class="grid w-full max-w-sm items-center gap-1.5">
      <Label for="image">Image (.jpg, .jpeg, .png)</Label>
      <Input id="image" type="file" accept="image/*" on:change={(e) => imageFile = e.target.files[0]} class="text-zinc-900" />
    </div>
    <Button type="submit" variant="secondary">Detect</Button>
  </form>
  
  <!-- Resultados -->
  <div class="flex w-full h-full mt-2">
    <Tabs.Root value="calculations" class="w-full flex flex-col justify-top">
      <Tabs.List class="w-full">
          <Tabs.Trigger value="prediction" class="w-full">Prediction</Tabs.Trigger>
          <Tabs.Trigger value="calculations" class="w-full">Calculations</Tabs.Trigger>
      </Tabs.List>
      <Tabs.Content value="prediction" class="w-full md:w-full">
        <div class="flex flex-col md:flex-row gap-4 md:gap-24 justify-center items-center px-8 w-full !mx-4 md:h-[35rem]"> 
          {#if isLoading}
            <img src={spinner} class="w-64 h-64" />
          {:else}
            <!-- Objetos -->  
            <div class="left">
              {#if detectedObjects.length > 0}
                <h2 class="font-bold hidden md:block">Detected objects</h2>
                <code class="hidden md:block"> 
                  {#each detectedObjects as obj}
                    {obj.label_name} - {obj.confidence.toFixed(2)}<span class="text-gray-500 text-xs">*</span><br/>
                  {/each}
                </code>
                <p class="text-gray-500 text-xs">* - Precision</p>
      
                <h2 class="font-bold mt-3">Waste (%)</h2>
                <p class={wastePercentageColor}>{wastePercentage.toFixed(2)}%</p>
              {/if} 
            </div>
      
            <!-- Imagem -->
            <div class="mb-4 flex flex-col md:flex-row gap-2">
              {#if imageBase64}
                <div class="flex flex-col gap-2">
                  <h2 class="font-bold hidden md:block">Detected Image</h2>
                  <img src={`data:image/jpeg;base64,${imageBase64}`} alt="Detected Image" class="w-[23rem] h-[30rem]"/>
                </div>
              {/if}
              {#if clusteringImageBase64}
                <div class="flex flex-col gap-2">
                  <h2 class="font-bold hidden md:block">Clustering Image</h2>
                  <img src={`data:image/jpeg;base64,${clusteringImageBase64}`} alt="Clustering Image" class="w-[23rem] h-[30rem]"/>
                </div>
              {/if}
            </div>
          {/if}
        </div> 
      </Tabs.Content>
      <Tabs.Content value="calculations" class="w-full md:w-full">
        <div class="flex flex-col gap-4 justify-top items-start px-8 mt-8 w-full !mx-4 md:h-[35rem]"> 
          <p class="text-gray-200"><span class="text-red-700">Considerations:</span></p>
          <ul>
            <li>- The waste (%) is the area of the objects (food) except the utensils and the garbage.</li>
            <li>- The waste (%) is 100% when the plate has the max amount of food.</li>
            <li>- Garbage is qualified as a type of food or object that cannot be eaten.</li>
            <li>- Every variable on the formula is calculated in Pixels</li>
          </ul>
          <p class="text-gray-200"><span class="text-red-700">Formula:</span></p>
          <div class="flex flex-row gap-5">
            <Math t={formula} />
          </div>
          {#if food_area && plate_area}
            <p class="text-gray-200"><span class="text-red-700">Formula used to determine current Waste (%):</span></p>
            <Math t={combinedFormula} />
          {/if}
        </div>
      </Tabs.Content>
    </Tabs.Root>
  </div>

  <div id="footer" class="absolute flex flex-col gap-1 bottom-6 md:bottom-5 w-full text-center text-xs text-gray-500">
    <p class="text-gray-200"><span class="text-red-700">NOTE:</span> Considering the waste (%) as the area of the objects (food) except the utensils and the garbage. The waste (%) is 100% when the plate have the max amount of food.<br/>
    Garbage is qualified as a type of food or object that cannot be eaten.</p>
    <!--
    <p>current git commit: <a href={"https://github.com/xurape/PROJ3-FWD/commit/" + currentCommit} target="_blank" rel="nofollow" class="text-yellow-600 underline">{currentCommit}</a></p>
    -->
  </div>
</div>
