

var delprodBtns = document.getElementsByClassName('fas fa-trash-alt');

for (i=0; i < delprodBtns.length; i++){
    delprodBtns[i].addEventListener('click', function(){
        var productId = this.dataset.allproduct;
        var percategories = this.dataset.categories;
        console.log('productId:',productId, 'percategories:',percategories)

        delete_product(productId, percategories)

    })
}

function delete_product(productId, producttype){
    var url = '/admin_django/del_product/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId, 'producttype':producttype})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True')

            location.reload();
            toastr.success('Product Deleted!')


    })
}
