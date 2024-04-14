<script>
    import fastapi from '../lib/api';
    import { onMount } from 'svelte';
    import { link } from 'svelte-spa-router'
    
  
    let dataList = [];
    let endpoint = "jobkorea_list"; // Default endpoint
  
    function fetchData(endpoint) {
      return fetch(`http://127.0.0.1:8000/api/data/${endpoint}`)
        .then(response => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .catch(error => {
          console.error(`Error fetching ${endpoint} data:`, error);
          return [];
        });
    }
  
    onMount(async () => {
      dataList = await fetchData(endpoint);
    });
  
    function switchEndpoint(newEndpoint) {
      endpoint = newEndpoint;
      fetchData(newEndpoint).then(data => {
        dataList = data;
      });
    }
  </script>
  
  <select bind:value={endpoint} on:change={() => switchEndpoint(endpoint)}>
    <option value="jobkorea_list">Job Korea</option>
    <option value="saramin_list">Saramin</option>
  </select>
  
  <ul>
    {#each dataList as data}
      <li><a use:link href="/data_detail/{endpoint}_{data.id}">{data.company}</a></li>
    {/each}
  </ul>
  