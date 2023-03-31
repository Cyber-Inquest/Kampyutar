function _vendor_del_order(ids, producttype){

    updateVendorOrder(ids, producttype)
}

function updateVendorOrder(productId, producttype){
    var url = '/vendor/update_order/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId, 'producttype':producttype , 'action': 'delete'})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True'){
            $("#order").load(" #order > *");
            toastr.success('Order Update!')
        }else{
            toastr.warning('Order cannot be updated!')
        }

    })
}