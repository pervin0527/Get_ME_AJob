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
        

        fetch(`http://127.0.0.1:8000/api/data/field_detail/${data_id}`).then((response) => {
            response.json().then((json) => {
                detail = json
            })
        })

    }

    get_detail()
</script>

<h1>{detail.field}</h1>
<div>
    {detail.cnt}<br>
    {detail.related}
    <!-- {detail.skill}<br> db에 skill값을 저장하게 되면 해당 값을 불러온다. -->
</div>
