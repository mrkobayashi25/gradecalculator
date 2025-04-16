import os
import matplotlib.pyplot as plt

students = {}
with open('data/students.txt') as f:
    for line in f:
        sid = line.strip()[:3]
        name = line.strip()[3:]
        students[sid] = name

assignments = {}
with open('data/assignments.txt') as f:
    lines = [line.strip() for line in f if line.strip()]
    for i in range(0, len(lines), 3):
        name = lines[i]
        aid = lines[i + 1]
        points = int(lines[i + 2])
        assignments[aid] = (name, points)

submissions = {}
submissions_dir = 'data/submissions'
for filename in os.listdir(submissions_dir):
    if filename.endswith('.txt'):
        with open(os.path.join(submissions_dir, filename)) as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    sid, aid, percent = parts
                    submissions.setdefault(aid, []).append((sid, float(percent)))

print("1. Student grade")
print("2. Assignment statistics")
print("3. Assignment graph\n")
choice = input("Enter your selection: ")

if choice == '1':
    name_input = input("What is the student's name: ")
    sid = None
    for id, name in students.items():
        if name == name_input:
            sid = id
            break
    if sid is None:
        print("Student not found")
    else:
        total_earned = 0
        for aid, records in submissions.items():
            for s_id, percent in records:
                if s_id == sid:
                    total_earned += (percent / 100) * assignments[aid][1]
        grade = round((total_earned / 1000) * 100)
        print(f"{grade}%")

elif choice == '2':
    assign_input = input("What is the assignment name: ")
    aid = None
    for id, (name, _) in assignments.items():
        if name == assign_input:
            aid = id
            break
    if aid is None or aid not in submissions:
        print("Assignment not found")
    else:
        scores = [percent for _, percent in submissions[aid]]
        print(f"Min: {int(min(scores))}%")
        print(f"Avg: {int(sum(scores)/len(scores))}%")
        print(f"Max: {int(max(scores))}%")

elif choice == '3':
    assign_input = input("What is the assignment name: ")
    aid = None
    for id, (name, _) in assignments.items():
        if name == assign_input:
            aid = id
            break
    if aid is None or aid not in submissions:
        print("Assignment not found")
    else:
        scores = [percent for _, percent in submissions[aid]]
        plt.hist(scores, bins=[0, 25, 50, 75, 100])
        plt.title(f"Scores for {assign_input}")
        plt.xlabel("Percentage")
        plt.ylabel("Number of Students")
        plt.savefig("histogram.png")
        plt.show()