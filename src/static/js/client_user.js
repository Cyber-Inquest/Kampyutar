var addwishlistbtns = document.getElementsByClassName('fas fa-heart');
var delwishlist = document.getElementsByClassName('wish_del_btn');

for (i=0; i < addwishlistbtns.length; i++){
    addwishlistbtns[i].addEventListener('click', function(){
        var wishproduct = this.dataset.wishproduct;
        var wishproducttype = this.dataset.wishproducttype;
        console.log('wishproduct:',wishproduct, 'wishproducttype:',wishproducttype)
        console.log('user:',user)
        if (user == 'AnonymousUser'){
            console.log('User is not authenticated ')
            toastr.warning('You must login first!')
        }else{
            console.log('User is authenticated, sending data ... ')
            add_wishlist(wishproducttype, wishproduct)
        }
    })
}

for (i=0; i < delwishlist.length; i++){
    delwishlist[i].addEventListener('click', function(){
        var product_id = this.dataset.del_wish_product;
        var product_type = this.dataset.del_wish_productype;
        console.log('product_id:',product_id, 'product_type:',product_type)
        console.log('user:',user)
        if (user == 'AnonymousUser'){
            console.log('User is not authenticated ')
            toastr.warning('You must login first!')
        }else{
            console.log('User is authenticated, sending data ... ')
            delete_wishlist(product_id, product_type)
        }
    })
}

function delete_wishlist(productId, producttype){
    var url = '/update_wishlist/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': window.CSRF_TOKEN,
        },
        body:JSON.stringify({'productId':productId, 'producttype': producttype})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        if (data['_actr'] == 'True'){
             $("#wishlist").load(" #wishlist > *");
        }

    })
}

function add_wishlist(producttype, productId){
    var url = '/add_wishlist/'

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
        if (data['_actr'] == 'True'){
            console.log('add to wishlist')
            $("#wishlist").load(" #wishlist > *");
            location.reload();
        }else{
            console.log('user is not authenticated')
            toastr.warning('You must login first!')
        }

    })
}

function del_order(productId){
    var url = '/update_orderlist/'

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
            $("#ua_orderList").load(" #ua_orderList > *");
    })
}

