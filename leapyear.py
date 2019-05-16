import datetime
import calendar

def findDay(date): 
    born = datetime.datetime.strptime(date, '%d %m %Y').weekday()
    return (calendar.day_name[born])


def get_leap_year(n):
    m = 4
    q = int(n / m)

    n1 = m * q

    if((n * m) > 0) : 
        n2 = (m * (q + 1))
    else:
        n2 = (m * (q - 1))

    if (abs(n - n1) < abs(n - n2)):
        return n1

    return n2

def solve(year):
        if year % 4 == 0:
            print(findDay("29 2 " + str(year)))
        else:
            next_year = get_leap_year(year)
            print(("This is not a leap year\nClosest leap year: {}\n").format(next_year))
            print(findDay("29 2 " + str(next_year)))

if __name__ == "__main__":
    year = input("Enter the year: ")
    solve(year)
