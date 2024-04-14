<script>
    import fastapi from "../lib/api"

    export let params = {}
    let data_id = params.data_id
    let detail = {}

    function get_detail() {
        fastapi("get", "/api/data/data_detail/" + data_id, {}, (json) => {
            detail = json
        })
    }

    get_detail()
</script>

<h1>{detail.company}</h1>
<div>
    {detail.title}<br>
    {detail.options}<br>
    {detail.techs}<br>
    {detail.link}
</div>
