import streamlit as st
STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / 'style.css'
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

("style.css")

# Add a title to the app
st.title("Sales Analysis")
st.write("""
The business requested an executive sales report for sales managers. User stories and acceptance criteria were created to guide the development of a Power BI dashboard that would provide sales managers with a dashboard overview of internet sales, allow sales representatives to view detailed Internet Sales data for customers and products, and compare sales data against budget. To create the necessary data model for the dashboard, data was cleansed and transformed using SQL statements on tables from the AdventureWorksDW2019 database, including DimDate, DimCustomer, DimProduct, and FactInternetSales. The data model was then enhanced with an Excel data source containing sales budget data.
""")

# Create a function that displays a project image and description
def show_project(image, description):
    st.image(image, width=700)
    st.markdown(description)

# Show the first project
#st.header("Project 1")
#show_project("project1.jpg", "This is the first project. It involves building a web application using Streamlit and Python.")

# Add a title to the app
st.header("Business Request & User Stories")
st.write("The business requested that an executive sales report be created for sales managers. To fulfill this request and ensure that the project met all necessary acceptance criteria, the following user stories were defined based on the business's request.")

st.header("Business Request")
show_project("req.png", "Here I highlighted the key information from the request.")

st.header("User Stories")
# Create a table with the given information
st.table([[ "As a (role)", "I want (request / demand)", "So that I (user value)", "Acceptance Criteria"],
    ["Sales Manager", "To get a dashboard overview of internet sales", "Can follow better which customers and products sells the best", "A Power BI dashboard which updates data once a day"],
    [ "Sales Representative", "A detailed overview of Internet Sales per Customers", "Can follow up my customers that buys the most and who we can sell more to", "A Power BI dashboard which allows me to filter data for each customer"],
    [ "Sales Representative", "A detailed overview of Internet Sales per Products", "Can follow up my Products that sells the most", "A Power BI dashboard which allows me to filter data for each Product"],
    [ "Sales Manager", "A dashboard overview of internet sales", "Follow sales over time against budget", "A Power Bi dashboard with graphs and KPIs comparing against budget"]
])


st.header("Raw Data")
show_project("sql.png", "Raw data in SQL.")
show_project("ex.png", "This is the sales budget file provided in Excel format.")


# Add a title to the app
st.title("Data Cleaning & Transformation (SQL)")
st.write("""
To create the necessary data model for analysis and fulfilling the business needs defined in the user stories, the following tables were extracted using SQL. One data source (sales budgets) was provided in Excel format and connected to the data model in a later step of the process. Below are the SQL statements for cleansing and transforming the necessary data
""")
st.subheader("DIM_Calendar:")
# Display a code example in markdown
st.markdown("""
```sql
-- Cleaned DIM_Date Table --
SELECT 
  [DateKey], 
  [FullDateAlternateKey] AS Date, 
  --[DayNumberOfWeek], 
  [EnglishDayNameOfWeek] AS Day, 
  --[SpanishDayNameOfWeek], 
  --[FrenchDayNameOfWeek], 
  --[DayNumberOfMonth], 
  --[DayNumberOfYear], 
  --[WeekNumberOfYear],
  [EnglishMonthName] AS Month, 
  -- Useful for front end date navigation and front end graphs.
  Left([EnglishMonthName], 3) AS MonthShort,   
  --[SpanishMonthName], 
  --[FrenchMonthName], 
  [MonthNumberOfYear] AS MonthNo, 
  [CalendarQuarter] AS Quarter, 
  [CalendarYear] AS Year --[CalendarSemester], 
  --[FiscalQuarter], 
  --[FiscalYear], 
  --[FiscalSemester] 
FROM 
 [AdventureWorksDW2019].[dbo].[DimDate]
WHERE 
  CalendarYear >= 2019
""")
st.subheader("DIM_Customers:")
# Display a code example in markdown
st.markdown("""
```sql
-- Cleansed DIM_Customers Table --
SELECT 
  c.customerkey AS CustomerKey, 
  --      ,[GeographyKey]
  --      ,[CustomerAlternateKey]
  --      ,[Title]
  c.firstname AS [First Name], 
  --      ,[MiddleName]
  c.lastname AS [Last Name], 
  c.firstname + ' ' + lastname AS [Full Name], 
  -- Combined First and Last Name
  --      ,[NameStyle]
  --      ,[BirthDate]
  --      ,[MaritalStatus]
  --      ,[Suffix]
  CASE c.gender WHEN 'M' THEN 'Male' WHEN 'F' THEN 'Female' END AS Gender,
  --      ,[EmailAddress]
  --      ,[YearlyIncome]
  --      ,[TotalChildren]
  --      ,[NumberChildrenAtHome]
  --      ,[EnglishEducation]
  --      ,[SpanishEducation]
  --      ,[FrenchEducation]
  --      ,[EnglishOccupation]
  --      ,[SpanishOccupation]
  --      ,[FrenchOccupation]
  --      ,[HouseOwnerFlag]
  --      ,[NumberCarsOwned]
  --      ,[AddressLine1]
  --      ,[AddressLine2]
  --      ,[Phone]
  c.datefirstpurchase AS DateFirstPurchase, 
  --      ,[CommuteDistance]
  g.city AS [Customer City] -- Joined in Customer City from Geography Table
FROM 
  [AdventureWorksDW2019].[dbo].[DimCustomer] as c
  LEFT JOIN dbo.dimgeography AS g ON g.geographykey = c.geographykey 
ORDER BY 
  CustomerKey ASC -- Ordered List by CustomerKey
""")
st.subheader("DIM_Products:")
# Display a code example in markdown
st.markdown("""
```sql
-- Cleansed DIM_Products Table --
SELECT 
  p.[ProductKey], 
  p.[ProductAlternateKey] AS ProductItemCode, 
  --      ,[ProductSubcategoryKey], 
  --      ,[WeightUnitMeasureCode]
  --      ,[SizeUnitMeasureCode] 
  p.[EnglishProductName] AS [Product Name], 
  ps.EnglishProductSubcategoryName AS [Sub Category], -- Joined in from Sub Category Table
  pc.EnglishProductCategoryName AS [Product Category], -- Joined in from Category Table
  --      ,[SpanishProductName]
  --      ,[FrenchProductName]
  --      ,[StandardCost]
  --      ,[FinishedGoodsFlag] 
  p.[Color] AS [Product Color], 
  --      ,[SafetyStockLevel]
  --      ,[ReorderPoint]
  --      ,[ListPrice] 
  p.[Size] AS [Product Size], 
  --      ,[SizeRange]
  --      ,[Weight]
  --      ,[DaysToManufacture]
  p.[ProductLine] AS [Product Line], 
  --     ,[DealerPrice]
  --      ,[Class]
  --      ,[Style] 
  p.[ModelName] AS [Product Model Name], 
  --      ,[LargePhoto]
  p.[EnglishDescription] AS [Product Description], 
  --      ,[FrenchDescription]
  --      ,[ChineseDescription]
  --      ,[ArabicDescription]
  --      ,[HebrewDescription]
  --      ,[ThaiDescription]
  --      ,[GermanDescription]
  --      ,[JapaneseDescription]
  --      ,[TurkishDescription]
  --      ,[StartDate], 
  --      ,[EndDate], 
  ISNULL (p.Status, 'Outdated') AS [Product Status] 
FROM 
  [AdventureWorksDW2019].[dbo].[DimProduct] as p
  LEFT JOIN dbo.DimProductSubcategory AS ps ON ps.ProductSubcategoryKey = p.ProductSubcategoryKey 
  LEFT JOIN dbo.DimProductCategory AS pc ON ps.ProductCategoryKey = pc.ProductCategoryKey 
order by 
  p.ProductKey asc
""")
st.subheader("FACT_InternetSales:")
# Display a code example in markdown
st.markdown("""
```sql
-- Cleansed FACT_InternetSales Table --
SELECT 
  [ProductKey], 
  [OrderDateKey], 
  [DueDateKey], 
  [ShipDateKey], 
  [CustomerKey], 
  --  ,[PromotionKey]
  --  ,[CurrencyKey]
  --  ,[SalesTerritoryKey]
  [SalesOrderNumber], 
  --  [SalesOrderLineNumber], 
  --  ,[RevisionNumber]
  --  ,[OrderQuantity], 
  --  ,[UnitPrice], 
  --  ,[ExtendedAmount]
  --  ,[UnitPriceDiscountPct]
  --  ,[DiscountAmount] 
  --  ,[ProductStandardCost]
  --  ,[TotalProductCost] 
  [SalesAmount] --  ,[TaxAmt]
  --  ,[Freight]
  --  ,[CarrierTrackingNumber] 
  --  ,[CustomerPONumber] 
  --  ,[OrderDate] 
  --  ,[DueDate] 
  --  ,[ShipDate] 
FROM 
  [AdventureWorksDW2019].[dbo].[FactInternetSales]
WHERE 
  LEFT (OrderDateKey, 4) >= YEAR(GETDATE()) -2 -- Ensures we always only bring two years of date from extraction.
ORDER BY
  OrderDateKey ASC
""")

st.header("Data Model")
st.write("""
Below is a screenshot of the data model after cleansed and prepared tables were read into Power BI.

This data model also shows how FACT_Budget has been connected to FACT_InternetSales and other necessary DIM tables.
""")
# Show the third project
#st.header("Project 3")
show_project("pic.png", "This is the third project. It involves analyzing a large dataset using SQL and Python.")

st.header("Sales Management Dashboard")
st.write("""
The finished sales management dashboard with one page showing the sales overview, and the other pages focused on combining tables for necessary details and visualizations to show sales over time, per customers and per products.
""")
st.write("You can interact with the dashboard below!")
st.markdown("""
    <iframe src='https://app.powerbi.com/view?r=eyJrIjoiMmMxMjU1ZDAtMDBhYy00ZTgyLTg1MWQtNzNlMGFlMjlmODc3IiwidCI6IjA5NmViYzNjLThhYmQtNDBhNi1iNGZmLTdjYmY0YTk2MmM5NSJ9&pageName=ReportSection' width='700' height='400'></iframe>
""", unsafe_allow_html=True)






