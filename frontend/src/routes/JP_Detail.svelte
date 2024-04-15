<!-- 각 분야에 대한 상세 정보를 보여주는 페이지-->

<script>
    import fastapi from "../lib/api"

    export let params = {}
    let data_id = params.data_id
    let detail = {}

    function get_detail() {        
        //fastapi("get", "/api/data/data_detail/" + data_id, {}, (json) => {
            //detail = json
        //})
        
        fetch(`http://127.0.0.1:8000/api/data/job_post_detail/${data_id}`).then((response) => {
            response.json().then((json) => {
                detail = json
            })
        })

    }

    get_detail()
</script>

<h1>{detail.main_field}</h1>
<div>
    {detail.num_posts}<br>
    {detail.related_field}
</div>
