
// AJAX ADD/DECREASE FUNCTION CART 
$(document).ready(function () {
    // Add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        data = {
            food_id: food_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                if(response.status == 'Failed') {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.message,
                    })
                } else if(response.status == 'login_required') {
                    Swal.fire({
                        icon: 'info',
                        title: 'Oops...',
                        text: response.message,
                      }).then(function(){
                        window.location = '/login';
                      })
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                }
            }
        })
    })


    // Place the cart item quantity to load
    $('.item_qty').each(function(){
        var the_id = $(this).attr("id")
        var qty = $(this).attr("data-qty")
        $('#qty-'+the_id).html(qty)
    })


    // Decrease to cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        data = {
            food_id: food_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                if(response.status == 'Failed') {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.message,
                    })
                } else if(response.status == 'login_required') {
                    Swal.fire({
                        icon: 'info',
                        title: 'Oops...',
                        text: response.message,
                      }).then(function(){
                        window.location = '/login';
                      })
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                }
                
            }
        })
    })
});