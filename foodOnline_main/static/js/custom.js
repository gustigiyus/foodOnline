
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

                    // Change amount of price 
                    $('#subtotal').text(response.get_cart_amount['subtotal'])
                    $('#tax').text(response.get_cart_amount['tax'])
                    $('#grand_total').text(response.get_cart_amount['grand_total'])
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
        cart_id = $(this).attr('id');
        
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

                    // Change amount of price 
                    $('#subtotal').text(response.get_cart_amount['subtotal'])
                    $('#tax').text(response.get_cart_amount['tax'])
                    $('#grand_total').text(response.get_cart_amount['grand_total'])

                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.qty, cart_id, response.get_cart_amount);
                        checkEmptyCart()
                    }
                }
                
            }
        })
    })

    // DELETE CART ITEMS
    $('.delete_cart').on('click', function(e){
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'Failed') {
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: response.message,
                    })
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: response.message,
                    })
                    removeCartItem(0, cart_id, response.get_cart_amount);
                    checkEmptyCart();
                }
                
            }
        })
    })

    // DELETE CART ELEMENTS IF THE QTY IS 0
    function removeCartItem(cartItemQty, cart_id, get_cart_amount) {
        if(cartItemQty <= 0) {
            // Remove cart item element
            $('#cart-item-'+cart_id).remove()

            // Change amount of price 
            $('#subtotal').text(get_cart_amount['subtotal'])
            $('#tax').text(get_cart_amount['tax'])
            $('#grand_total').text(get_cart_amount['grand_total'])
        }   
    }

    // CHECK IF TEH CART IS EMPTY
    function checkEmptyCart() {
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0) {
            document.getElementById('empty-cart').style.display = "block";
        } 
    }

});