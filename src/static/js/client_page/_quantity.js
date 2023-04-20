function cart_update(cartIds,productId,user,action)
{
    final_ids = '_quantity_cart' + cartIds
    var quantity_value = document.getElementById(final_ids).value;
    if (user == 'AnonymousUser'){
        if(action == 'add'){
                if (cart[productId] == undefined){
                    cart[productId] = {'quantity': 1}
                    toastr.success('Add to Cart!')
                }else{
                    var quantity = cart[productId]['quantity'] 
                    cart[productId]['quantity'] = parseInt(quantity)+1
                    toastr.success('Add to Carterer!')
                }
            }
        else if(action == 'sub'){
            cart[productId]['quantity'] -= 1

            if (cart[productId]['quantity'] <= 0 ){

                delete cart[productId]
            }
        }
        else if(action == 'manual_input')
        {

            cart[productId]['quantity'] = quantity_value
            if (parseInt(cart[productId]['quantity']) <= 0 ){
                
                delete cart[productId]
            }
            toastr.success('Add to Cart!')
        }
        else{
            toastr.error('Error Occured !')
        }
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
        location.reload();
    }
    else{
        if(action == 'add'){
            var url = '/updateCart/'
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type':'application/json',
                    'X-CSRFToken': window.CSRF_TOKEN,
                },
                body:JSON.stringify({'productId':productId, 'action': 'update', 'quantity':parseInt(quantity_value)+1})
            })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                if (data['_actr'] == 'True'){
                    $("#_cart_list").load(" #_cart_list > *");
                    toastr.success('Cart Updated!')
                }
            })
        }
        else if(action == 'sub'){
            var url = '/updateCart/'
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type':'application/json',
                    'X-CSRFToken': window.CSRF_TOKEN,
                },
                body:JSON.stringify({'productId':productId, 'action': 'update', 'quantity':parseInt(quantity_value)-1})
            })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                if (data['_actr'] == 'True'){
                    $("#_cart_list").load(" #_cart_list > *");
                    toastr.success('Cart Updated!')
                }
            })
        }
        else if (action == 'manual_input'){
            var url = '/updateCart/'
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type':'application/json',
                    'X-CSRFToken': window.CSRF_TOKEN,
                },
                body:JSON.stringify({'productId':productId, 'action': 'update', 'quantity':parseInt(quantity_value)})
            })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                if (data['_actr'] == 'True'){
                    $("#_cart_list").load(" #_cart_list > *");
                    toastr.success('Cart Updated!')
                }
            })
        }
        else{
            toastr.error('Error Occured !')
        }
        location.reload();
    }
    
    
}

function deleteCart(produtId,user){
    if (user == 'AnonymousUser'){
        delete cart[produtId]
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
        location.reload();
    }
    else{
        var url = '/updateCart/'
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken': window.CSRF_TOKEN,
            },
            body:JSON.stringify({'productId':produtId, 'action': 'update', 'quantity':0})
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if (data['_actr'] == 'True'){
                $("#_cart_list").load(" #_cart_list > *");
                toastr.success('Cart Updated!')
            }
        })
        location.reload();
    }
}

function _quantity(ids, categories, current_user){
    alert('hello')
    final_ids = '_quantity_cart' + ids
    var quantity_value = document.getElementById(final_ids).value;

    if (user == 'AnonymousUser'){

        if(cart[categories] == undefined){
            cart[categories] = {}
            cart[categories][ids] = {'quantity': 1}


        }else{
            if (cart[categories][ids] == undefined){

                cart[categories][ids] = {'quantity': 1}

            }else{

                cart[categories][ids]['quantity'] += 1

            }

        }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload();

    }else{
      var url = '/updateCart/'

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken': window.CSRF_TOKEN,
            },
            body:JSON.stringify({'productId':ids, 'action': 'update', 'quantity':quantity_value})
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            if (data['_actr'] == 'True'){
                $("#_cart_list").load(" #_cart_list > *");
                toastr.success('Cart Updated!')
            }

        })

    }
}
