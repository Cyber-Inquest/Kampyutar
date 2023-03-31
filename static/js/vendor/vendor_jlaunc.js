var brandBtns = document.getElementsByClassName('_vendor_brand_image_jlaunch');

for (i=0; i < brandBtns.length; i++){
    brandBtns[i].addEventListener('click', function(){

        var brandId = this.dataset.brandid;
        var price_min = document.getElementById("price_min").value;
        var price_max = document.getElementById("price_max").value;
        var condition = document.getElementById("v_tB_condition").value;
        var toggle_checkbox = jQuery('#toggle_checkbox').is(':checked')?'yes':'no';

        updateBrandSelection(brandId, price_min, price_max, condition, toggle_checkbox)
    })
}

function updateBrandSelection(brandId, price_min, price_max, condition, toggle_checkbox){
    var url = '/vendor/vendor_ajax_just_launched/'

    $.ajax({
            url: url,
            data: {
                'brandId': brandId, 'price_min': price_min, 'price_max': price_max, 'condition': condition, 'toggle_checkbox': toggle_checkbox
            },
            success: function (data) {
                var delprodBtns1 = document.getElementsByClassName('pcTitle_name');
                let html_data = '';
                let count = 0;
                data.forEach(function (city) {

                    html_data +=
                        `<div class="v_cS_perContent">
                            <div class="v_cS_pCTitle">
                                <span class="pcTitle_name">${city[0]}</span>
                                <p>${city[1]}</p>
                            </div>
                            <div class="v_cS_btns">
                                <div class="v_cS_hotTags">
                                    <i class="fa-solid fa-fire-flame-curved" style="color: red;"></i>
                                    <i class="fa-solid fa-droplet" style="color: green;"></i>
                                    <i class="fa-solid fa-rocket" style="color: #4CB9EB;"></i>
                                </div>
                                <div class="v_cS_priceTag">Rs. ${city[2]}</div>
                                <div class="v_cS_qty">
                                    <input type="number" name="_vendor_quantity" id="_vendor_quantity_id${count}" value="1" placeholder="QTY">
                                </div>
                                ${stock_fun(city[3], city[4], city[5], count)}
                            </div>
                        </div>`
                        count += 1
                });
                $(".vendor_contentSpace").html(html_data);
            }
        });
}

function stock_fun(stock_item, _p_id, _p_type, itemcount) {
     let mark = '';
     product_id = _p_id;
     product_type = _p_type;
     product_item = itemcount;

    if (stock_item == 0){
      mark = ` <div class="v_cS_addToCart">
                <button class="v_cS_addToCartBtn_disable" style="background-color:grey;"  disabled>Add To Cart</button>
              </div>`
    } else {
        mark =`<div class="v_cS_addToCart">
                <button onclick="vendorcartadd(${product_id}, '${product_type}', ${product_item});" class="v_cS_addToCartBtn">Add To Cart</button>
        </div>`
    }
    return mark;
}
