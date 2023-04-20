var updataBtns = document.getElementsByClassName('bb_item_addToCart_btn');
var addtocart = document.getElementsByClassName('_add_to_cart_btn');
var removeCartBtns = document.getElementsByClassName('_remove_cart_btn');


for (i=0; i < updataBtns.length; i++){
    updataBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        if (user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

for (i=0; i < addtocart.length; i++){
    addtocart[i].addEventListener('click', function(){
        var productId = this.dataset.perproduct;
        var action = this.dataset.peraction;
        var quantity_value = document.getElementById('_quantity_per_page').value;

        if (user == 'AnonymousUser'){
            addCookieItems(productId, action, quantity_value)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

for (i=0; i < removeCartBtns.length; i++){
    removeCartBtns[i].addEventListener('click', function(){
        var productId = this.dataset.rdeletion;
        var action = this.dataset.raction;

        if (user == 'AnonymousUser'){
            deleteCookieItem(productId,action)
        }else{
            delete_cartlist(productId, )
        }
    })
}

function delete_cartlist(productId){
    var url = '/update_cartlist/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True')
            $("#_cart_list").load(" #_cart_list > *");
            location.reload();
    })
}

function addCookieItem(productId, action){

    if(action == 'add'){

        if(cart == undefined){
            cart = {}
            cart[productId] = {'quantity': 1}
            toastr.success('Add to Cart!')
        }else{
            if (cart[productId] == undefined){
                cart[productId] = {'quantity': 1}
                toastr.success('Add to Cart!')
            }else{

                var caer_quantity = cart[productId]['quantity']
                var quantity = parseInt(caer_quantity) + 1
                cart[productId]['quantity']  = quantity
                toastr.success('Add to Cart!')
            }

        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    $("#append_here").load(" #append_here > *")
}


function addCookieItems(productId, action, quantity){

    if(action == 'add'){

        if(cart == undefined){
            cart = {}
            cart[productId] = {'quantity': quantity}
            toastr.success('Add to Cart!')
        }else{
            if (cart[productId] == undefined){

                cart[productId] = {'quantity': quantity}
                toastr.success('Add to Cart!')
            }else{

                var caer_quantity = cart[productId]['quantity']
                var quantity = parseInt(caer_quantity) + parseInt(quantity)
                cart[productId]['quantity'] = quantity
                toastr.success('Add to Cart!')
            }

        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    $("#append_here").load(" #append_here > *")
}

function deleteCookieItem(productId, action){

    if(action == 'delete'){
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0 ){

            delete cart[productId]
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload();

}


function updateUserOrder(productId, action){

    var url = '/updateCart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True'){
            $("#append_here").load(" #append_here > *");
            toastr.success('Add to Cart!')
        }

    })
}

function updateUserOrderDatabase(productId){
    var cart_quantity = document.getElementById('_quantity_per_pagess').value;
    var url = '/updateCart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId, 'action':'details_cart_button_update', 'quantity':cart_quantity})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True'){
            $("#append_here").load(" #append_here > *");
            toastr.success('Add to Cart!')
        }

    })
}
