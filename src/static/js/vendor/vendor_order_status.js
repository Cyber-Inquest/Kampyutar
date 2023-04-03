function vendor_eachorder_status(order_id, order_status){
     var url = '/admin_vendor/order_status/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'order_id':order_id, 'order_status':order_status})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True'){
            $("#admin_customers").load(" #admin_customers > *");
            toastr.success('Order Updated!')
        }

    })
}

function vendor_eachorder_delete(order_id, product_type, user_id){
     var url = '/admin_vendor/del_order/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'order_id':order_id, 'product_type':product_type, 'user_id': user_id})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True'){
            $("#admin_customers").load(" #admin_customers > *");
            toastr.success('Order Updated!')
        }

    })
}