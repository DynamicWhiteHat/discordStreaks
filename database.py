import sqlite3
from datetime import datetime, timedelta


conn = sqlite3.connect('streaks.db')
c = conn.cursor()

today = datetime.today().date()


def add_user(username):
    with conn:
        c.execute("INSERT INTO streaks VALUES (?, ?, ?, ?)", (username, 1, 1, today,))


def set_streak(username, type):
    print(username)
    c.execute("SELECT * FROM streaks WHERE username=?", (username,))
    result = c.fetchone()  # Fetch the result properly
    print("Before update:", result)
    with conn:
        c.execute("SELECT currentstreak, best FROM streaks WHERE username=?", (username,))
        streak = c.fetchone()
        current_streak, best_streak = streak
        if type == 1:
            if current_streak >= best_streak: # New record streak
                c.execute("UPDATE streaks SET currentstreak = ?, best = ?, lastupdate = ? WHERE username = ?", (current_streak+1, current_streak+1, today, username)) #Update current streak for username
            else: # Only update current streak
                c.execute("UPDATE streaks SET currentstreak = ?, lastupdate = ? WHERE username = ?", (current_streak+1, today, username)) #Update current streak for username
            c.execute("SELECT * FROM streaks WHERE username=?", (username,))
            updated_result = c.fetchone()  # Fetch the updated result, from earlier line of code selects the username's results
            print("After update:", updated_result)
        elif type == 0:
            c.execute("UPDATE streaks SET currentstreak = ?, lastupdate = ? WHERE username = ?", (1, today, username)) #Update current streak for username
    
def checkstreak(username):
    c.execute ("SELECT lastupdate FROM streaks WHERE username=?", (username,))
    result = c.fetchone()

    if result:
        last_update = datetime.strptime(result[0], "%Y-%m-%d").date() 
        if (today-last_update).days == 1:
            set_streak(username, 1)
        elif (today-last_update).days > 1: 
            set_streak(username, 0)
        elif (today-last_update).days == 0:
            print("pdayt")
    else:
        add_user(username)
def get(username, type):
    if type == 1:  # Get current streak
        with conn:
            c.execute("SELECT currentstreak FROM streaks WHERE username=?", (username,))
            res = c.fetchone()
            return res[0] if res else None  # Return the value directly if found, else None

    elif type == 2:  # Top 3
        with conn:
            c.execute("SELECT currentstreak FROM streaks")
        best = [full[0] for full in c.fetchall()]  # List of current streaks
        c.execute("SELECT username FROM streaks")
        names = [full[0] for full in c.fetchall()]  # List of usernames

        # Lists to store top 3 results
        fName, sName, tName = [], [], []
        fHigh, sHigh, tHigh = [], [], []

        # Iterate to find top 3 streaks
        for x in range(3):
            if best:  # Check if `best` is not empty
                curr = max(best)  # Find the highest streak
                indices = [i for i, val in enumerate(best) if val == curr]  # Indices of max streak

                for idx in indices:
                    # Add values to the appropriate list based on iteration
                    if x == 0:
                        fName.append(names[idx])
                        fHigh.append(curr)
                    elif x == 1:
                        sName.append(names[idx])
                        sHigh.append(curr)
                    elif x == 2:
                        tName.append(names[idx])
                        tHigh.append(curr)

                # Remove processed values from `best` and `names`
                for idx in reversed(indices):
                    best.pop(idx)
                    names.pop(idx)
            else:
                break  # Exit loop if there are no more streaks

        # Return results
        return fName, fHigh, sName, sHigh, tName, tHigh

            
    elif type == 3: #username best streak
        with conn:
            c.execute("SELECT best FROM streaks WHERE username = ?", (username,))
            res = c.fetchone()
            return res[0] if res else None
        
    elif type == 4: #server best streak
        with conn:
            c.execute("SELECT best FROM streaks")
            best = [full[0] for full in c.fetchall()]
            fHigh = max(best)
            indices = [i for i, val in enumerate(best) if val == fHigh]
            c.execute("SELECT username FROM streaks")
            names = [full[0] for full in c.fetchall()]
            return fHigh, indices, names

    elif type == 5: #username info
        with conn:
            c.execute("SELECT * FROM streaks WHERE username = ?", (username,))
            rows = c.fetchall()
            if rows: 
                row = rows[0]
                print(row)
                current = row[1]
                best = row[2]
                timestamp = row[3]
                return current, best, timestamp
            else:
                return None

            

# c.execute("""CREATE TABLE streaks (
#           username text,
#           currentstreak integer,
#           best integer,
#           lastupdate date
#         )""")

conn.commit()
