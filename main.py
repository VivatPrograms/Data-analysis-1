import pandas as pd
import matplotlib.pyplot as plt
from csv_create import create_random_csv
from fpdf import FPDF
import mimetypes
from tabulate import tabulate

create_random_csv()

df = pd.read_csv("sample_data.csv", 
                 sep=",", 
                 header=0, 
                 names=["date", "product", "quantity", "price"],
                 parse_dates=[0], 
                 index_col=None)

quan_by_product = df.groupby("product")["quantity"].sum()
avr_sale_by_product = df.groupby("product")["price"].mean()
max_sold = pd.DataFrame({'month': quan_by_product.idxmax(), 'highest_sales': quan_by_product.max()}, index=[0])
monthly_sales = df.groupby(df["date"].dt.month)["quantity"].sum()
best_month = pd.DataFrame({'month': monthly_sales.idxmax(), 'highest_sales': monthly_sales.max()}, index=[0])
price_by_date =df.groupby('date')['price'].sum()

repeat = True
while repeat:
    answer1 = input('----------------------------------------\nPick one chart - bar, line, pie : ')
    if answer1 == 'bar':
        answer2 = input('----------------------------------------\nPick one type - h (horizontal) or v (vertical) : ')
        if answer2 == 'h':
            plt.barh(quan_by_product.index, quan_by_product.values, color = 'green', align = 'center', alpha = 1)
        elif answer2 == 'v':
            plt.bar(quan_by_product.index, quan_by_product.values, color = 'green', align = 'center', alpha = 1)
        else: repeat = False
        plt.xlabel("Product")
        plt.ylabel("Total Sales")
        plt.title("Total Sales by Product")
        plt.savefig("chart.png")
        plt.show()
    elif answer1 == 'line':
        plt.plot(monthly_sales.index, monthly_sales.values, color = 'green')
        plt.xlabel("Month")
        plt.ylabel("Total Sales")
        plt.title("Total Sales over Time")
        plt.savefig("chart.png")
        plt.show()
    elif answer1 == 'pie':
        plt.pie(quan_by_product.values, labels=quan_by_product.index, 
                autopct=lambda p:"{:.2f}%  ({:,.0f})".format(p, (p/100)*sum(quan_by_product.values)))
        plt.legend(quan_by_product.index, bbox_to_anchor=(1,0), loc="lower right", bbox_transform=plt.gcf().transFigure)
        plt.title("Total Sales by Product")
        plt.savefig("chart.png")
        plt.show()
    
    if input('----------------------------------------\nExport data to html? (Y to export) ') == 'Y':
        answer3 = input('----------------------------------------\npdf or html : ')
        if answer3 == 'pdf':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            table = tabulate(df, headers='keys', tablefmt='pipe', numalign = "center")
            pdf.write(8, table)
            img_path = 'chart.png'
            pdf.image(img_path, x=10, y=10, w=190, h=0)
            pdf.output("table.pdf")
        elif answer3 == 'html':
            html_table = df.to_html()
            with open("table.html", "w") as f:
                f.write(html_table)
            with open("table.html", "a") as f:
                f.write("<br>")
                img_path = "chart.png"
                img_type = mimetypes.guess_type(img_path)[0]
                f.write(f'<img src="{img_path}" alt="Chart" type="{img_type}">')

    if input('----------------------------------------\nDo you wish to continue? (N to stop) ') == 'N': repeat = False