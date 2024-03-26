import mysql.connector

class Employee:
    def __init__(self, name, emp_id, title, department):
        self.name = name
        self.emp_id = emp_id
        self.title = title
        self.department = department

    def display_details(self):
        print(f"Name: {self.name}\nID: {self.emp_id}\nTitle: {self.title}\nDepartment: {self.department}")

    def __str__(self):
        return f"{self.name} - {self.emp_id}"

class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, emp_id):
        self.employees = [employee for employee in self.employees if employee.emp_id != emp_id]

    def list_employees(self):
        if self.employees:
            print(f"Employees in department {self.name}:")
            for employee in self.employees:
                employee.display_details()
        else:
            print(f"No employees in department {self.name}.")

class Company:
    def __init__(self):
        self.departments = {}

    def add_department(self, department):
        self.departments[department.name] = department
        print("Department added successfully.")

    def remove_department(self, department_name):
        if department_name in self.departments:
            del self.departments[department_name]
            print("Department removed successfully.")
        else:
            print("Department not found.")

    def display_departments(self):
        if self.departments:
            print("Departments:")
            for department_name, department in self.departments.items():
                print(department_name)
        else:
            print("No departments.")

    # Your code...

def save_to_database(self):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql@123",
            database="emp_db"
        )

        cursor = db.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS departments (name VARCHAR(255))")
        cursor.execute("CREATE TABLE IF NOT EXISTS employees (name VARCHAR(255), emp_id INT, title VARCHAR(255), department VARCHAR(255))")

        cursor.execute("DELETE FROM departments")
        cursor.execute("DELETE FROM employees")

        for department_name in self.departments:
            cursor.execute("INSERT INTO departments (name) VALUES (%s)", (department_name,))

        for department in self.departments.values():
            for employee in department.employees:
                cursor.execute("INSERT INTO employees (name, emp_id, title, department) VALUES (%s, %s, %s, %s)",
                               (employee.name, employee.emp_id, employee.title, employee.department))

        db.commit()
        print("Data saved to database successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
def menu():
    print("Menu:")
    print("1. Add Employee")
    print("2. Remove Employee")
    print("3. List Employees in Department")
    print("4. Add Department")
    print("5. Remove Department")
    print("6. Display Departments")
    print("7. Exit")

def main():
    company = Company()

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter employee name: ")
            emp_id = int(input("Enter employee ID: "))
            title = input("Enter employee title: ")
            department_name = input("Enter department name: ")
            if department_name in company.departments:
                employee = Employee(name, emp_id, title, department_name)
                company.departments[department_name].add_employee(employee)
                print("Employee added successfully.")
            else:
                print("Department does not exist.")
        elif choice == '2':
            emp_id = int(input("Enter employee ID to remove: "))
            for department in company.departments.values():
                department.remove_employee(emp_id)
            print("Employee removed successfully.")
        elif choice == '3':
            department_name = input("Enter department name: ")
            if department_name in company.departments:
                company.departments[department_name].list_employees()
            else:
                print("Department does not exist.")
        elif choice == '4':
            department_name = input("Enter department name: ")
            department = Department(department_name)
            company.add_department(department)
        elif choice == '5':
            department_name = input("Enter department name to remove: ")
            company.remove_department(department_name)
            print("Department removed successfully.")
        elif choice == '6':
            company.display_departments()
        elif choice == '7':
            company.save_to_database()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            
            
if __name__ == "__main__":
    main()

