
function handleSelectChange(event) {

    var selectElement = event.target;
    var value = selectElement.value;

    var url = '/admin_django/product_selected/'

       $.ajax({
            url: url,
            data: {
                'producttype': value
            },
            success: function (data) {
                let html_data = '<option value="">---------</option>';
                data.forEach(function (city) {
                    html_data += `<option value="${city.id}">${city.title}</option>`
                });
                $("#id_sub_categories").html(html_data);
            }
        });
}
