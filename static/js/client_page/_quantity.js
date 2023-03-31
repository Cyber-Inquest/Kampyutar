
function _quantity(ids, categories, current_user){
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
            body:JSON.stringify({'productId':ids, 'producttype':categories , 'action': 'update', 'quantity':quantity_value})
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
