# Google Search Crawler

### EN:

Use WebDriver to crawl Google search results for links and titles

and write Excel data

Built-in functions to manipulate Excel, so you can adjust your own needs

### ZH:

使用 WebDriver 爬取谷歌搜索结果的链接及标题

并写入 Excel 数据

内置有操作 Excel 的函数，可自行调整需求

## Install

```python
pip install -r requirements.txt
```

## ChromeDriver Install

https://sites.google.com/chromium.org/driver/

Download the file and add environment variables
下载文件并添加环境变量

## Set

### EN:

Set the main file configuration variables

```
# Human Machine Inspection Page Tips Text
HM_inspection_tips

# Search engine domain name
search_domain

# Excel file address
file_path

# Table worksheet name
table_name

# table cell
table_cell
```

### ZH:

设置 main 文件配置变量

```
# 人机检查页面提示文本
HM_inspection_tips

# 搜寻引擎域名
search_domain

# Excel文件地址
file_path

# 表格工作表名称
table_name

# 表格单元格
table_cell
```

## Use

### EN:

1. Complete the necessary settings -> run the main.py file

2. Open Driver browser -> Google search page settings -> search results for 100 items -> set region and language

3. Run the interface and enter the next step. ( If you encounter a human machine check, you must pass it manually before entering the next step )

4. After running the program, the table will be written according to the set excel file address (default from cell A2, can be set)

### ZH:

1. 完成必要设置->运行 main.py 文件.

2. 在打开的 Driver 浏览器->谷歌搜索页面设置->搜索结果为 100 条->设置地区及语言.

3. 运行界面回车键下一步.( 若遇到人机检查则必须手动通过后才回车键下一步 )

4. 运行程序后会根据设置的表格文件地址写入表格( 默认从 A2 单元格开始写,可设置 )
