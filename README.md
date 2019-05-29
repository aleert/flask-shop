This is a small shop written for educational purposes in Flask with some js filled with
randomly generated filler items.

To run it use `pip install -r requirements.txt` and then do `flask run`.
After that - navigate to `localhost:5000` in your browser.

It uses in-memory sqlite db, so if you restart a server
all carts will be removed from it, but cart_it still be kept
in browser localstorage, which can lead to 404 if you click Cart icon
right after restarting a server. To reset a cart_id just add some item to cart (or configure db to use a file).

Checkout button does nothing but delete all items from cart.
There's currently no way to delete a single item from cart.
