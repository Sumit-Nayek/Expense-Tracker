
## 📌 Project Overview  
The **Expense-Tracker** application is a lightweight tool to help users record, categorize, and analyze their daily expenses. It provides functionality for adding expense entries, categorizing them (e.g., food, bills, travel), viewing summary reports, and tracking spending trends. The app emphasises core programming concepts—data structures, control flow, modular design—and demonstrates how they work together to create a functional application.

---

## 🧠 Programming Concepts & How They Work Together  
### 1. Data Structures  
- **Lists / Arrays**: Used to hold individual expense entries perhaps in memory or as interim storage.  
- **Dictionaries / Hash Maps**: Employed for categorizing expenses (category → list of entries) and for quick look-ups (e.g., totals per category).  
- **Classes / Objects**: If an object-oriented approach is used, each expense record may be an instance of an `Expense` class with properties like `amount`, `date`, `category`, `notes`.  
These data structures provide the backbone for storing, retrieving and aggregating expense data.

### 2. Control Flow & Logic  
- **Input Handling**: User input is validated via conditionals (if/else) and loops (while/for) to continuously accept new entries until user exits.  
- **Data Processing**: When summarizing or aggregating expenses, loops iterate over data structures (lists/dicts), conditionals filter entries (by date or category), and functions perform calculations (sum, average).  
- **Modular Functions/Methods**: Key operations (add expense, remove expense, compute total, generate report) are encapsulated in functions or methods, improving readability and maintainability.  
- **Error Handling**: Try/except blocks (or equivalent) protect against invalid inputs (non-numeric amounts, invalid dates) and ensure graceful behaviour.

### 3. Integration Flow  
When a user adds a new expense:  
- The input is captured and validated.  
- A new `Expense` object (or dictionary) is created and appended to the list of all expenses.  
- The category dictionary is updated (if category key exists, append; else create new list).  
- The summary logic loops across the dictionary, computing totals per category and generating a report view.  
- The user interface (CLI or GUI) displays the updated summary and trend indicators.

By separating concerns **data storage**, **business logic**, **UI/control flow** the application remains modular and easier to test or extend.

---

## ⚠️ Limitations of Data Structures & Control Flow  
### Data Structure Limitations  
- Using simple lists/dictionaries in memory means all data is lost when the app stops or the device shuts down unless persistent storage (e.g., file, database) is added.  
- Dictionaries keyed by category assume category names are consistent and do not change or duplicate (risk of typos/fuzzy matches).  
- No indexed or time-series optimized structure: aggregations across date ranges may be slow if the number of entries grows large, since loops must traverse entire lists.

### Control Flow / Logic Limitations  
- Linear loops for aggregation (e.g., summing across all entries each time) may become inefficient when the dataset gets large (O(n) each time).  
- Nested loops (e.g., for each category, loop each entry) can lead to O(n·m) complexity if both categories and entries are many—performance may degrade.  
- The input validation logic may become complex if many edge-cases are supported, reducing readability.  
- If the UI/control loop is blocking (e.g., waiting synchronously for user input), scalability or responsiveness may suffer in more advanced GUI/web versions.

