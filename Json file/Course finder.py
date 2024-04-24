import datetime
import json

from buttons import CustomButton
from linebot.models.flex_message import FlexSendMessage
from linebot.models.sources import SourceGroup, SourceRoom
from QuickReply import add_quick_reply_custom

seasons_dict = {"spring": 0, "summer": 1, "fall": 2}
seasons_list = ["spring", "summer", "fall"]
gened_list = ['GA', 'GB', 'GD', 'GG', 'GQ', 'GS', 'GU', 'GW', 'GY', 'GZ']


def course_DB_init(conn, drop=False):
    with conn.cursor() as cur:
        try:
            cur.execute("show databases;")
            print(list(cur))
            cur.execute("select version();")
            print(list(cur))
            if drop:
                cur.execute("Drop Table Session")
                cur.execute("Drop Table Course")
                cur.execute("Drop Table Department")
                cur.execute("Drop Table Semester")

            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Semester (
                        semester VARCHAR(10) NOT NULL,
                        year YEAR(4) NOT NULL,
                        season VARCHAR(6) NOT NULL,
                        created DATE NOT NULL,
                        PRIMARY KEY (semester))
                        ENGINE = InnoDB;""")

            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Department (
                        department_name VARCHAR(125) NOT NULL,
                        PRIMARY KEY (department_name))
                        ENGINE = InnoDB;
                        """)

            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Course (
                        semester VARCHAR(10) NOT NULL,
                        course_id VARCHAR(45) NOT NULL,
                        department_name VARCHAR(125) NOT NULL,
                        course_number INT NOT NULL,
                        title VARCHAR(125) NOT NULL,
                        credits CHAR(1) NOT NULL,
                        gened CHAR(2) NULL,
                        special_info VARCHAR(125) NULL,
                        PRIMARY KEY (semester, course_id),
                        INDEX fk_Course_Department1_idx (department_name ASC) VISIBLE,
                        INDEX fk_Course_Semester1_idx (semester ASC) VISIBLE,
                        CONSTRAINT fk_Course_Department1
                            FOREIGN KEY (department_name)
                            REFERENCES Department (department_name)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION,
                        CONSTRAINT fk_Course_Semester1
                            FOREIGN KEY (semester)
                            REFERENCES Semester (semester)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION)
                        ENGINE = InnoDB;
                        """)

            cur.execute("""
                        CREATE TABLE IF NOT EXISTS Session (
                        semester VARCHAR(10) NOT NULL,
                        course_id VARCHAR(45) NOT NULL,
                        session_number INT NOT NULL,
                        day_time VARCHAR(30) NOT NULL,
                        instructor VARCHAR(100) NOT NULL,
                        crn INT NOT NULL,
                        PRIMARY KEY (semester, course_id, session_number),
                        INDEX fk_Session_Course1_idx (semester ASC, course_id ASC) VISIBLE,
                        CONSTRAINT fk_Session_Course1
                            FOREIGN KEY (semester , course_id)
                            REFERENCES Course (semester , course_id)
                            ON DELETE NO ACTION
                            ON UPDATE NO ACTION)
                        ENGINE = InnoDB;""")
            conn.commit()
            insert_course_DB(conn)

            return True
        except Exception as e:
            print("Failed initializing db")
            raise ValueError("Failed initializing db with " + str(e))


def insert_course_DB(conn, force=False):
    print("Inserting course data in DB")
    try:
        with conn.cursor() as cur:
            cur.execute("SET FOREIGN_KEY_CHECKS=0;")

            # Check if there is a club data update within a week
            print("Checking update condition")
            # if force update is true, update forcely without checking update condition.
            print("Force update course finder DB")
            if not force:
                cur.execute(
                    """SELECT * 
                    FROM Semester 
                    WHERE CURDATE() < DATE_ADD(created, INTERVAL 2 WEEK);""")

                # If there is club data update in a week, return. No need for update
                result = list(cur)
                if len(result) != 0:
                    print("Update is not needed")
                    return False

        # Start updating club information data
        print("Start updating course information")
        query_semester = """
        INSERT IGNORE INTO Semestzer (
            semester, year, season, created)
        VALUES (%s, %s, %s, CURDATE())"""

        query_department = """
        INSERT IGNORE INTO Department (
            department_name)
        VALUES (%s)"""

        query_course = """
        INSERT IGNORE INTO Course (
            semester, course_id, department_name, course_number, title, credits, gened, special_info)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        query_session = """
        INSERT IGNORE INTO Session (
            semester, course_id, session_number, day_time, instructor, crn)
        VALUES (%s, %s, %s, %s, %s, %s)"""

        # Get data from TUJ server with web scrap
        print("Loading full semesters information from TUJ website")
        full_semesters_courses_dict = get_full_semesters_courses()
        print(full_semesters_courses_dict)
        with conn.cursor() as cur:
            for semester in full_semesters_courses_dict:
                # Inserting semesters
                print("Inserting " + semester + " into Semester table")
                cur.execute(query_semester, (semester,
                                             semester[-4:], semester[:-4]))

                # Insert departments
                for department in full_semesters_courses_dict[semester]:
                    # Inserting departments
                    print("Inserting " + department + " into Department table")
                    cur.execute(query_department, (department))

                    # Insert courses
                    for course in full_semesters_courses_dict[semester][department]:
                        course_dict = full_semesters_courses_dict[semester][department][course]
                        # Inserting courses
                        print("Inserting " + course +
                              " (" + semester + ") into Course table")
                        cur.execute(query_course, (
                        semester, course, department, course[-4:], course_dict["Title"], course_dict["Credits"],
                        course_dict["GenEd"] if course_dict["GenEd"] != "" else None,
                        course_dict["Special_Info"] if course_dict["Special_Info"] != "" else None))

                        # Insert sessions
                        for session in full_semesters_courses_dict[semester][department][course]["Sessions"]:
                            # Inserting courses
                            print("Inserting " + session["Session_Number"] + "-" +
                                  course + "(" + semester + ") into Session table")
                            cur.execute(
                                query_session, (
                                semester, course, session["Session_Number"], session["Day&Time"], session["Instructor"],
                                session["CRN"]))

            conn.commit()
            print("Inserted full courses data in DB")
            return True
    # Catch Error and handle it
    except Exception as e:
        print("Inserting courses information failed with error message : " + str(e))
        raise ValueError(
            "Inserting courses information failed with error message : " + str(e))


def get_full_semesters_courses(record=False):
    from bs4 import BeautifulSoup

    import requests
    root_url = "https://ug-schedules.tuj.ac.jp/"

    html = requests.get(root_url).content
    soup = BeautifulSoup(html, "html.parser")
    semester_links = soup.find_all("a")

    semesters = [link.text for link in semester_links]
    semesters_courses_dict = {}
    for semester in semesters:
        semesters_courses_dict[semester] = load_courses(semester)

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    if record:
        with open(f"assets/CourseSchedule/full_semesters-{date}.json", 'w', encoding="utf-8_sig") as f:
            json.dump(semesters_courses_dict, f, indent=2, ensure_ascii=False)

    return semesters_courses_dict


# Webscraping program for a semester.


def load_courses(semester=None, record=False):
    from bs4 import BeautifulSoup
    import requests
    root_url = root_url = "https://ug-schedules.tuj.ac.jp/ug/academics/semester-info/schedule/"

    html = requests.get(root_url).content
    soup = BeautifulSoup(html, "html.parser")
    semester_links = soup.find_all("a")
    for link in semester_links:
        # print("Accessing URL : " + link.get('href'))

        url = root_url + link.get('href')

    url = root_url + semester

    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")

    table = soup.select_one("body table")
    tbody = table.find("tbody")
    courses = tbody.find_all("tr")
    headers = [header.text for header in table.find("tr").find_all("th")]
    data_dict = {}

    # Department
    for row in courses:
        data_dict[row.find("td").text] = {}

    for row in courses:
        # Course Detail
        attributes = row.find_all("td")
        detail = {}
        # Prepare course detail (0 is department and 1 is course number)

        department = attributes[0].text
        course_number = attributes[1].text[:-6]
        session_number = attributes[1].text[-4:-1]
        for i in range(4, len(headers) - 4):
            detail[headers[i]] = attributes[i].text.replace("\n", "")

        detail["Session_Number"] = session_number

        # Create course number key if it does not exist in dict
        if course_number not in data_dict[department]:
            data_dict[department][course_number] = {}
            data_dict[department][course_number]["Title"] = attributes[2].text
            data_dict[department][course_number]["Credits"] = attributes[3].text
            data_dict[department][course_number]["GenEd"] = attributes[7].text
            data_dict[department][course_number]["Prior"] = attributes[8].text
            data_dict[department][course_number]["Special_Info"] = attributes[9].text
            data_dict[department][course_number]["Sessions"] = []

        # Set course detail to course
        data_dict[department][course_number]["Sessions"].append(detail)

    # pop empty row
    if "" in data_dict:
        data_dict.pop('')
    if " " in data_dict:
        data_dict.pop(' ')

    # pprint.pprint(data_dict)
    if record:
        with open("assets/CourseSchedule/" + url.split("/")[-1] + ".json", 'w', encoding="utf-8_sig") as f:
            json.dump(data_dict, f, indent=2,
                      ensure_ascii=False, sort_keys=True)
    return data_dict


def get_semeter_data(semester):
    import datetime
    nSeasons = len(seasons_list)

    # if semester is specified then use that semester value.
    # Otherwise get current year and month from os
    if semester is None:
        current_datetime = datetime.datetime.now()
        month = current_datetime.month
        year = current_datetime.year
    else:
        year = int(semester[-4:])
        if semester[:-4] == "spring":
            month = 1
        elif semester[:-4] == "summer":
            month = 5
        elif semester[:-4] == "fall":
            month = 8

    if 1 <= month <= 4:
        current_season_num = 0
    elif 5 <= month <= 7:
        current_season_num = 1
    elif 8 <= month <= 12:
        current_season_num = 2

    next_season_num = (current_season_num + 1) % nSeasons
    year_next = year + (current_season_num + 1) // nSeasons

    season_dict = {"CurrentSemester": {"Year": year,
                                       "Season": seasons_list[current_season_num],
                                       "String": seasons_list[current_season_num] + str(year)},
                   "NextSemester": {"Year": year_next,
                                    "Season": seasons_list[next_season_num],
                                    "String": seasons_list[next_season_num] + str(year_next)}}
    print(season_dict)

    return season_dict


# You can specify semester and generate menu.
def course_finder_menu(conn, semester=None, next_semester=False, notification=True, record=False):
    print("Preparing course finder menu message")
    # Get semester information
    semester_dict = get_semeter_data(semester=semester)
    semester = semester_dict["CurrentSemester" if not next_semester else "NextSemester"]["String"]

    print("Loading department data from DB")
    with conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        cur.execute(
            """SELECT DISTINCT department_name 
            FROM Course 
            WHERE semester = '""" + semester_dict["CurrentSemester" if not next_semester else "NextSemester"][
                "String"] + "'"
            + " Order By department_name")

        departments = [x[0] for x in list(cur)]

    with conn.cursor() as cur:
        cur.execute(
            """SELECT DISTINCT semester 
            FROM Course""")

        semesters = [x[0] for x in list(cur)]
        print(semesters)
        print(semester_dict["NextSemester"]["String"])
        print(semester_dict["NextSemester"]["String"] in semesters)

    carousel = {
        "type": "carousel",
        "contents": []
    }

    buttons_row = []
    buttons_horizontal = {
        "type": "box",
        "layout": "horizontal",
        "contents": [],
        "spacing": "md"
    }

    print(1)
    print(departments)
    start_letter = departments[0][0].upper()
    print(2)

    header = [
        {
            "color": "#1DB446",
            "size": "sm",
            "text": "Course Finder",
            "type": "text",
            "weight": "bold",
            "align": "center"
        },
        {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "color": "#FFFFFF" if not next_semester else "#1DB446",
                    "size": "sm",
                    "text": str(semester_dict["CurrentSemester"]["Year"]) + " " + semester_dict["CurrentSemester"][
                        "Season"].capitalize(),
                    "type": "text",
                    "weight": "bold",
                    "align": "center"
                }
            ],
            "backgroundColor": "#1DB446" if not next_semester else "#efefef",
            "height": "20px",
            "cornerRadius": "10px",
            "borderWidth": "1px",
            "borderColor": "#dcdcdc",
            "action": {
                "type": "postback",
                "label": "action",
                "data": "CourseFinder--" + semester_dict["CurrentSemester"]["String"],
                "displayText": semester_dict["CurrentSemester"]["String"] + " Course Finder"
            }
        }]
    print(3)

    # Check if the next semester information is available in TUJ website,
    # If Yes, then add next semester, if not just keep current semester.
    if semester_dict["NextSemester"]["String"] in semesters:
        header.append({
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "color": "#1DB446" if not next_semester else "#FFFFFF",
                    "size": "sm",
                    "text": str(semester_dict["NextSemester"]["Year"]) + " " + semester_dict["NextSemester"][
                        "Season"].capitalize(),
                    "type": "text",
                    "weight": "bold",
                    "align": "center"
                }
            ],
            "backgroundColor": "#efefef" if not next_semester else "#1DB446",
            "height": "20px",
            "cornerRadius": "10px",
            "borderColor": "#dcdcdc",
            "borderWidth": "1px",
            "action": {
                "type": "postback",
                "label": "action",
                "data": "CourseFinder--" + semester_dict["CurrentSemester"]["String"] + "--next",
                "displayText": semester_dict["NextSemester"]["String"] + " Course Finder"
            }
        })
    print(4)

    # Disable current semester button.
    header[1 + int(next_semester)].pop("action")

    for i in range(len(departments)):
        buttons_horizontal["contents"].append(
            CustomButton(departments[i], shadow=True, shadow_distance=4,
                         command_prefix="CourseFinder--" + semester + "--", notification=notification))
        if i % 2 == 1:
            buttons_row.append(buttons_horizontal)
            buttons_horizontal = {
                "type": "box",
                "layout": "horizontal",
                "contents": [],
                "spacing": "md"
            }

        if i % 10 == 0 and i != 0 or i == len(departments) - 1:
            button_box = {
                "type": "box",
                "layout": "vertical",
                "contents": buttons_row,
                "margin": "md",
                "spacing": "md"
            }
            buttons_row = []

            bubble = {
                "type": "bubble",
                "size": "giga",
                "direction": "ltr",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": header,
                            "justifyContent": "space-around",
                            "spacing": "lg"
                        },
                        {
                            "type": "text",
                            "weight": "bold",
                            "size": "3xl",
                            "margin": "md",
                            "text": start_letter + " - " + departments[i][0].upper(),
                            "offsetStart": "15px"
                        },
                        {
                            "type": "text",
                            "text": "Select department",
                            "size": "sm",
                            "color": "#aaaaaa",
                            "offsetStart": "8px"
                        },
                        {
                            "type": "separator",
                            "margin": "lg"
                        },

                        button_box,
                        {
                            "type": "separator",
                            "margin": "lg"
                        }
                    ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }

            # bubble["body"]["contents"][0]["contents"][1 + int(next_semester)].pop("action")

            carousel["contents"].append(bubble)
            if i < len(departments) - 1:
                start_letter = departments[i][0].upper()

    print(5)

    bubble_gened = {
        "type": "bubble",
        "size": "giga",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": header,
                    "justifyContent": "space-around",
                    "spacing": "lg"
                },
                {
                    "type": "text",
                    "weight": "bold",
                    "size": "3xl",
                    "margin": "md",
                    "text": "GenEd",
                    "offsetStart": "15px"
                },
                {
                    "type": "text",
                    "text": "Select GenEd category",
                    "size": "sm",
                    "color": "#aaaaaa",
                    "offsetStart": "8px"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },

                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [CustomButton(gened_list[i * 2 + j], shadow=True, letter_shift=1,
                                                      shadow_distance=4,
                                                      command_prefix="CourseFinder--" + semester + "--",
                                                      notification=notification)
                                         for j in range(2)],
                            "spacing": "md"
                        } for i in range(len(gened_list) // 2)
                    ],
                    "margin": "md",
                    "spacing": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                }
            ]
        },
        "styles": {
            "footer": {
                "separator": True
            }
        }
    }
    carousel["contents"].append(bubble_gened)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    if record:
        with open("assets/CourseSchedule/CourseFinderMenu_" + semester_dict["CurrentSemester"][
            "String"] + "-" + date + ".json", 'w', encoding="utf-8_sig") as f:
            json.dump(carousel, f, indent=2,
                      ensure_ascii=False, sort_keys=True)

    return carousel


def course_finder_courses(conn, semester, department=None, gened=None, notification=True, record=False):
    # Get semester information
    semester_dict = get_semeter_data(semester=semester)

    print("Loading department course data from DB")
    with conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        query = """SELECT DISTINCT course_id, title, gened 
            FROM Course 
            WHERE semester = '""" + semester_dict["CurrentSemester"]["String"] + "'"
        if department is not None:
            query += " AND department_name = '" + department + "'"
        if gened is not None:
            query += " AND gened = '" + gened + "'"
            department = gened.upper()

        query += " ORDER BY course_id, course_number"
        print(query)
        cur.execute(query)

        db_data = list(cur)

    carousel = {
        "type": "carousel",
        "contents": []
    }

    courses_dict_list = []

    for i in range(len(db_data)):
        course_id, title, gened = db_data[i]

        course = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "align": "center",
                    "color": "#555555",
                    "gravity": "center",
                    "maxLines": 2,
                    "text": title,
                    "weight": "bold",
                    "wrap": True,
                    "flex": 2
                },
                CustomButton(course_id, flex=1, adjust_color=100 - (int(course_id[-4]) - 3) * 15, shadow=True,
                             shadow_distance=4, command_prefix="CourseFinder--" + semester + "--" + department + "--",
                             notification=notification)
            ],
            "spacing": "md"
            # ,
            # "alignItems": "center"
        }

        # Add GenEd Icon to GenEd courses
        if gened != None:
            course["contents"].append(CustomButton(
                gened, text_size="sm", height=15, width=30, shadow=True, letter_shift=1, shadow_distance=4,
                rounded=True, absolute=True, notification=notification, disable=True))

        courses_dict_list.append(course)

        if (i + 1) % 5 == 0 and i != 0 or i == len(db_data) - 1:
            button_box = {
                "type": "box",
                "layout": "vertical",
                "contents": courses_dict_list,
                "margin": "md",
                "spacing": "md"
            }
            courses_dict_list = []
            bubble = {
                "type": "bubble",
                "size": "giga",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "color": "#1DB446",
                            "size": "sm",
                            "text": str(semester_dict["CurrentSemester"]["Year"]) + " " +
                                    semester_dict["CurrentSemester"]["Season"].capitalize()
                                    + " Course Finder",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "margin": "md",
                            "offsetStart": "15px",
                            "size": "xxl",
                            "text": department,
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "color": "#aaaaaa",
                            "text": "Select a course",
                            "offsetStart": "8px",
                            "size": "sm"
                        },
                        {
                            "margin": "lg",
                            "type": "separator"
                        },
                        button_box,
                        {
                            "margin": "lg",
                            "type": "separator"
                        }
                    ]
                }
            }
            carousel["contents"].append(bubble)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    if record:
        with open("assets/CourseSchedule/CourseFinderCourseList_" + department + "-" + date + ".json", 'w',
                  encoding="utf-8_sig") as f:
            json.dump(carousel, f, indent=2,
                      ensure_ascii=False, sort_keys=True)
    return carousel


def course_finder_course(conn, semester, course_id, record=False):
    # Get semester information
    semester_dict = get_semeter_data(semester=semester)

    print("Loading course data from DB")
    with conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        cur.execute(
            """SELECT title, credits, gened, special_info 
            FROM Course
            WHERE semester = '""" + semester + "'"
            + " AND " + "course_id = '" + course_id + "'")

        title, credits, gened, special_info = list(cur)[0]
        course_info = {"Title": title, "Credits": str(
            credits), "GenEd": gened, "Special Info": special_info}

        # Delete keys Gened and special info if they are empty
        if course_info["GenEd"] is None:
            course_info.pop("GenEd")
        if course_info["Special Info"] is None:
            course_info.pop("Special Info")

    print("Loading semester data from DB")
    with conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        cur.execute(
            """SELECT year, season
            FROM Semester
            WHERE semester = '""" + semester + "'")

        year, season = list(cur)[0]
        season_info = {"Year": str(year), "Season": season.capitalize()}

    print("Loading session data from DB")
    with conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        cur.execute(
            """SELECT session_number, day_time, instructor, crn
            FROM Session
            WHERE semester = '""" + semester + "'"
            + " AND course_id = '" + course_id + "'"
            + " ORDER BY session_number")

        sessions_list = list(cur)

    carousel = {
        "type": "carousel",
        "contents": []
    }

    course_data_box = {
        "type": "box",
        "layout": "vertical",
        "margin": "xxl",
        "spacing": "lg",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": str(semester_dict["CurrentSemester"]["Year"]) + " " + semester_dict["CurrentSemester"][
                            "Season"].capitalize(),
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": course_id,
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                ]
            }
        ]
    }

    for key in list(course_info.keys()):
        course_data_horizontal = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": key,
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": course_info[key],
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
            ]
        }
        course_data_box["contents"].append(course_data_horizontal)

    cover_bubble = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "contents": [
                {
                    "color": "#1DB446",
                    "size": "sm",
                    "text": str(semester_dict["CurrentSemester"]["Year"]) + " " + semester_dict["CurrentSemester"][
                        "Season"].capitalize(),
                    "type": "text",
                    "weight": "bold"
                },
                {
                    "margin": "md",
                    "offsetStart": "15px",
                    "size": "xxl",
                    "text": title,
                    "type": "text",
                    "weight": "bold",
                    "wrap": True
                },
                {
                    # "margin": "xxl",
                    "margin": "lg",
                    "type": "separator"
                },
                course_data_box,
                {
                    # "margin": "xxl",
                    "margin": "lg",
                    "type": "separator"
                }
            ],
            "layout": "vertical",
            "type": "box"
        }
    }

    carousel["contents"].append(cover_bubble)

    session_data_list = []
    for session_tuple in sessions_list:
        session_number, day_time, instructor, crn = session_tuple
        session = {"Day&Time": day_time,
                   "Instructor": instructor, "CRN": str(crn)}

        for key in list(session.keys()):
            session_data_horizontal = {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": key,
                        "size": "sm",
                        "color": "#555555",
                        "flex": 0
                    },
                    {
                        "type": "text",
                        "text": session[key],
                        "size": "sm",
                        "color": "#111111",
                        "align": "end"
                    }
                ]
            }

            session_data_list.append(session_data_horizontal)

        session_data_box = {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "lg",
            "contents": session_data_list
        }

        session_data_list = []

        session_bubble = {
            "type": "bubble",
            "size": "giga",
            "body": {
                "contents": [
                    {
                        "color": "#1DB446",
                        "size": "sm",
                        "text": str(semester_dict["CurrentSemester"]["Year"]) + " " + semester_dict["CurrentSemester"][
                            "Season"].capitalize()
                                + " Course Finder",
                        "type": "text",
                        "weight": "bold"
                    },
                    {
                        "margin": "md",
                        "offsetStart": "15px",
                        "size": "xxl",
                        "text": "Settion " + str(session_number),
                        "type": "text",
                        "weight": "bold",
                        "wrap": True
                    },
                    {
                        # "margin": "xxl",
                        "margin": "lg",
                        "type": "separator"
                    },
                    session_data_box,
                    {
                        # "margin": "xxl",
                        "margin": "lg",
                        "type": "separator"
                    }
                ],
                "layout": "vertical",
                "type": "box"
            }
        }
        carousel["contents"].append(session_bubble)

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    if record:
        with open("assets/CourseSchedule/CourseFinderCourse_" + course_id + "-" + date + ".json", 'w',
                  encoding="utf-8_sig") as f:
            json.dump(carousel, f, indent=2,
                      ensure_ascii=False, sort_keys=True)
    print(carousel)
    return carousel


def course_finder(line_bot_api, event, conn):
    if event.message.text.lower().strip() == "course finder":
        notification = True

        if isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
            notification = False
        contents = course_finder_menu(conn, notification=notification)

        payload = {
            "type": "flex",
            "altText": "Course Finder ",
            "contents": contents

        }
        line_bot_api.reply_message(event.reply_token,
                                   messages=FlexSendMessage.new_from_json_dict(payload),
                                   notification_disabled=not notification)
        # Check for update
        insert_course_DB(conn)

        return True
    return False


def course_finder_postback(line_bot_api, event, conn, debug_command=None):
    notification = True
    # debug_command is debug option and if it is true, take debug_command as postback data
    # This will output result in console and does not use line_bot_api
    if debug_command:
        data_list = debug_command.split("--")
    # if debug_command is not given then it is normal operation.
    else:
        if isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom):
            notification = False
        data = event.postback.data
        data_list = data.split("--")

    if data_list[0] == "CourseFinder":
        payload = None
        if len(data_list) == 2:

            contents = course_finder_menu(
                conn, semester=data_list[1], notification=notification)
            payload = {
                "type": "flex",
                "altText": "Course Finder",
                "contents": contents
            }

        elif len(data_list) == 3:
            # Menu with next optionm
            # Check if we apply next-semester option
            # Next postback : CourseFinder--next
            if data_list[2] == "next":
                contents = contents = course_finder_menu(
                    conn, semester=data_list[1], next_semester=True, notification=notification)
            elif data_list[2] in gened_list:
                contents = course_finder_courses(
                    conn, data_list[1], gened=data_list[2], notification=notification)
            else:
                contents = course_finder_courses(
                    conn, data_list[1], data_list[2], notification=notification)
            payload = {
                "type": "flex",
                "altText": "Course Finder",
                "contents": contents
            }

            add_quick_reply_custom(
                payload, [("postback", "Go back to top", "CourseFinder--" + data_list[1])])

        # data_list[2] is department,
        # data_list[3] is course
        elif len(data_list) == 4:
            contents = course_finder_course(conn, data_list[1], data_list[3])
            payload = {
                "type": "flex",
                "altText": "Course Finder",
                "contents": contents
            }
            # if data_list[1] != "gened":
            add_quick_reply_custom(payload, [("postback", "Go back to top", "CourseFinder--" + data_list[1]),
                                             ("postback", "Select other course",
                                              "CourseFinder--" + data_list[1] + "--" + data_list[2])])
            # else:
            #     add_quick_reply_custom(
            #         payload, [("postback", "Go back to top", "CourseFinder--" + data_list[2])])
        # if payload is not empty, send message.
        if payload is not None:
            # if test command is disabled, send message to Line
            if debug_command is None:
                line_bot_api.reply_message(event.reply_token,
                                           messages=FlexSendMessage.new_from_json_dict(payload),
                                           notification_disabled=not notification)
            # Save contests of message for debugging
            else:
                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d")
                with open("assets/CourseSchedule/CourseFinder_postback_" + debug_command + "-" + date + ".json", 'w',
                          encoding="utf-8_sig") as f:
                    json.dump(contents, f, indent=2,
                              ensure_ascii=False, sort_keys=True)
            return True

    return False


if __name__ == '__main__':
    get_full_semesters_courses(record=True)
