"""Main Program."""
import products
import promotions
import store

# setup initial stock of inventory
product_list = [ products.Product("MacBook Air M2", price=1450, quantity=100),
                 products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                 products.Product("Google Pixel 7", price=500, quantity=250),
                 products.NonStockedProduct("Windows License", price=125),
                 products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
               ]
best_buy = store.Store(product_list)

# Create promotion catalog
second_half_price = promotions.SecondHalfPrice("Second Half price!")
third_one_free = promotions.ThirdOneFree("Third One Free!")
thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

# Add promotions to products
product_list[0].set_promotion(second_half_price)
product_list[1].set_promotion(third_one_free)
product_list[3].set_promotion(thirty_percent)

def start(store_object: store.Store):
    """Main Program. it starts the buy and order process."""
    while True:
        print("""Store Menu
   ----------
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit""")

        choice = input("Please choose a number: ")

        if choice == "1":
            for index, product in enumerate(store_object.get_all_products(), start=1):
                print(f"{index}. ", end="")
                product.show()

        elif choice == "2":
            print(f"Total of {store_object.get_total_quantity()} items in store")

        elif choice == "3":
            shopping_list = []

            print("---------")

            for index, product in enumerate(store_object.get_all_products(), start=1):
                print(f"{index}. ", end="")
                product.show()

            print("---------")

            print("When you want to finish order, enter empty text.")

            while True:
                product_input = input("Which product # do you want? ")
                if product_input == "":
                    break

                try:
                    product_index = int(product_input) - 1
                    available_products = store_object.get_all_products()

                    if product_index < 0 or product_index >= len(available_products):
                        print("Invalid product number.")
                        continue

                    quantity_input = input("What amount do you want? ")
                    if quantity_input == "":
                        break

                    quantity = int(quantity_input)
                    if quantity <= 0:
                        print("Quantity must be positive.")
                        continue

                    shopping_list.append((available_products[product_index], quantity))

                except ValueError:
                    print("Please enter a valid number.")

            if shopping_list:
                try:
                    total_price = store_object.order(shopping_list)
                    print(f"Order made! Total payment: ${total_price}")
                except Exception as err:
                    print(f"Error processing order: {err}")
            else:
                print("No items ordered.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    start(best_buy)