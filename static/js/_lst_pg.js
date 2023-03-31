function updatecategory(categoryId){
    var url = '/updateCart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':categoryId})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        $("#_append_here").load(" #append_here > *");
    })
}
