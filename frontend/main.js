field_to_id = {
    "nlp":1,
    "cv":2
}

search = document.querySelector('.search')
images = document.querySelectorAll('.img_section img')


search.addEventListener('change', (event)=>{
    images.forEach(element => {
        element.classList.toggle('deactivate', true)
    });

    if (search.value == 'cv'){
        active_id = field_to_id["cv"]
        images[active_id].classList.toggle('deactivate', false)
    }

    else if(search.value == 'nlp'){
        active_id = field_to_id["nlp"]
        images[active_id].classList.toggle('deactivate', false)
    }
})

