<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
    import Field from './routes/Field.svelte';

  const routes = {
    '/': Home,
    '/data_detail/:data_id': Detail,
    '/field_anal': Field,
  }
</script>

<Router {routes}/>
