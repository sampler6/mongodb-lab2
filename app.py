import tkinter as tk
from tkinter import ttk
import json
from db import shop


class ProductQueryApp():
    def __init__(self, master, collection, f: tuple[str, str, str]):
        self.master = master
        #self.master.geometry("1920x1080")
        self.master.title("Product Query App")
        self.master['background']='grey'
        self.listCategory = sorted(list(collection.distinct("category")))
        self.listCustomer = sorted(list(collection.distinct("customer_info.customer_name")))
        self.listColors = sorted(list(collection.distinct("characteristics.color")))
        self.listProducts = sorted(list(collection.distinct("product_name")))
        self.listDeliveries = sorted(list(collection.distinct("customer_info.delivery_service")))
        self.collection = collection

        # Первый запрос
        self.category_label1 = tk.Label(self.master, text="Категория:", background="grey", font=f)
        self.category_label1.grid(row=0, column=0, padx=10, pady=10)

        self.category_var = tk.StringVar()
        self.category_entry = ttk.Combobox(master, textvariable=self.category_var, values=self.listCategory)
        self.category_entry.grid(row=1, column=0)

        self.query_button_1 = tk.Button(self.master, text="1. Названия товаров по категории",
                                        command=self.get_product_names_by_catregory)
        self.query_button_1.grid(row=5, column=0, padx=10, pady=10)

        # Второй запрос
        self.query_button_2 = tk.Button(self.master, text="2. Характеристики товаров по категории",
                                        command=self.get_product_characteristics_by_category)
        self.query_button_2.grid(row=5, column=1, padx=10, pady=10)

        # Третий запрос
        self.category_label2 = tk.Label(self.master, text="Покупатели:", background="grey", font=f)
        self.category_label2.grid(row=0, column=1, padx=10, pady=10)

        self.clients_var = tk.StringVar()
        self.clients_entry = ttk.Combobox(master, textvariable=self.clients_var, values=self.listCustomer)
        self.clients_entry.grid(row=1, column=1)

        self.query_button_3 = tk.Button(self.master, text="3. Товары, купленные заданным покупателем",
                                        command=self.get_products_by_customer)
        self.query_button_3.grid(row=5, column=3, padx=10, pady=10)

        # Четвертый запрос
        self.category_label4 = tk.Label(self.master, text="Цвета:", background="grey", font=f)
        self.category_label4.grid(row=0, column=2, padx=10, pady=10)

        self.colors_var = tk.StringVar()
        self.colors_entry = ttk.Combobox(master, textvariable=self.colors_var, values=self.listColors)
        self.colors_entry.grid(row=1, column=2)

        self.query_button_4 = tk.Button(self.master, text="4. Товары с заданным цветом", command=self.get_products_by_color)
        self.query_button_4.grid(row=5, column=4, padx=10, pady=10)

        # Пятый запрос
        self.category_label5 = tk.Label(self.master, text="Общая сумма:", background="grey", font=f)
        self.category_label5.grid(row=3, column=0, padx=10, pady=10)

        self.query_button_5 = tk.Button(self.master, text="5. Общая сумма проданных товаров",
                                        command=self.get_total_sold_amount)
        self.query_button_5.grid(row=6, column=0, padx=10, pady=10)

        # Шестой запрос
        self.query_button_6 = tk.Button(self.master, text="6. Количество товаров в каждой категории",
                                        command=self.get_products_count_by_category)
        self.query_button_6.grid(row=6, column=1, padx=10, pady=10)

        # Седьмой запрос
        self.category_label7 = tk.Label(self.master, text="Товары:", background="grey", font=f)
        self.category_label7.grid(row=0, column=3, padx=10, pady=10)

        self.products_var = tk.StringVar()
        self.products_entry = ttk.Combobox(master, textvariable=self.products_var, values=self.listProducts)
        self.products_entry.grid(row=1, column=3)

        self.query_button_7 = tk.Button(self.master, text="7. Имена покупателей заданного товара",
                                        command=self.get_customer_names_by_product)
        self.query_button_7.grid(row=6, column=3, padx=10, pady=10)

        # Восьмой запрос
        self.category_label8_1 = tk.Label(self.master, text="Службы доставки", background="grey", font=f)
        self.category_label8_1.grid(row=0, column=4, padx=10, pady=10)

        self.products_var_1 = tk.StringVar()
        self.collection_entry8 = ttk.Combobox(master, textvariable=self.products_var_1, values=self.listDeliveries)
        self.collection_entry8.grid(row=1, column=4)

        self.query_button_8 = tk.Button(self.master, text="8. Имена покупателей с доставкой\nзаданных товаров "
                                                          "от заданной фирмы",
                                        command=self.get_customer_names_by_product_and_delivery)
        self.query_button_8.grid(row=6, column=4, padx=10, pady=10)

        # Блок с результатом
        self.result_label = tk.Label(self.master, text="Результат:", background="grey", font=f)
        self.result_label.grid(row=8, column=1, columnspan=3, padx=10, pady=10)

        self.result_text = tk.Text(self.master, height=10, width=100, state="disabled")
        self.result_text.grid(row=9, column=1, columnspan=3, padx=10, pady=10)

        #####################################################
        # 1 запрос

    def get_product_names_by_catregory(self):
        category = self.category_var.get()
        result_text = f"1. Названия товаров по категории '{category}':\n"

        pipeline = [
            {
                "$match": {"category": category}
            },
            {
                "$project": {
                    "_id": 0,
                    "product_name": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )

        for name in a:
            result_text += name['product_name'] + '\n'

        self.update_result_text(result_text)

        # 2 запрос

    def get_product_characteristics_by_category(self):
        category = self.category_var.get()
        result_text = f"2. Характеристики товаров по категории '{category}':\n"

        pipeline = [
            {
                "$match": {"category": category}
            },
            {
                "$project": {
                    "_id": 0,
                    "product_name": 1,
                    "characteristics": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n_______________________________________\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

        # 3 запрос

    def get_products_by_customer(self):
        customer = self.clients_var.get()

        result_text = f"3. Товары, купленные покупателем '{customer}':\n"

        pipeline = [
            {
                "$match": {"customer_info.customer_name": customer}
            },
            {
                "$project": {
                    "_id": 0,
                    "product_name": "$product_name",
                    "price": "$price"
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

        # 4 запрос

    def get_products_by_color(self):
        color = self.colors_var.get()
        result_text = f"4. Товары с цветом '{color}':\n"

        pipeline = [
            {
                "$match": {"characteristics.color": color}
            },
            {
                "$project": {
                    "_id": 0,
                    "product_name": "$product_name",
                    "manufacturer": "$manufacturer",
                    "price": "$price"
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    def get_total_sold_amount(self):
        result_text = f"5. Общая сумма проданных товаров: "

        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_sales": {"$sum": "$price"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "total_sales": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = doc["total_sales"]
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    def get_products_count_by_category(self):
        result_text = f"6. Количество товаров в каждой категории:\n"

        pipeline = [
            {
                "$group": {
                    "_id": "$category",
                    "total_products": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "category": "$_id",
                    "total_products": 1
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    def get_customer_names_by_product(self):
        product_name = self.products_var.get()
        result_text = f"7. Имена покупателей товара '{product_name}':\n"

        pipeline = [
            {
                "$match": {"product_name": product_name}
            },
            {
                "$group": {
                    "_id": "$customer_info.customer_name"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "customer_name": "$_id"
                }
            }
        ]

        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = json.dumps(doc, indent=2, ensure_ascii=False) + '\n\n\n'
            self.result_text.insert(tk.END, json_str)

        self.result_text.config(state="disabled")

    def get_customer_names_by_product_and_delivery(self):
        product_name = self.products_var.get()
        delivery_service = self.products_var_1.get()

        result_text = f"8. Имена покупателей товара '{product_name}' с доставкой от '{delivery_service}':\n"

        pipeline = [
            {
                "$match": {"product_name": product_name, "customer_info.delivery_service": delivery_service}
            },
            {
                "$unwind": "$customer_info"
            },
            {
                "$match": {"customer_info.delivery_service": delivery_service}
            },
            {
                "$group": {
                    "_id": "$customer_info.customer_name"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "customer_name": "$_id"
                }
            }
        ]
        a = self.collection.aggregate(
            pipeline
        )
        self.result_text.config(state=tk.NORMAL)  #
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

        for doc in a:
            json_str = doc["customer_name"]
            self.result_text.insert(tk.END, "-" + json_str + ",\n")

        self.result_text.config(state="disabled")

    def update_result_text(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state="disabled")


root = tk.Tk()
app = ProductQueryApp(root, shop, ("Courier", "20", tk.NORMAL))
root.mainloop()
