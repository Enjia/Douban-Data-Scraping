![image](https://github.com/user-attachments/assets/4d4e2765-0ea2-4b04-b329-530e0be53182)# Douban-Data-Scraping
This project is aiming at scraping datum of books or movies that you tagged "want to read/watch" and saving them in local sheet. 

# How to use
## Step1: Check your user agent and cookie in web browser(e.g. Chrome)
Open www.douban.com and see the method mentioned in this [blog](https://blog.csdn.net/weixin_44578172/article/details/109353017)

## Step2:Open cmdline interaction window in your local computer
Windows: Windows Key + R, then input "cmd" and enter
MacOS: command + space, then search "terminal"
If you haven't installed python3.x, please search the installation step by yourself

## Step3: Check your own parameters
Taking my own scraping process for example, there are six parameters you must provide:
- data_type: Choose "books" or "movies"
- num_items: Number of total items of books or movies being tagged for the moment
- base_url: Sign in your own douban homepage and click the buttom of "xxx本想读" or "xxx部想看", then select an random page and copy the base url. For exammple, after I sign in my douban homepage and click page 9, then I can get my base url boxed in red rectangle:
![image](https://github.com/user-attachments/assets/37536a34-2db3-46e5-bc64-526d5c4a47bb)
- save_path: The sheet name and its absolute path you want to save to after scraping
- agent: See step1
- cookie: See step1

## Step4: Input command line for scraping

![image](https://github.com/user-attachments/assets/92ff2fd6-3930-46b5-8c12-e642ef60784a)

If you successfully finished scraping, there would be some inforamtion:
![image](https://github.com/user-attachments/assets/d877445c-6908-4482-b58f-66b6cc6ddd4f)
