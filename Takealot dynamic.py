from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from time import sleep
import webbrowser
brave_path = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'


try: 
    product_info=open("takealot_products.txt","r") #Obtaining the stored product Link
    
    product_info=[i.strip() for i in product_info]
    
    
    product_link=product_info[0]
    
    target_price=int(product_info[1])

except:
    new=2;
    url="https://www.takealot.com/"
    webbrowser.open(url,new)  #Get Product Link
    
    product_link=input("Product Link:")
    target_price=int(input("Price Less Than:"))
    new_prod= open("takealot_products.txt","w")
    new_prod.write(product_link+"\n")
    new_prod.write(str(target_price))
    new_prod.close()
        
#product_link=input("Product Link:")
#target_price=int(input("Price Less Than:"))
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = brave_path
browser = webdriver.Chrome(options=chrome_options)
browser.minimize_window()
while True:
    try:
        
        browser.get(product_link)
        sleep(10) #give the browser time to load
        
        price=browser.find_element(By.XPATH,'//span [contains(@data-ref,"c")]').text
        
        stock_availability =browser.find_element(By.XPATH,'//div [contains(@data-ref,"stock-availability-status")]').text
        stock_location= ""
        if stock_availability == 'In stock':
            stock_location = browser.find_element(By.XPATH,'//div [contains(@class,"cell shrink in-stock-indicator-module_pills-wrapper_3KYbT")]').text
        
        price=price.replace("R","")
        if "," in price:
            price=price.replace(",","")
        price=price.strip()
        product_name=browser.find_element(By.XPATH,'//div//h1').text
        
        no_letters=len(product_name)
        print(product_name)
        print("\nCurrent price is R"+price+"\n")
        font_reduction=round((13/53)*no_letters)
        
        if len(stock_location)>3:
            
            stock_location=stock_location[:3]+" & " +stock_location[3:]
            
        if int(price)<target_price:
            root=tk.Tk()
            root.title("Takealot Notification")
            canvas=tk.Canvas(root,width=800,height=400,bg="white")
            canvas.pack()
            canvas.create_text(400,50, text=product_name,font=("Helvetica",32-font_reduction))
            canvas.create_text(400,175, text="R"+price,font=("Helvetica",38),fill="light green")
            canvas.create_text(400,238, text=stock_availability+" : "+stock_location)
            canvas.create_text(400,300, text="On takealot",font=("Helvetica",24))
            def open_takealot():
                new=2;
                url=product_link
                webbrowser.open(url,new)
            buy_button=tk.Button(root,text="  BUY  ",command=open_takealot)
            canvas.create_window(400,380,window=buy_button)
            
            root.mainloop()
            
            break
        sleep(3600*3)
        
    except:
        
        sleep(300)
