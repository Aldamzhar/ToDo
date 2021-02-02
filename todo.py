from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def day_tasks(day):
    rows = session.query(Table).filter(Table.deadline == day.date()).all()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for j in range(len(rows)):
            print(str(j+1) + ". " + str(rows[j]))


def week_tasks():
    today = datetime.today()
    for i in range(1,8):
        print("{} {} {}".format(today.strftime("%A"), today.day, today.strftime("%b")))
        day_tasks(today)
        print("")
        today += timedelta(days=1)


def add_task(task_input, task_deadline):
    new_row = Table(task=task_input, deadline=task_deadline)
    session.add(new_row)
    session.commit()


def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
    if len(rows) == 0:
        print("Nothing is missed!")
    else:
        for z in range(len(rows)):
            print(str(z+1) + ". " + str(rows[z]) + ".")


def menu():
    user_input = ""
    while True:
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) Missed tasks")
        print("4) Add task")
        print("5) Delete task")
        print("0) Exit")
        print("")
        user_input = input()
        
        if user_input == "1":
            print("Today {} {}:".format(datetime.today().day, datetime.today().strftime("%b")))
            day_tasks(datetime.today())
            print("")

        elif user_input == "2":
            week_tasks()
            print("")

        elif user_input == "3":
            missed_tasks()
            print("")

        elif user_input == "4":
            print("Enter task")
            task_input = input()
            print("Enter deadline")
            deadline_input = input()
            add_task(task_input, datetime.strptime(deadline_input,'%Y-%m-%d'))
            print("The task has been added")
            print("")

        elif user_input == "5":
            rows = session.query(Table).order_by(Table.deadline).all()
            if len(rows) == 0:
                print("No tasks to delete!")
                print("")
            else:
                for z in range(len(rows)):
                    print(str(z+1) + ". " + str(rows[z]) + ".")
                print("Choose the number of the task you want to delete:")
                deleted_task = input()
                session.delete(rows[int(deleted_task)-1])
                session.commit()
                print("The task has been deleted!")
                print("")

        elif user_input == "0":
            print("Bye!")
            break


menu()

