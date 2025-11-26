import json
import os.path

from unicodedata import category


class Grade:

    def __init__(self):
        self.students = {}
        self.load_grades()

    def save_grade(self):
        grade = {"Students": self.students}
        with open("grade_app.json", "w") as file:
            json.dump(grade, file, indent=3)


    def load_grades(self):
        try:
            if os.path.exists("grade_app.json"):
                with open("grade_app.json", "r") as file:
                    grade = json.load(file)
                    self.students = grade.get("Students", {})

            else:
                self.students = {}

        except FileNotFoundError:
            print("No records of Students and grades yet. \n Add students with grade and save to automatically create the file")


    def add_student(self, name, grade):
        self.students[name] = grade
        self.save_grade()

    def view_grades(self):
        if not self.students:
            print("No grade records yet.")
        else:
            arranged = sorted(self.students.items(), key=lambda x: x[1], reverse=True)

            for student, grade in arranged:
                category = self.get_category()
                print(f"{student} : {grade} ({category})")

    def update_grade(self, name, new_grade):
        if name in self.students:
            self.students[name] = new_grade
            self.save_grade()
            print(f"{name}'s grade updated to {new_grade}.")
        else:
            print(f"{name} not found.")

    def search(self, query):
        query = query.lower
        found = False

        for student, grade in self.students.items():
            if query in student.lower:
                print(f"{student}: {grade}")
                found = True

        if not found:
            print("There's no name as such here.")

    def average_score(self):
        total = sum(self.students.values())
        count = len(self.students)

        average = total / count
        print(f"The class average is: {average:.2f}")

    def delete_student(self, name):
        if name in self.students:
            del self.students[name]
            self.save_grade()
            print(f"{name} has been removed from the gradebook.")
        else:
            print(f"{name} not found.")

    def get_category(self, grade):
        if grade >= 80:
            return "A"
        elif grade >= 70:
            return "B"
        elif grade >= 60:
            return "C"
        elif grade >= 50:
            return "D"
        else:
            return "F"

    def top_student(self):
        if not self.students:
            print("No grade records yet.")
            return

        top = max(self.students.items(), key=lambda x: x[1])
        print(f"Top student: {top[0]} with {top[1]}")

    def lowest(self):
        if not self.students:
            print("No grade records yet.")
            return

        low = min(self.students.items(), key=lambda x: x[1])
        print(f"Lowest Student: {low[0]} with {low[1]}")

    def generate_report(self):
        if not self.students:
            print("No grade records to generate report.")
            return

        arranged = sorted(self.students.items(), key=lambda x: x[1], reverse=True)

        with open("class_report.txt", "w") as file:
            file.write("===== CLASS REPORT =====\n")
            file.write("\n")

            file.write("Student Grades (High --> Low):\n")
            for name, grade in arranged:
                category = self.get_category(grade)
                file.write(f"{name} : {grade} ({category})\n")

            file.write("\n")

            avg = sum(self.students.values()) / len(self.students)
            file.write(f"Class Average: {avg:.2f}\n")

            top = max(self.students.items(), key=lambda x: x[1])
            file.write(f"Top Student: {top[0]} ({top[1]})\n")

            low = min(self.students.items(), key=lambda x: x[1])
            file.write(f"Lowest Student: {low[0]} ({low[1]})\n")

            file.write("\nReport Generated Successfully.\n")

        print("Class report saved as 'class_report.txt'.")
