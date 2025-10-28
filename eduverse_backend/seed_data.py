from sqlalchemy.orm import Session
from database import SessionLocal
from models.course import Course
from models.lesson import Lesson
from models.quiz import Quiz, QuizQuestion, QuizOption
from models.badge import Badge
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Course).first():
            print("Database already seeded!")
            return
        
        # Create Courses
        courses_data = [
            {
                "title": "Python Programming Fundamentals",
                "description": "Master the basics of Python programming from scratch",
                "category": "Programming",
                "difficulty": "Beginner",
                "estimated_hours": 20,
                "xp_reward": 500,
                "thumbnail": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400"
            },
            {
                "title": "Web Development with React",
                "description": "Build modern web applications using React and JavaScript",
                "category": "Web Development",
                "difficulty": "Intermediate",
                "estimated_hours": 30,
                "xp_reward": 750,
                "thumbnail": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=400"
            },
            {
                "title": "Data Science with Python",
                "description": "Learn data analysis, visualization, and machine learning",
                "category": "Data Science",
                "difficulty": "Advanced",
                "estimated_hours": 40,
                "xp_reward": 1000,
                "thumbnail": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400"
            },
            {
                "title": "Machine Learning Basics",
                "description": "Introduction to machine learning algorithms and applications",
                "category": "AI & ML",
                "difficulty": "Intermediate",
                "estimated_hours": 35,
                "xp_reward": 850,
                "thumbnail": "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=400"
            }
        ]
        
        courses = []
        for course_data in courses_data:
            course = Course(**course_data)
            db.add(course)
            courses.append(course)
        
        db.commit()
        
        # Create Lessons for Python Course
        python_lessons = [
            {
                "course_id": courses[0].id,
                "title": "Introduction to Python",
                "content": """# Welcome to Python Programming! 🐍

## What is Python?

Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, Python has become one of the most popular programming languages in the world.

## Why Learn Python?

1. **Easy to Learn**: Python's syntax is clear and intuitive, making it perfect for beginners
2. **Versatile**: Used in web development, data science, AI, automation, and more
3. **Large Community**: Extensive libraries and frameworks available
4. **High Demand**: One of the most sought-after skills in the job market

## Your First Python Program

```python
print("Hello, World!")
```

This simple line of code displays "Hello, World!" on the screen. The `print()` function is one of Python's built-in functions.

## Python Features

- **Dynamic Typing**: No need to declare variable types
- **Object-Oriented**: Supports OOP principles
- **Cross-Platform**: Runs on Windows, Mac, Linux
- **Extensive Libraries**: NumPy, Pandas, Django, Flask, and more

## Getting Started

To start coding in Python, you'll need:
1. Python installed on your computer (download from python.org)
2. A text editor or IDE (VS Code, PyCharm, or IDLE)
3. Enthusiasm to learn!

Let's begin your Python journey! 🚀""",
                "order": 1,
                "video_url": "https://www.youtube.com/embed/kqtD5dpn9C8",
                "duration_minutes": 30,
                "xp_reward": 50
            },
            {
                "course_id": courses[0].id,
                "title": "Variables and Data Types",
                "content": """# Variables and Data Types in Python

## What are Variables?

Variables are containers for storing data values. In Python, you don't need to declare the type of a variable - it's automatically determined.

## Creating Variables

```python
# String variable
name = "Alice"

# Integer variable
age = 25

# Float variable
height = 5.6

# Boolean variable
is_student = True
```

## Python Data Types

### 1. Numeric Types
- **int**: Whole numbers (e.g., 42, -17, 0)
- **float**: Decimal numbers (e.g., 3.14, -0.5)
- **complex**: Complex numbers (e.g., 3+4j)

### 2. Text Type
- **str**: Strings of characters (e.g., "Hello", 'Python')

### 3. Boolean Type
- **bool**: True or False values

### 4. Sequence Types
- **list**: Ordered, mutable collection [1, 2, 3]
- **tuple**: Ordered, immutable collection (1, 2, 3)
- **range**: Sequence of numbers range(5)

## Examples

```python
# Numbers
x = 10
y = 3.14
z = 1 + 2j

# Strings
greeting = "Hello, Python!"
name = 'John'

# Lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]

# Tuples
coordinates = (10, 20)

# Boolean
is_active = True
has_permission = False
```

## Type Conversion

```python
# Convert to integer
x = int("10")  # x = 10

# Convert to float
y = float("3.14")  # y = 3.14

# Convert to string
z = str(100)  # z = "100"
```

## Checking Types

```python
x = 5
print(type(x))  # <class 'int'>

name = "Alice"
print(type(name))  # <class 'str'>
```

Practice these concepts to build a strong foundation! 💪""",
                "order": 2,
                "video_url": "https://www.youtube.com/embed/ppsCxnNm-JI",
                "duration_minutes": 45,
                "xp_reward": 75
            },
            {
                "course_id": courses[0].id,
                "title": "Control Flow and Loops",
                "content": """# Control Flow and Loops in Python

## Conditional Statements (if, elif, else)

Control flow allows your program to make decisions based on conditions.

### If Statement

```python
age = 18

if age >= 18:
    print("You are an adult")
```

### If-Else Statement

```python
temperature = 25

if temperature > 30:
    print("It's hot outside")
else:
    print("The weather is pleasant")
```

### If-Elif-Else Statement

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Your grade is: {grade}")
```

## Loops

Loops allow you to repeat code multiple times.

### For Loop

Used to iterate over a sequence (list, tuple, string, etc.)

```python
# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Loop through a range
for i in range(5):
    print(i)  # Prints 0, 1, 2, 3, 4

# Loop with start and end
for i in range(1, 6):
    print(i)  # Prints 1, 2, 3, 4, 5
```

### While Loop

Repeats as long as a condition is true.

```python
count = 0
while count < 5:
    print(count)
    count += 1

# Be careful with infinite loops!
# while True:
#     print("This runs forever!")
```

## Loop Control Statements

### Break Statement

```python
for i in range(10):
    if i == 5:
        break  # Exit the loop
    print(i)
```

### Continue Statement

```python
for i in range(5):
    if i == 2:
        continue  # Skip this iteration
    print(i)
```

## Nested Loops

```python
for i in range(3):
    for j in range(3):
        print(f"i={i}, j={j}")
```

## Practical Examples

### Example 1: Sum of Numbers

```python
total = 0
for i in range(1, 11):
    total += i
print(f"Sum of 1 to 10: {total}")
```

### Example 2: Find Even Numbers

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = []

for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)

print(f"Even numbers: {even_numbers}")
```

### Example 3: Password Validator

```python
password = input("Enter password: ")

if len(password) < 8:
    print("Password too short")
elif not any(char.isdigit() for char in password):
    print("Password must contain a number")
else:
    print("Password accepted!")
```

Master these control structures to write powerful programs! 🎯""",
                "order": 3,
                "video_url": "https://www.youtube.com/embed/94UHCEmprCY",
                "duration_minutes": 60,
                "xp_reward": 100
            },
            {
                "course_id": courses[0].id,
                "title": "Functions and Modules",
                "content": """# Functions and Modules in Python

## What are Functions?

Functions are reusable blocks of code that perform specific tasks. They help organize code and avoid repetition.

## Defining Functions

```python
def greet():
    print("Hello, World!")

# Call the function
greet()
```

## Functions with Parameters

```python
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")
greet_person("Bob")
```

## Functions with Return Values

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8
```

## Default Parameters

```python
def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()  # Hello, Guest!
greet("Alice")  # Hello, Alice!
```

## Multiple Return Values

```python
def get_user_info():
    name = "Alice"
    age = 25
    city = "New York"
    return name, age, city

name, age, city = get_user_info()
```

## Lambda Functions

Short, anonymous functions for simple operations.

```python
# Regular function
def square(x):
    return x ** 2

# Lambda function
square = lambda x: x ** 2

print(square(5))  # 25
```

## Modules

Modules are files containing Python code that you can import and use.

### Importing Modules

```python
# Import entire module
import math
print(math.pi)

# Import specific function
from math import sqrt
print(sqrt(16))

# Import with alias
import numpy as np
```

### Creating Your Own Module

**mymodule.py:**
```python
def greet(name):
    return f"Hello, {name}!"

PI = 3.14159
```

**main.py:**
```python
import mymodule

print(mymodule.greet("Alice"))
print(mymodule.PI)
```

## Common Built-in Modules

- **math**: Mathematical functions
- **random**: Random number generation
- **datetime**: Date and time operations
- **os**: Operating system interface
- **json**: JSON encoding/decoding

## Practical Examples

```python
import random
import datetime

# Random number
print(random.randint(1, 100))

# Current date
today = datetime.date.today()
print(today)

# Calculate factorial
import math
print(math.factorial(5))  # 120
```

Functions and modules are essential for writing clean, maintainable code! 📦""",
                "order": 4,
                "video_url": "https://www.youtube.com/embed/89cGQjB5R4M",
                "duration_minutes": 50,
                "xp_reward": 90
            },
            {
                "course_id": courses[0].id,
                "title": "Lists and Dictionaries",
                "content": """# Lists and Dictionaries in Python

## Lists

Lists are ordered, mutable collections that can hold items of different types.

### Creating Lists

```python
# Empty list
my_list = []

# List with items
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]
```

### Accessing List Items

```python
fruits = ["apple", "banana", "cherry"]

print(fruits[0])   # apple
print(fruits[-1])  # cherry (last item)
print(fruits[1:3]) # ['banana', 'cherry']
```

### Modifying Lists

```python
fruits = ["apple", "banana", "cherry"]

# Add items
fruits.append("orange")
fruits.insert(1, "mango")

# Remove items
fruits.remove("banana")
popped = fruits.pop()

# Change items
fruits[0] = "pear"
```

### List Methods

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

numbers.sort()        # Sort in place
numbers.reverse()     # Reverse in place
count = numbers.count(1)  # Count occurrences
index = numbers.index(4)  # Find index
```

### List Comprehension

```python
# Create list of squares
squares = [x**2 for x in range(10)]

# Filter even numbers
evens = [x for x in range(20) if x % 2 == 0]
```

## Dictionaries

Dictionaries store key-value pairs, like a real dictionary stores word-definition pairs.

### Creating Dictionaries

```python
# Empty dictionary
my_dict = {}

# Dictionary with items
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}
```

### Accessing Dictionary Items

```python
person = {"name": "Alice", "age": 25}

print(person["name"])        # Alice
print(person.get("age"))     # 25
print(person.get("email", "Not found"))  # Not found
```

### Modifying Dictionaries

```python
person = {"name": "Alice", "age": 25}

# Add/update items
person["email"] = "alice@example.com"
person["age"] = 26

# Remove items
del person["age"]
removed = person.pop("email")
```

### Dictionary Methods

```python
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Get all keys
keys = person.keys()

# Get all values
values = person.values()

# Get all items
items = person.items()

# Loop through dictionary
for key, value in person.items():
    print(f"{key}: {value}")
```

### Dictionary Comprehension

```python
# Create dictionary of squares
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

## Practical Examples

### Example 1: Student Grades

```python
students = {
    "Alice": 95,
    "Bob": 87,
    "Charlie": 92
}

# Add new student
students["David"] = 88

# Calculate average
average = sum(students.values()) / len(students)
print(f"Average grade: {average}")
```

### Example 2: Word Counter

```python
text = "hello world hello python"
words = text.split()

word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

print(word_count)
# {'hello': 2, 'world': 1, 'python': 1}
```

### Example 3: Shopping Cart

```python
cart = []

# Add items
cart.append({"name": "Apple", "price": 1.50, "qty": 3})
cart.append({"name": "Banana", "price": 0.75, "qty": 6})

# Calculate total
total = sum(item["price"] * item["qty"] for item in cart)
print(f"Total: ${total}")
```

Lists and dictionaries are fundamental data structures in Python! 🗂️""",
                "order": 5,
                "video_url": "https://www.youtube.com/embed/W8KRzm-HUcc",
                "duration_minutes": 55,
                "xp_reward": 85
            }
        ]
        
        lessons = []
        for lesson_data in python_lessons:
            lesson = Lesson(**lesson_data)
            db.add(lesson)
            lessons.append(lesson)
        
        db.commit()
        
        # Create Lessons for React Course
        react_lessons = [
            {
                "course_id": courses[1].id,
                "title": "Introduction to React",
                "content": """# Welcome to React! ⚛️

## What is React?

React is a powerful JavaScript library for building user interfaces, developed and maintained by Facebook (Meta). It's one of the most popular frontend frameworks in the world.

## Why Learn React?

1. **Component-Based**: Build encapsulated components that manage their own state
2. **Declarative**: Design simple views for each state in your application
3. **Learn Once, Write Anywhere**: Create web apps, mobile apps (React Native), and more
4. **Huge Ecosystem**: Thousands of libraries and tools available
5. **High Demand**: React developers are in high demand worldwide

## Key Concepts

### Components

Components are the building blocks of React applications. They're like JavaScript functions that return HTML.

```jsx
function Welcome() {
  return <h1>Hello, React!</h1>;
}
```

### JSX

JSX is a syntax extension that looks like HTML but works in JavaScript.

```jsx
const element = <h1>Hello, World!</h1>;
```

### Virtual DOM

React uses a virtual DOM to efficiently update the actual DOM, making applications fast and responsive.

## Setting Up React

```bash
# Create a new React app
npx create-react-app my-app
cd my-app
npm start
```

## Your First Component

```jsx
import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>Welcome to React!</h1>
      <p>Let's build something amazing!</p>
    </div>
  );
}

export default App;
```

## React Features

- **Fast**: Virtual DOM ensures optimal performance
- **Flexible**: Works with other libraries and frameworks
- **Powerful**: Handles complex UIs with ease
- **Popular**: Massive community support

Get ready to build modern web applications! 🚀""",
                "order": 1,
                "video_url": "https://www.youtube.com/embed/SqcY0GlETPk",
                "duration_minutes": 35,
                "xp_reward": 50
            },
            {
                "course_id": courses[1].id,
                "title": "Components and Props",
                "content": """# Components and Props in React

## Understanding Components

Components let you split the UI into independent, reusable pieces. There are two types:

### Function Components

```jsx
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

### Class Components (Legacy)

```jsx
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

**Note**: Function components with Hooks are now the standard!

## Props (Properties)

Props are arguments passed to components, similar to function parameters.

### Passing Props

```jsx
function App() {
  return (
    <div>
      <Welcome name="Alice" />
      <Welcome name="Bob" />
    </div>
  );
}

function Welcome(props) {
  return <h1>Hello, {props.name}!</h1>;
}
```

### Props are Read-Only

```jsx
// ❌ Never modify props
function Welcome(props) {
  props.name = "Changed"; // ERROR!
  return <h1>Hello, {props.name}</h1>;
}

// ✅ Props should be treated as immutable
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}
```

## Destructuring Props

```jsx
// Instead of this:
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

// Do this:
function Welcome({ name, age }) {
  return (
    <div>
      <h1>Hello, {name}</h1>
      <p>Age: {age}</p>
    </div>
  );
}
```

## Default Props

```jsx
function Welcome({ name = "Guest" }) {
  return <h1>Hello, {name}</h1>;
}
```

## Children Props

```jsx
function Card({ children }) {
  return (
    <div className="card">
      {children}
    </div>
  );
}

// Usage
<Card>
  <h2>Title</h2>
  <p>Content goes here</p>
</Card>
```

## Practical Example

```jsx
function UserCard({ name, email, avatar, role = "User" }) {
  return (
    <div className="user-card">
      <img src={avatar} alt={name} />
      <h3>{name}</h3>
      <p>{email}</p>
      <span className="badge">{role}</span>
    </div>
  );
}

function App() {
  return (
    <div>
      <UserCard 
        name="Alice Johnson"
        email="alice@example.com"
        avatar="/alice.jpg"
        role="Admin"
      />
      <UserCard 
        name="Bob Smith"
        email="bob@example.com"
        avatar="/bob.jpg"
      />
    </div>
  );
}
```

## Component Composition

```jsx
function Header() {
  return <header><h1>My App</h1></header>;
}

function Sidebar() {
  return <aside>Sidebar content</aside>;
}

function Content() {
  return <main>Main content</main>;
}

function App() {
  return (
    <div>
      <Header />
      <Sidebar />
      <Content />
    </div>
  );
}
```

Master components and props to build reusable UI elements! 🧩""",
                "order": 2,
                "video_url": "https://www.youtube.com/embed/m7OWXtbiXX8",
                "duration_minutes": 45,
                "xp_reward": 75
            },
            {
                "course_id": courses[1].id,
                "title": "State and Hooks",
                "content": """# State and Hooks in React

## What is State?

State is data that changes over time in your component. Unlike props, state is managed within the component.

## useState Hook

The most important Hook for managing state in function components.

### Basic Usage

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

### Multiple State Variables

```jsx
function UserForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState(0);
  
  return (
    <form>
      <input 
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input 
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input 
        type="number"
        value={age}
        onChange={(e) => setAge(e.target.value)}
        placeholder="Age"
      />
    </form>
  );
}
```

## useEffect Hook

Perform side effects in function components (data fetching, subscriptions, etc.)

### Basic Usage

```jsx
import { useState, useEffect } from 'react';

function DataFetcher() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch('https://api.example.com/data')
      .then(res => res.json())
      .then(data => {
        setData(data);
        setLoading(false);
      });
  }, []); // Empty array = run once on mount
  
  if (loading) return <p>Loading...</p>;
  return <div>{JSON.stringify(data)}</div>;
}
```

### Dependency Array

```jsx
function SearchResults({ query }) {
  const [results, setResults] = useState([]);
  
  useEffect(() => {
    // This runs whenever 'query' changes
    fetch(`/api/search?q=${query}`)
      .then(res => res.json())
      .then(setResults);
  }, [query]); // Re-run when query changes
  
  return <div>{/* render results */}</div>;
}
```

### Cleanup Function

```jsx
useEffect(() => {
  const timer = setInterval(() => {
    console.log('Tick');
  }, 1000);
  
  // Cleanup function
  return () => {
    clearInterval(timer);
  };
}, []);
```

## Other Important Hooks

### useContext

Share data without passing props.

```jsx
import { createContext, useContext } from 'react';

const ThemeContext = createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  const theme = useContext(ThemeContext);
  return <div className={theme}>Toolbar</div>;
}
```

### useRef

Access DOM elements or persist values.

```jsx
import { useRef } from 'react';

function TextInput() {
  const inputRef = useRef(null);
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  return (
    <>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus Input</button>
    </>
  );
}
```

## Practical Example: Todo App

```jsx
import { useState } from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');
  
  const addTodo = () => {
    if (input.trim()) {
      setTodos([...todos, { id: Date.now(), text: input, done: false }]);
      setInput('');
    }
  };
  
  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, done: !todo.done } : todo
    ));
  };
  
  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };
  
  return (
    <div>
      <h1>Todo List</h1>
      <input 
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && addTodo()}
      />
      <button onClick={addTodo}>Add</button>
      
      <ul>
        {todos.map(todo => (
          <li key={todo.id}>
            <input 
              type="checkbox"
              checked={todo.done}
              onChange={() => toggleTodo(todo.id)}
            />
            <span style={{ textDecoration: todo.done ? 'line-through' : 'none' }}>
              {todo.text}
            </span>
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

Hooks make React components powerful and flexible! 🎣""",
                "order": 3,
                "video_url": "https://www.youtube.com/embed/O6P86uwfdR0",
                "duration_minutes": 60,
                "xp_reward": 100
            }
        ]
        
        for lesson_data in react_lessons:
            lesson = Lesson(**lesson_data)
            db.add(lesson)
            lessons.append(lesson)
        
        db.commit()
        
        # Create Lessons for Data Science Course
        data_science_lessons = [
            {
                "course_id": courses[2].id,
                "title": "Introduction to Data Science",
                "content": """# Welcome to Data Science! 📊

## What is Data Science?

Data Science is an interdisciplinary field that uses scientific methods, algorithms, and systems to extract knowledge and insights from structured and unstructured data.

## Why Learn Data Science?

1. **High Demand**: Data scientists are among the most sought-after professionals
2. **Impactful**: Make data-driven decisions that affect millions
3. **Versatile**: Apply to healthcare, finance, marketing, sports, and more
4. **Lucrative**: High-paying career opportunities
5. **Future-Proof**: Data is the new oil

## Key Components

### 1. Statistics & Mathematics
- Probability theory
- Statistical inference
- Linear algebra
- Calculus

### 2. Programming
- Python (NumPy, Pandas, Scikit-learn)
- R
- SQL

### 3. Machine Learning
- Supervised learning
- Unsupervised learning
- Deep learning

### 4. Data Visualization
- Matplotlib
- Seaborn
- Plotly
- Tableau

## The Data Science Process

```
1. Define the Problem
   ↓
2. Collect Data
   ↓
3. Clean & Prepare Data
   ↓
4. Explore Data (EDA)
   ↓
5. Build Models
   ↓
6. Evaluate Results
   ↓
7. Deploy & Monitor
```

## Essential Python Libraries

### NumPy
```python
import numpy as np

# Create array
arr = np.array([1, 2, 3, 4, 5])
print(arr.mean())  # 3.0
```

### Pandas
```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'salary': [50000, 60000, 70000]
})
print(df.head())
```

### Matplotlib
```python
import matplotlib.pyplot as plt

# Simple plot
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('My First Plot')
plt.show()
```

## Types of Data

### Structured Data
- Organized in rows and columns
- Examples: Excel files, SQL databases

### Unstructured Data
- No predefined format
- Examples: Text, images, videos

### Semi-Structured Data
- Some organization but not fully structured
- Examples: JSON, XML

## Real-World Applications

1. **Healthcare**: Disease prediction, drug discovery
2. **Finance**: Fraud detection, risk assessment
3. **E-commerce**: Recommendation systems, price optimization
4. **Social Media**: Sentiment analysis, trend prediction
5. **Transportation**: Route optimization, autonomous vehicles

## Getting Started

```python
# Install essential libraries
pip install numpy pandas matplotlib seaborn scikit-learn jupyter
```

## Your First Data Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('sales_data.csv')

# Basic statistics
print(data.describe())

# Visualize
data['sales'].plot(kind='hist')
plt.title('Sales Distribution')
plt.show()
```

## Skills You'll Develop

- Data cleaning and preprocessing
- Statistical analysis
- Machine learning
- Data visualization
- Communication of insights

Start your journey into the world of data! 🚀""",
                "order": 1,
                "video_url": "https://www.youtube.com/embed/ua-CiDNNj30",
                "duration_minutes": 40,
                "xp_reward": 50
            },
            {
                "course_id": courses[2].id,
                "title": "Data Analysis with Pandas",
                "content": """# Data Analysis with Pandas 🐼

## What is Pandas?

Pandas is a powerful Python library for data manipulation and analysis. It provides data structures and functions needed to work with structured data.

## Core Data Structures

### Series (1D)

```python
import pandas as pd

# Create a Series
s = pd.Series([1, 2, 3, 4, 5])
print(s)

# Series with custom index
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s['a'])  # 10
```

### DataFrame (2D)

```python
# Create DataFrame from dictionary
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'age': [25, 30, 35, 28],
    'city': ['NYC', 'LA', 'Chicago', 'Houston'],
    'salary': [70000, 80000, 90000, 75000]
})
print(df)
```

## Reading Data

```python
# Read CSV
df = pd.read_csv('data.csv')

# Read Excel
df = pd.read_excel('data.xlsx')

# Read JSON
df = pd.read_json('data.json')

# Read from URL
url = 'https://example.com/data.csv'
df = pd.read_csv(url)
```

## Exploring Data

```python
# First few rows
df.head()

# Last few rows
df.tail()

# Shape (rows, columns)
df.shape

# Column names
df.columns

# Data types
df.dtypes

# Summary statistics
df.describe()

# Info about DataFrame
df.info()
```

## Selecting Data

```python
# Select single column
df['name']

# Select multiple columns
df[['name', 'age']]

# Select rows by index
df.iloc[0]  # First row
df.iloc[0:3]  # First 3 rows

# Select by label
df.loc[0, 'name']

# Conditional selection
df[df['age'] > 30]
df[df['city'] == 'NYC']
df[(df['age'] > 25) & (df['salary'] > 75000)]
```

## Data Manipulation

### Adding Columns

```python
# New column
df['bonus'] = df['salary'] * 0.1

# Calculated column
df['total_comp'] = df['salary'] + df['bonus']
```

### Modifying Data

```python
# Update values
df.loc[df['age'] < 30, 'category'] = 'Young'
df.loc[df['age'] >= 30, 'category'] = 'Experienced'

# Replace values
df['city'].replace('NYC', 'New York', inplace=True)
```

### Deleting Data

```python
# Drop column
df.drop('bonus', axis=1, inplace=True)

# Drop row
df.drop(0, axis=0, inplace=True)

# Drop rows with missing values
df.dropna()
```

## Handling Missing Data

```python
# Check for missing values
df.isnull().sum()

# Fill missing values
df['age'].fillna(df['age'].mean(), inplace=True)

# Drop rows with any missing values
df.dropna()

# Drop columns with any missing values
df.dropna(axis=1)
```

## Grouping and Aggregation

```python
# Group by single column
df.groupby('city')['salary'].mean()

# Group by multiple columns
df.groupby(['city', 'category'])['salary'].sum()

# Multiple aggregations
df.groupby('city').agg({
    'salary': ['mean', 'min', 'max'],
    'age': 'mean'
})
```

## Sorting

```python
# Sort by single column
df.sort_values('age')

# Sort descending
df.sort_values('salary', ascending=False)

# Sort by multiple columns
df.sort_values(['city', 'age'])
```

## Merging DataFrames

```python
# Merge (like SQL JOIN)
df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
df2 = pd.DataFrame({'id': [1, 2, 3], 'score': [90, 85, 95]})

merged = pd.merge(df1, df2, on='id')
```

## Practical Example: Sales Analysis

```python
import pandas as pd

# Load sales data
sales = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
    'product': ['A', 'B', 'A'],
    'quantity': [10, 15, 8],
    'price': [100, 150, 100]
})

# Convert date to datetime
sales['date'] = pd.to_datetime(sales['date'])

# Calculate revenue
sales['revenue'] = sales['quantity'] * sales['price']

# Total revenue by product
product_revenue = sales.groupby('product')['revenue'].sum()
print(product_revenue)

# Daily statistics
daily_stats = sales.groupby('date').agg({
    'quantity': 'sum',
    'revenue': 'sum'
})
print(daily_stats)
```

## Exporting Data

```python
# Save to CSV
df.to_csv('output.csv', index=False)

# Save to Excel
df.to_excel('output.xlsx', index=False)

# Save to JSON
df.to_json('output.json')
```

Pandas makes data analysis efficient and enjoyable! 📈""",
                "order": 2,
                "video_url": "https://www.youtube.com/embed/vmEHCJofslg",
                "duration_minutes": 55,
                "xp_reward": 75
            },
            {
                "course_id": courses[2].id,
                "title": "Data Visualization",
                "content": """# Data Visualization with Python 📊

## Why Visualize Data?

- **Understand patterns**: See trends and outliers
- **Communicate insights**: Pictures speak louder than numbers
- **Make decisions**: Visual data aids decision-making
- **Tell stories**: Engage your audience

## Matplotlib Basics

### Simple Line Plot

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Simple Line Plot')
plt.grid(True)
plt.show()
```

### Multiple Lines

```python
x = [1, 2, 3, 4, 5]
y1 = [1, 4, 9, 16, 25]
y2 = [1, 2, 3, 4, 5]

plt.plot(x, y1, label='Quadratic', color='blue', linewidth=2)
plt.plot(x, y2, label='Linear', color='red', linestyle='--')
plt.legend()
plt.title('Multiple Lines')
plt.show()
```

### Scatter Plot

```python
import numpy as np

x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = 1000 * np.random.rand(50)

plt.scatter(x, y, c=colors, s=sizes, alpha=0.5, cmap='viridis')
plt.colorbar()
plt.title('Scatter Plot')
plt.show()
```

### Bar Chart

```python
categories = ['A', 'B', 'C', 'D']
values = [23, 45, 56, 78]

plt.bar(categories, values, color='skyblue')
plt.xlabel('Category')
plt.ylabel('Value')
plt.title('Bar Chart')
plt.show()
```

### Histogram

```python
data = np.random.randn(1000)

plt.hist(data, bins=30, color='green', alpha=0.7, edgecolor='black')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.show()
```

### Pie Chart

```python
sizes = [30, 25, 20, 25]
labels = ['A', 'B', 'C', 'D']
colors = ['gold', 'lightblue', 'lightgreen', 'pink']
explode = (0.1, 0, 0, 0)  # Explode first slice

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.title('Pie Chart')
plt.show()
```

## Seaborn - Statistical Visualization

```python
import seaborn as sns
import pandas as pd

# Set style
sns.set_style('whitegrid')

# Load sample data
tips = sns.load_dataset('tips')
```

### Distribution Plot

```python
sns.histplot(tips['total_bill'], kde=True)
plt.title('Distribution of Total Bill')
plt.show()
```

### Box Plot

```python
sns.boxplot(x='day', y='total_bill', data=tips)
plt.title('Total Bill by Day')
plt.show()
```

### Violin Plot

```python
sns.violinplot(x='day', y='total_bill', data=tips)
plt.title('Total Bill Distribution by Day')
plt.show()
```

### Heatmap

```python
# Correlation matrix
corr = tips.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.show()
```

### Pair Plot

```python
sns.pairplot(tips, hue='sex')
plt.show()
```

## Subplots

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1
axes[0, 0].plot([1, 2, 3], [1, 4, 9])
axes[0, 0].set_title('Plot 1')

# Plot 2
axes[0, 1].scatter([1, 2, 3], [1, 4, 9])
axes[0, 1].set_title('Plot 2')

# Plot 3
axes[1, 0].bar(['A', 'B', 'C'], [10, 20, 15])
axes[1, 0].set_title('Plot 3')

# Plot 4
axes[1, 1].hist(np.random.randn(100), bins=20)
axes[1, 1].set_title('Plot 4')

plt.tight_layout()
plt.show()
```

## Practical Example: Sales Dashboard

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample sales data
sales_data = pd.DataFrame({
    'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    'revenue': [45000, 52000, 48000, 61000, 58000, 67000],
    'expenses': [30000, 32000, 31000, 38000, 36000, 40000],
    'customers': [120, 135, 128, 152, 148, 165]
})

# Calculate profit
sales_data['profit'] = sales_data['revenue'] - sales_data['expenses']

# Create dashboard
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Sales Dashboard', fontsize=16, fontweight='bold')

# Revenue vs Expenses
axes[0, 0].plot(sales_data['month'], sales_data['revenue'], 
                marker='o', label='Revenue', linewidth=2)
axes[0, 0].plot(sales_data['month'], sales_data['expenses'], 
                marker='s', label='Expenses', linewidth=2)
axes[0, 0].set_title('Revenue vs Expenses')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Profit by Month
axes[0, 1].bar(sales_data['month'], sales_data['profit'], color='green', alpha=0.7)
axes[0, 1].set_title('Monthly Profit')
axes[0, 1].set_ylabel('Profit ($)')

# Customer Growth
axes[1, 0].plot(sales_data['month'], sales_data['customers'], 
                marker='D', color='purple', linewidth=2)
axes[1, 0].set_title('Customer Growth')
axes[1, 0].set_ylabel('Number of Customers')
axes[1, 0].grid(True, alpha=0.3)

# Revenue Distribution
axes[1, 1].pie(sales_data['revenue'], labels=sales_data['month'], 
               autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('Revenue Distribution')

plt.tight_layout()
plt.show()
```

## Best Practices

1. **Choose the right chart type**
   - Line: Trends over time
   - Bar: Comparisons
   - Scatter: Relationships
   - Pie: Proportions
   - Histogram: Distributions

2. **Keep it simple**: Don't overcomplicate
3. **Use colors wisely**: Meaningful and accessible
4. **Label everything**: Axes, titles, legends
5. **Tell a story**: Guide the viewer's attention

Visualize data to unlock insights! 🎨""",
                "order": 3,
                "video_url": "https://www.youtube.com/embed/DAQNHzOcO5A",
                "duration_minutes": 50,
                "xp_reward": 100
            }
        ]
        
        for lesson_data in data_science_lessons:
            lesson = Lesson(**lesson_data)
            db.add(lesson)
            lessons.append(lesson)
        
        db.commit()
        
        # Create Lessons for Machine Learning Course
        ml_lessons = [
            {
                "course_id": courses[3].id,
                "title": "Introduction to Machine Learning",
                "content": """# Welcome to Machine Learning! 🤖

## What is Machine Learning?

Machine Learning (ML) is a subset of Artificial Intelligence that enables computers to learn from data without being explicitly programmed.

## Types of Machine Learning

### 1. Supervised Learning
Learn from labeled data to make predictions.

**Examples:**
- Email spam detection
- House price prediction
- Image classification

```python
from sklearn.linear_model import LinearRegression

# Training data
X = [[1], [2], [3], [4], [5]]
y = [2, 4, 6, 8, 10]

# Create and train model
model = LinearRegression()
model.fit(X, y)

# Make prediction
prediction = model.predict([[6]])
print(prediction)  # ~12
```

### 2. Unsupervised Learning
Find patterns in unlabeled data.

**Examples:**
- Customer segmentation
- Anomaly detection
- Recommendation systems

```python
from sklearn.cluster import KMeans

# Data points
X = [[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]]

# Create clusters
kmeans = KMeans(n_clusters=2)
kmeans.fit(X)

# Get cluster labels
labels = kmeans.labels_
print(labels)
```

### 3. Reinforcement Learning
Learn through trial and error with rewards.

**Examples:**
- Game playing (AlphaGo)
- Robotics
- Self-driving cars

## The ML Workflow

```
1. Define Problem
   ↓
2. Collect Data
   ↓
3. Prepare Data
   ↓
4. Choose Model
   ↓
5. Train Model
   ↓
6. Evaluate Model
   ↓
7. Tune Parameters
   ↓
8. Deploy Model
```

## Key Concepts

### Features and Labels

```python
# Features (X): Input variables
# Labels (y): Output variable

import pandas as pd

data = pd.DataFrame({
    'size': [1500, 2000, 1800, 2200],  # Features
    'bedrooms': [3, 4, 3, 4],          # Features
    'price': [300000, 400000, 350000, 450000]  # Label
})

X = data[['size', 'bedrooms']]  # Features
y = data['price']                # Labels
```

### Training and Testing

```python
from sklearn.model_selection import train_test_split

# Split data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### Model Evaluation

```python
from sklearn.metrics import mean_squared_error, r2_score

# Make predictions
y_pred = model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'MSE: {mse}')
print(f'R²: {r2}')
```

## Common Algorithms

### 1. Linear Regression
Predict continuous values.

```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### 2. Logistic Regression
Binary classification.

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### 3. Decision Trees
Classification and regression.

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### 4. Random Forest
Ensemble of decision trees.

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

### 5. K-Nearest Neighbors
Classification based on similarity.

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

## Practical Example: Iris Classification

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load data
iris = load_iris()
X, y = iris.data, iris.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print(classification_report(y_test, y_pred, target_names=iris.target_names))
```

## Essential Libraries

- **Scikit-learn**: ML algorithms
- **TensorFlow**: Deep learning
- **PyTorch**: Deep learning
- **Keras**: High-level neural networks
- **XGBoost**: Gradient boosting

## Real-World Applications

1. **Healthcare**: Disease diagnosis, drug discovery
2. **Finance**: Fraud detection, algorithmic trading
3. **E-commerce**: Product recommendations
4. **Transportation**: Route optimization, autonomous vehicles
5. **Entertainment**: Content recommendations (Netflix, Spotify)

## Getting Started

```bash
# Install essential libraries
pip install scikit-learn numpy pandas matplotlib
```

Start building intelligent systems! 🚀""",
                "order": 1,
                "video_url": "https://www.youtube.com/embed/ukzFI9rgwfU",
                "duration_minutes": 45,
                "xp_reward": 50
            },
            {
                "course_id": courses[3].id,
                "title": "Classification Algorithms",
                "content": """# Classification Algorithms 🎯

## What is Classification?

Classification is a supervised learning task where the goal is to predict discrete class labels.

## Binary vs Multi-class Classification

### Binary Classification
Two possible outcomes (Yes/No, True/False, 0/1)

**Examples:**
- Email: Spam or Not Spam
- Medical: Disease or No Disease
- Finance: Fraud or Legitimate

### Multi-class Classification
More than two possible outcomes

**Examples:**
- Digit recognition (0-9)
- Animal classification (cat, dog, bird)
- Sentiment analysis (positive, neutral, negative)

## Logistic Regression

Despite its name, it's used for classification!

```python
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Generate sample data
X, y = make_classification(n_samples=1000, n_features=20, 
                          n_classes=2, random_state=42)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:')
print(cm)
```

## Decision Trees

Tree-like model of decisions.

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt

# Train model
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Visualize tree
plt.figure(figsize=(20,10))
tree.plot_tree(model, filled=True, feature_names=[f'Feature {i}' for i in range(20)])
plt.show()

# Feature importance
importances = model.feature_importances_
print('Feature Importances:', importances)
```

## Random Forest

Ensemble of decision trees.

```python
from sklearn.ensemble import RandomForestClassifier

# Train model
model = RandomForestClassifier(
    n_estimators=100,  # Number of trees
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

# Predict with probability
y_pred_proba = model.predict_proba(X_test)
print('Prediction probabilities:', y_pred_proba[:5])

# Feature importance
importances = model.feature_importances_
```

## Support Vector Machines (SVM)

Find the best boundary between classes.

```python
from sklearn.svm import SVC

# Train model
model = SVC(kernel='rbf', C=1.0, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'SVM Accuracy: {accuracy:.2f}')
```

## K-Nearest Neighbors (KNN)

Classify based on nearest neighbors.

```python
from sklearn.neighbors import KNeighborsClassifier

# Train model
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Try different k values
for k in [3, 5, 7, 9]:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    score = knn.score(X_test, y_test)
    print(f'k={k}, Accuracy: {score:.2f}')
```

## Naive Bayes

Based on Bayes' theorem.

```python
from sklearn.naive_bayes import GaussianNB

# Train model
model = GaussianNB()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Naive Bayes Accuracy: {accuracy:.2f}')
```

## Model Evaluation Metrics

### Accuracy

```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
```

### Precision, Recall, F1-Score

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred))
```

### Confusion Matrix

```python
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
```

### ROC Curve and AUC

```python
from sklearn.metrics import roc_curve, auc

# Get prediction probabilities
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

## Practical Example: Titanic Survival Prediction

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Sample Titanic data
data = pd.DataFrame({
    'Pclass': [3, 1, 3, 1, 3, 3, 1, 3],
    'Sex': [1, 0, 0, 0, 1, 1, 0, 1],  # 1=male, 0=female
    'Age': [22, 38, 26, 35, 35, 27, 54, 2],
    'Fare': [7.25, 71.28, 7.92, 53.10, 8.05, 8.46, 51.86, 10.46],
    'Survived': [0, 1, 1, 1, 0, 0, 1, 1]
})

# Features and target
X = data[['Pclass', 'Sex', 'Age', 'Fare']]
y = data['Survived']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print('Accuracy:', accuracy_score(y_test, y_pred))
print('\\nClassification Report:')
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print('\\nFeature Importance:')
print(feature_importance)
```

## Cross-Validation

```python
from sklearn.model_selection import cross_val_score

# 5-fold cross-validation
scores = cross_val_score(model, X, y, cv=5)
print(f'Cross-validation scores: {scores}')
print(f'Mean accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})')
```

## Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

# Grid search
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy'
)

grid_search.fit(X_train, y_train)

print('Best parameters:', grid_search.best_params_)
print('Best score:', grid_search.best_score_)
```

Master classification to solve real-world problems! 🎓""",
                "order": 2,
                "video_url": "https://www.youtube.com/embed/7eh4d6sabA0",
                "duration_minutes": 60,
                "xp_reward": 75
            },
            {
                "course_id": courses[3].id,
                "title": "Model Evaluation and Optimization",
                "content": """# Model Evaluation and Optimization 🎯

## Why Evaluate Models?

- **Measure performance**: How well does the model work?
- **Compare models**: Which algorithm is best?
- **Avoid overfitting**: Ensure generalization
- **Build confidence**: Trust your predictions

## Train-Test Split

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% for testing
    random_state=42,    # Reproducibility
    stratify=y          # Maintain class distribution
)

print(f'Training set: {len(X_train)} samples')
print(f'Test set: {len(X_test)} samples')
```

## Cross-Validation

More robust than single train-test split.

### K-Fold Cross-Validation

```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)

# 5-fold cross-validation
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f'Scores: {scores}')
print(f'Mean: {scores.mean():.3f}')
print(f'Std: {scores.std():.3f}')
```

### Stratified K-Fold

Maintains class distribution in each fold.

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for train_idx, test_idx in skf.split(X, y):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    # Train and evaluate model
```

## Evaluation Metrics

### Classification Metrics

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Make predictions
y_pred = model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print(f'Accuracy: {accuracy:.3f}')
print(f'Precision: {precision:.3f}')
print(f'Recall: {recall:.3f}')
print(f'F1-Score: {f1:.3f}')

# Detailed report
print('\\nClassification Report:')
print(classification_report(y_test, y_pred))
```

### Confusion Matrix

```python
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
```

### ROC Curve and AUC

```python
from sklearn.metrics import roc_curve, roc_auc_score

# Get probabilities
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
auc_score = roc_auc_score(y_test, y_pred_proba)

# Plot
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'AUC = {auc_score:.3f}')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## Hyperparameter Tuning

### Grid Search

Exhaustive search over parameter grid.

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Create grid search
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,  # Use all CPU cores
    verbose=1
)

# Fit
grid_search.fit(X_train, y_train)

# Best parameters
print('Best parameters:', grid_search.best_params_)
print('Best score:', grid_search.best_score_)

# Use best model
best_model = grid_search.best_estimator_
```

### Random Search

Faster alternative to grid search.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

# Define parameter distributions
param_dist = {
    'n_estimators': randint(50, 500),
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10)
}

# Random search
random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions=param_dist,
    n_iter=100,  # Number of parameter settings sampled
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)

print('Best parameters:', random_search.best_params_)
print('Best score:', random_search.best_score_)
```

## Feature Scaling

Important for many algorithms.

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Standardization (mean=0, std=1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Normalization (range 0-1)
scaler = MinMaxScaler()
X_train_normalized = scaler.fit_transform(X_train)
X_test_normalized = scaler.transform(X_test)
```

## Feature Selection

Select most important features.

```python
from sklearn.feature_selection import SelectKBest, f_classif

# Select top 10 features
selector = SelectKBest(f_classif, k=10)
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)

# Get selected feature indices
selected_features = selector.get_support(indices=True)
print('Selected features:', selected_features)
```

## Handling Imbalanced Data

### Class Weights

```python
from sklearn.ensemble import RandomForestClassifier

# Automatically balance classes
model = RandomForestClassifier(
    class_weight='balanced',
    random_state=42
)
model.fit(X_train, y_train)
```

### SMOTE (Synthetic Minority Over-sampling)

```python
from imblearn.over_sampling import SMOTE

# Apply SMOTE
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

print(f'Original: {len(y_train)}')
print(f'After SMOTE: {len(y_train_balanced)}')
```

## Learning Curves

Diagnose overfitting/underfitting.

```python
from sklearn.model_selection import learning_curve

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5,
    scoring='accuracy'
)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_scores.mean(axis=1), label='Training score')
plt.plot(train_sizes, val_scores.mean(axis=1), label='Validation score')
plt.xlabel('Training Set Size')
plt.ylabel('Accuracy')
plt.title('Learning Curves')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## Practical Example: Complete Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Parameter grid
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [5, 10, 15],
    'classifier__min_samples_split': [2, 5, 10]
}

# Grid search
grid_search = GridSearchCV(
    pipeline,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1
)

# Fit
grid_search.fit(X_train, y_train)

# Evaluate
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print('Best parameters:', grid_search.best_params_)
print('Test accuracy:', accuracy_score(y_test, y_pred))
print('\\nClassification Report:')
print(classification_report(y_test, y_pred))
```

## Model Persistence

Save and load models.

```python
import joblib

# Save model
joblib.dump(best_model, 'best_model.pkl')

# Load model
loaded_model = joblib.load('best_model.pkl')

# Use loaded model
predictions = loaded_model.predict(X_new)
```

## Best Practices

1. **Always use cross-validation** for robust evaluation
2. **Scale features** when using distance-based algorithms
3. **Handle imbalanced data** appropriately
4. **Tune hyperparameters** systematically
5. **Monitor for overfitting** using validation curves
6. **Use pipelines** for reproducible workflows
7. **Save models** for deployment

Build robust and optimized models! 🚀""",
                "order": 3,
                "video_url": "https://www.youtube.com/embed/Gol_qOgRqfA",
                "duration_minutes": 65,
                "xp_reward": 100
            }
        ]
        
        for lesson_data in ml_lessons:
            lesson = Lesson(**lesson_data)
            db.add(lesson)
            lessons.append(lesson)
        
        db.commit()
        
        # Create Quizzes (use the first lesson)
        quiz1 = Quiz(
            lesson_id=lessons[0].id,
            title="Python Basics Quiz",
            description="Test your knowledge of Python fundamentals",
            passing_score=70,
            time_limit_minutes=15,
            xp_reward=100
        )
        db.add(quiz1)
        db.commit()
        
        # Create Quiz Questions
        questions_data = [
            {
                "quiz_id": quiz1.id,
                "question_text": "What is Python?",
                "question_type": "multiple_choice",
                "points": 10,
                "order": 1
            },
            {
                "quiz_id": quiz1.id,
                "question_text": "Which keyword is used to define a function in Python?",
                "question_type": "multiple_choice",
                "points": 10,
                "order": 2
            },
            {
                "quiz_id": quiz1.id,
                "question_text": "What is the correct file extension for Python files?",
                "question_type": "multiple_choice",
                "points": 10,
                "order": 3
            },
            {
                "quiz_id": quiz1.id,
                "question_text": "Which of the following is a mutable data type in Python?",
                "question_type": "multiple_choice",
                "points": 10,
                "order": 4
            },
            {
                "quiz_id": quiz1.id,
                "question_text": "What does the 'print()' function do?",
                "question_type": "multiple_choice",
                "points": 10,
                "order": 5
            },
            {
                "quiz_id": quiz1.id,
                "question_text": "Which operator is used for exponentiation in Python?",
                "question_type": "multiple_choice",
                "points": 10,
                "order": 6
            },
            {
                "quiz_id": quiz1.id,
                "question_text": "What is the output of: print(type(5.0))?",
                "question_type": "multiple_choice",
                "points": 10,
                "order": 7
            },
            {
                "quiz_id": quiz1.id,
                "question_text": "Which statement is used to exit a loop prematurely?",
                "question_type": "multiple_choice",
                "points": 10,
                "order": 8
            }
        ]
        
        questions = []
        for q_data in questions_data:
            question = QuizQuestion(**q_data)
            db.add(question)
            questions.append(question)
        
        db.commit()
        
        # Create Quiz Options (use actual question IDs)
        options_data = [
            # Question 1: What is Python?
            {"question_id": questions[0].id, "option_text": "A programming language", "is_correct": True, "order": 1},
            {"question_id": questions[0].id, "option_text": "A snake", "is_correct": False, "order": 2},
            {"question_id": questions[0].id, "option_text": "A database", "is_correct": False, "order": 3},
            {"question_id": questions[0].id, "option_text": "An operating system", "is_correct": False, "order": 4},
            
            # Question 2: Which keyword is used to define a function?
            {"question_id": questions[1].id, "option_text": "def", "is_correct": True, "order": 1},
            {"question_id": questions[1].id, "option_text": "function", "is_correct": False, "order": 2},
            {"question_id": questions[1].id, "option_text": "func", "is_correct": False, "order": 3},
            {"question_id": questions[1].id, "option_text": "define", "is_correct": False, "order": 4},
            
            # Question 3: File extension
            {"question_id": questions[2].id, "option_text": ".py", "is_correct": True, "order": 1},
            {"question_id": questions[2].id, "option_text": ".python", "is_correct": False, "order": 2},
            {"question_id": questions[2].id, "option_text": ".pt", "is_correct": False, "order": 3},
            {"question_id": questions[2].id, "option_text": ".pyt", "is_correct": False, "order": 4},
            
            # Question 4: Mutable data type
            {"question_id": questions[3].id, "option_text": "List", "is_correct": True, "order": 1},
            {"question_id": questions[3].id, "option_text": "Tuple", "is_correct": False, "order": 2},
            {"question_id": questions[3].id, "option_text": "String", "is_correct": False, "order": 3},
            {"question_id": questions[3].id, "option_text": "Integer", "is_correct": False, "order": 4},
            
            # Question 5: print() function
            {"question_id": questions[4].id, "option_text": "Displays output to the console", "is_correct": True, "order": 1},
            {"question_id": questions[4].id, "option_text": "Reads input from user", "is_correct": False, "order": 2},
            {"question_id": questions[4].id, "option_text": "Creates a new file", "is_correct": False, "order": 3},
            {"question_id": questions[4].id, "option_text": "Deletes a variable", "is_correct": False, "order": 4},
            
            # Question 6: Exponentiation operator
            {"question_id": questions[5].id, "option_text": "**", "is_correct": True, "order": 1},
            {"question_id": questions[5].id, "option_text": "^", "is_correct": False, "order": 2},
            {"question_id": questions[5].id, "option_text": "exp", "is_correct": False, "order": 3},
            {"question_id": questions[5].id, "option_text": "pow", "is_correct": False, "order": 4},
            
            # Question 7: type(5.0)
            {"question_id": questions[6].id, "option_text": "<class 'float'>", "is_correct": True, "order": 1},
            {"question_id": questions[6].id, "option_text": "<class 'int'>", "is_correct": False, "order": 2},
            {"question_id": questions[6].id, "option_text": "<class 'double'>", "is_correct": False, "order": 3},
            {"question_id": questions[6].id, "option_text": "<class 'number'>", "is_correct": False, "order": 4},
            
            # Question 8: Exit loop
            {"question_id": questions[7].id, "option_text": "break", "is_correct": True, "order": 1},
            {"question_id": questions[7].id, "option_text": "exit", "is_correct": False, "order": 2},
            {"question_id": questions[7].id, "option_text": "stop", "is_correct": False, "order": 3},
            {"question_id": questions[7].id, "option_text": "continue", "is_correct": False, "order": 4},
        ]
        
        for opt_data in options_data:
            option = QuizOption(**opt_data)
            db.add(option)
        
        db.commit()
        
        # Create Badges
        badges_data = [
            {
                "name": "First Steps",
                "description": "Complete your first lesson",
                "icon": "🎯",
                "criteria": "complete_first_lesson",
                "xp_reward": 50
            },
            {
                "name": "Quiz Master",
                "description": "Score 100% on any quiz",
                "icon": "🏆",
                "criteria": "perfect_quiz_score",
                "xp_reward": 100
            },
            {
                "name": "Course Completer",
                "description": "Complete an entire course",
                "icon": "🎓",
                "criteria": "complete_course",
                "xp_reward": 200
            },
            {
                "name": "Streak Champion",
                "description": "Maintain a 7-day learning streak",
                "icon": "🔥",
                "criteria": "7_day_streak",
                "xp_reward": 150
            }
        ]
        
        for badge_data in badges_data:
            badge = Badge(**badge_data)
            db.add(badge)
        
        db.commit()
        
        print("✅ Database seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()