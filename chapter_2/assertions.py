# Use the assert statement to test that a condition is true.
# If the assert condition evaluates to True, nothing happens,
# if it evaluates to False, and AssertionError exception is raised.
#
# Assertions are a debugging aid best used to inform developers of unrecoverable
# errors in the program. Do not use for errors where the user can take
# a corrective action or try again.
#
# assert_stmt ::= "assert" expression1 ["," expression2]
# expression1 = condition to test, expression2 optional error message
def apply_discount(product, discount):
    price = int(product['price']) * (1.0 - discount)
    assert 0 <= price <= product['price'], "Error: Discounted price bust be > 0 and < product price"
    return price


shoes = {'name': 'Fancy Shoes', 'price': 14900}  # price in pence
print('Correct discounted price:', apply_discount(shoes, 0.10), end='\n\n')  # apply 10% discount
print('Invalid discount of 200%:')
print(apply_discount(shoes, 2.0))  # 200% discount raises AssertionError


###############################
# Caveats to using assertions #
###############################
# 1. Don't use assertions for data validation.
# You can disable assertions globally with the -O and -OO command line switches,
# as well as the PYTHONOPTIMIZE environment variable when using CPython.
# Disabling assertions turns any assert statement into a null operation,
# effectively disabling your data validation, which is a security risk!
# Example:
class Product:
    def __init__(self, product_id):
        self.product_id = product_id

    def __repr__(self):
        return f'<Product {self.product_id}>'

    def delete(self):
        pass


class Store:
    def __init__(self, store_id):
        self.store_id = store_id

    def __repr__(self):
        return f'<Store {self.store_id}'

    @staticmethod
    def has_product_id(prod_id):
        pass

    @staticmethod
    def get_product(prod_id):
        return Product(prod_id)


class AuthError(BaseException):
    pass


def delete_product(product_id, user):
    store = Store(1)
    # with assertions disabled, ANY USER can now delete products. Oops!
    assert user.is_admin(), 'Must be and admin'
    # with assertions disabled, the has_product() check is skipped, meaning
    # the .get_product() method could bne called with invalid product IDs.
    # This could lead to DoS is deleting an invalid product crashes the app!
    assert store.has_product_id(product_id), 'Unknown product'
    store.get_product(product_id).delete()
    # Instead, use regular if statements for data validation
    if not user.is_admin():
        raise AuthError('Must be and admin to delete')
    if not store.has_product_id(product_id):
        raise ValueError('Unknown product ID')
    store.get_product(product_id).delete()


# 2. Asserts that never fail - when passing a tuple as the first argument of an assert statement
# the assertion always evaluates to True a d never fails!
# Non-empty tuples in Python are always evaluated to True!
assert (1 == 2, 'This should fail...')  # A good linter should pick this up!
