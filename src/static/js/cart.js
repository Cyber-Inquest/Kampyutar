var updataBtns = document.getElementsByClassName('bb_item_addToCart_btn');
var addtocart = document.getElementsByClassName('_add_to_cart_btn');
var removeCartBtns = document.getElementsByClassName('_remove_cart_btn');


for (i=0; i < updataBtns.length; i++){
    updataBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var producttype = this.dataset.producttype;
        if (user == 'AnonymousUser'){
            addCookieItem(productId, producttype, action)
        }else{
            updateUserOrder(productId, producttype, action)
        }
    })
}

for (i=0; i < addtocart.length; i++){
    addtocart[i].addEventListener('click', function(){
        var productId = this.dataset.perproduct;
        var action = this.dataset.peraction;
        var producttype = this.dataset.perproducttype;
        var quantity_value = document.getElementById('_quantity_per_page').value;

        if (user == 'AnonymousUser'){
            addCookieItems(productId, producttype, action, quantity_value)
        }else{
            updateUserOrder(productId, producttype, action)
        }
    })
}

for (i=0; i < removeCartBtns.length; i++){
    removeCartBtns[i].addEventListener('click', function(){
        var productId = this.dataset.rdeletion;
        var action = this.dataset.raction;
        var producttype = this.dataset.rproducttype;

        if (user == 'AnonymousUser'){
            deleteCookieItem(productId, producttype, action)
        }else{
            delete_cartlist(productId, producttype)
        }
    })
}

function delete_cartlist(productId, producttype){
    var url = '/update_cartlist/'

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
            $("#_cart_list").load(" #_cart_list > *");
            location.reload();
    })
}

function addCookieItem(productId, producttype, action){

    if(action == 'add'){

        if(cart[producttype] == undefined){
            cart[producttype] = {}
            cart[producttype][productId] = {'quantity': 1}
            toastr.success('Add to Cart!')
        }else{
            if (cart[producttype][productId] == undefined){

                cart[producttype][productId] = {'quantity': 1}
                toastr.success('Add to Cart!')
            }else{


                cart[producttype][productId]['quantity'] += 1
                toastr.success('Add to Cart!')
            }

        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    $("#append_here").load(" #append_here > *")
}


function addCookieItems(productId, producttype, action, quantity){

    if(action == 'add'){

        if(cart[producttype] == undefined){
            cart[producttype] = {}
            cart[producttype][productId] = {'quantity': quantity}
            toastr.success('Add to Cart!')
        }else{
            if (cart[producttype][productId] == undefined){

                cart[producttype][productId] = {'quantity': quantity}
                toastr.success('Add to Cart!')
            }else{


                cart[producttype][productId]['quantity'] += quantity
                toastr.success('Add to Cart!')
            }

        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    $("#append_here").load(" #append_here > *")
}

function deleteCookieItem(productId, producttype, action){

    if(action == 'delete'){
        cart[producttype][productId]['quantity'] -= 1

        if (cart[producttype][productId]['quantity'] <= 0 ){

            delete cart[producttype][productId]
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload();

}


function updateUserOrder(productId, producttype, action){
    var url = '/updateCart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId, 'producttype':producttype, 'action':action})
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