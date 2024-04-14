<script>
    import fastapi from "../lib/api"
    let field_anal_list = []

    function get_field_anal_list() {
        fastapi('get', '/api/data/field_anal', {}, (json) => {
            field_anal_list = json
        })
    }

    get_field_anal_list()
</script>

<ul>
    {#each field_anal_list as field}
        <li>{field.field}<br>{field.count}</li>
    {/each}
</ul>