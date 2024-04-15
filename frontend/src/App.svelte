<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import JP_Detail from './routes/JP_Detail.svelte';

  const routes = {
    '/': Home,
    '/data_detail/:data_id': Detail,
    '/job_post_detail/:data_id': JP_Detail,
  }
</script>

<Router {routes}/>
