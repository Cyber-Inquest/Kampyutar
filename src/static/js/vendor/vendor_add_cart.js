function _quantity_vendor(ids, categories){
    final_ids = '_quantity_vendor_cart' + ids
    console.log(categories)
    console.log(ids)
    var quantity_value = document.getElementById(final_ids).value;
    console.log(quantity_value)

    updateVendorCart(ids, categories, quantity_value)
}

function vendorcartadd(product, producttype, product_item){
    console.log(product, producttype, product_item)
    var final_ids = '_vendor_quantity_id' + product_item
    console.log(final_ids)
    var element_value = document.getElementById(final_ids).value;
    console.log(element_value)

    updateVendorOrder(product, producttype, element_value)

}

function vendorcartdelete(product, producttype){
    DeleteVendorOrder(product, producttype)

}

function updateVendorOrder(productId, producttype, element_value){
    var url = '/vendor/update_cart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId, 'producttype':producttype , 'action': 'add', 'quantity':element_value})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True'){
            $("#vendor_append").load(" #vendor_append > *");
            toastr.success('Add to Cart!')
        }

    })
}

function DeleteVendorOrder(productId, producttype){
    var url = '/vendor/update_cart/'

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
            $("#_cart_list").load(" #_cart_list > *");
            $("#vendor_append").load(" #vendor_append > *");
            $("#_cart_heading").load(" #_cart_heading > *");
            toastr.success('Item deleted!')
        }

    })
}

function updateVendorCart(productId, producttype, element_value){
    var url = '/vendor/update_cart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId, 'producttype':producttype , 'action': 'update', 'quantity':element_value})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True'){
            $("#vendor_append").load(" #vendor_append > *");
            $("#_cart_heading").load(" #_cart_heading > *");
            toastr.success('Add to Cart!')
        }

    })
}