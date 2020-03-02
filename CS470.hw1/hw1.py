import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('/Users/admin/Desktop/EMORY/Academics/Spring_2020/CS470/CS470-1.hw1/grades.csv')

#
# Cleaning the data
#

# df.fillna(0, inplace=True)
for i in range(len(df.columns)):
    col = df.columns[i - 1]
    if 3 < i - 1 < 10 or 10 < i - 1 < 23 or 25 < i - 1 < 28:
        df[col].fillna(np.sum(df[col]) / (np.count_nonzero(~np.isnan(df[col].tolist()))), inplace=True)
    else:
        df[col].fillna(0, inplace=True)

#
# Combining attributes Semester and Section
#
semesterAndSection = []
for i in range(0, df.shape[0]):
    semester = df['Semester'].get(i)
    section = df['Section'].get(i)
    semesterAndSection.append((int(semester[1:]) + 2000) * 100 + (semester[0] == 'F') * 10 + section)

df.insert(0, 'SemesterAndSection', semesterAndSection)

#
# Data Initialization
#

semester = ['S', 'F']
homeworkMean, homeworkSD = [], []
homeworkMeanSem = {'F18': [], 'S18': [], 'F17': [], 'S17': [], 'F16': []}
homeworkSDSem = {'F18': [], 'S18': [], 'F17': [], 'S17': [], 'F16': []}
homework5Number = []

quizMean = []
quizSD = []
quizMeanSem = {'F18': [], 'S18': [], 'F17': [], 'S17': [], 'F16': []}
quizSDSem = {'F18': [], 'S18': [], 'F17': [], 'S17': [], 'F16': []}
quiz5Number = []

peMean = np.average(df['Peer Evaluations'])
peSD = np.std(df['Peer Evaluations'])
peMeanSem = {'F18': 0, 'S18': 0, 'F17': 0, 'S17': 0, 'F16': 0}
peSDSem = {'F18': 0, 'S18': 0, 'F17': 0, 'S17': 0, 'F16': 0}
pe5Number = []

finalMean = np.average(df['Final Exam'])
finalSD = np.std(df['Final Exam'])
finalMeanSem = {'F18': 0, 'S18': 0, 'F17': 0, 'S17': 0, 'F16': 0}
finalSDSem = {'F18': 0, 'S18': 0, 'F17': 0, 'S17': 0, 'F16': 0}
final5Number = []

totalMean = np.average(df['Total Score'])
totalSD = np.std(df['Total Score'])
totalMeanSem = {'F18': 0, 'S18': 0, 'F17': 0, 'S17': 0, 'F16': 0}
totalSDSem = {'F18': 0, 'S18': 0, 'F17': 0, 'S17': 0, 'F16': 0}
total5Number = []

#
# Calculating means and standard deviations
#
for i in range(1, 6):
    # updating homeworkMean and homeworkSD
    homeworkMean.append(np.average(df['Homework %s' % i]))
    homeworkSD.append(np.std(df['Homework %s' % i]))

for i in range(1, 13):
    # updating quizMean and quizSD
    quizMean.append(np.average(df['Quiz 0%s' % i]) if i < 10 else np.average(df['Quiz %s' % i]))
    quizSD.append(np.std(df['Quiz 0%s' % i]) if i < 10 else np.std(df['Quiz %s' % i]))

for s in semester:
    for y in range(16, 19):
        sem = "%s%s" % (s, y)
        # updating semester homeworkMean and homeworkSD
        for i in range(1, 6):
            if not (s == 'S' and y == 16):
                homeworkMeanSem[sem].append(
                    np.average(df.loc[df['Semester'] == s + str(y), 'Homework %s' % i]))
                homeworkSDSem[sem].append(np.std(df.loc[df['Semester'] == s + str(y), 'Homework %s' % i]))

        for i in range(1, 13):
            # updating semester quizMean and quizSD
            if not (s == 'S' and y == 16):
                if i < 10:
                    quizMeanSem[sem].append(np.average(df.loc[df['Semester'] == s + str(y), 'Quiz 0%s' % i]))
                    quizSDSem[sem].append(np.std(df.loc[df['Semester'] == s + str(y), 'Quiz 0%s' % i]))
                else:
                    quizMeanSem[sem].append(np.average(df.loc[df['Semester'] == s + str(y), 'Quiz %s' % i]))
                    quizSDSem[sem].append(np.std(df.loc[df['Semester'] == s + str(y), 'Quiz %s' % i]))

        # calculating PeerEv, Final and Total mean and SD
        peMeanSem[sem] = np.average(df.loc[df['Semester'] == s + str(y), 'Peer Evaluations'])
        peSDSem[sem] = np.std(df.loc[df['Semester'] == s + str(y), 'Peer Evaluations'])
        finalMeanSem[sem] = np.average(df.loc[df['Semester'] == s + str(y), 'Final Exam'])
        finalSDSem[sem] = np.std(df.loc[df['Semester'] == s + str(y), 'Final Exam'])
        totalMeanSem[sem] = np.average(df.loc[df['Semester'] == s + str(y), 'Total Score'])
        totalSDSem[sem] = np.std(df.loc[df['Semester'] == s + str(y), 'Total Score'])

for i in range(1, 6):
    homework5Number.append([np.min(df['Homework %s' % i]), np.quantile(df['Homework %s' % i], 0.25),
                            np.quantile(df['Homework %s' % i], 0.5), np.quantile(df['Homework %s' % i], 0.75),
                            np.max(df['Homework %s' % i])])

for i in range(1, 13):
    quiz5Number.append([np.min(df['Quiz 0%s' % i] if i < 10 else df['Quiz %s' % i]),
                        np.quantile(df['Quiz 0%s' % i] if i < 10 else df['Quiz %s' % i], 0.25),
                        np.quantile(df['Quiz 0%s' % i] if i < 10 else df['Quiz %s' % i], 0.5),
                        np.quantile(df['Quiz 0%s' % i] if i < 10 else df['Quiz %s' % i], 0.75),
                        np.max(df['Quiz 0%s' % i] if i < 10 else df['Quiz %s' % i])])

pe5Number.append([np.min(df['Peer Evaluations']), np.quantile(df['Peer Evaluations'], 0.25),
                  np.quantile(df['Peer Evaluations'], 0.5), np.quantile(df['Peer Evaluations'], 0.75),
                  np.max(df['Peer Evaluations'])])

final5Number.append([np.min(df['Final Exam']), np.quantile(df['Final Exam'], 0.25),
                     np.quantile(df['Final Exam'], 0.5), np.quantile(df['Final Exam'], 0.75),
                     np.max(df['Final Exam'])])

total5Number.append([np.min(df['Total Score']), np.quantile(df['Total Score'], 0.25),
                     np.quantile(df['Total Score'], 0.5), np.quantile(df['Total Score'], 0.75),
                     np.max(df['Total Score'])])

print('homeworkMean:\t ', homeworkMean)
print('homeworkSD:\t', homeworkSD)
print('homeworkMeanSem:\t', homeworkMeanSem)
print('homeworkSDSem:\t', homeworkSDSem)

print('quizMean:\t', quizMean)
print('quizSD:\t', quizSD)
print('quizMeanSem:\t', quizMeanSem)
print('quizSDSem:\t', quizSDSem)

#
# Calculating scaled scores
#

homeworkScale1, homeworkScale2, homeworkScale3 = [], [], []
homeworkScale = [homeworkScale1, homeworkScale2, homeworkScale3]
quizScale1, quizScale2, quizScale3 = [], [], []
quizScale = [quizScale1, quizScale2, quizScale3]

for i in range(1, 6):
    homeworkScale1.append((df['Homework %s' % i] * 2.5).tolist())
    homeworkScale2.append([x / homeworkSD[i - 1] for x in (df['Homework %s' % i] - homeworkMean[i - 1])])
    homeworkScale3.append([((score - homeworkMeanSem[sem][i - 1]) / homeworkSDSem[sem][i - 1]) for (score, sem) in
                           zip(df['Homework %s' % i].tolist(), df['Semester'])])

for i in range(1, 13):
    if i < 10:
        quizScale1.append((df['Quiz 0%s' % i] * 2).tolist())
        quizScale2.append([x / quizSD[i - 1] for x in (df['Quiz 0%s' % i] - quizMean[i - 1])])
        quizScale3.append(
            [((score - quizMeanSem[sem][i - 1]) / quizSDSem[sem][i - 1]) for (score, sem) in
             zip(df['Quiz 0%s' % i].tolist(), df['Semester'])])
    else:
        quizScale1.append((df['Quiz %s' % i] * 2).tolist())
        quizScale2.append([x / quizSD[i - 1] for x in (df['Quiz %s' % i] - quizMean[i - 1])])
        quizScale3.append([((score - quizMeanSem[sem][i - 1]) / quizSDSem[sem][i - 1]) for (score, sem) in
                           zip(df['Quiz %s' % i].tolist(), df['Semester'])])

peScale1 = [x / 1.5 for x in df['Peer Evaluations']]
peScale2 = [(x - peMean) / peSD for x in df['Peer Evaluations']]
peScale3 = [(score - peMeanSem[sem]) / peSDSem[sem] for score, sem in
            zip(df['Peer Evaluations'].tolist(), df['Semester'])]
peScale = [peScale1, peScale2, peScale3]

finalScale1 = [x / 1.5 for x in df['Final Exam']]
finalScale2 = [(x - finalMean) / finalSD for x in df['Final Exam']]
finalScale3 = [(score - finalMeanSem[sem]) / finalSDSem[sem] for score, sem in
               zip(df['Final Exam'].tolist(), df['Semester'])]
finalScale = [finalScale1, finalScale2, finalScale3]

totalScale1 = [x / 10 for x in df['Total Score']]
totalScale2 = [(x - totalMean) / totalSD for x in df['Total Score']]
totalScale3 = [(score - totalMeanSem[sem]) / totalSDSem[sem] for score, sem in
               zip(df['Total Score'].tolist(), df['Semester'])]
totalScale = [totalScale1, totalScale2, totalScale3]

print("homeworkScale1:\t", homeworkScale1)
print("homeworkScale2:\t", homeworkScale2)
print("homeworkScale3:\t", homeworkScale3)
print("quizScale1:\t", quizScale1)
print("quizScale2:\t", quizScale2)
print("quizScale3:\t", quizScale3)
print("peScale1:\t", peScale1)
print("peScale2:\t", peScale2)
print("peScale3:\t", peScale3)
print("finalScale1:\t", finalScale1)
print("finalScale2:\t", finalScale2)
print("finalScale3:\t", finalScale3)

#
# Adding attributes to dataframe
#
for i in range(3):
    # Adding homework scaling
    for j in range(1, 6):
        df.insert(df.columns.get_loc('Homework %s' % j) + i + 1, 'Homework %s Scaling %s' % (j, i + 1),
                  homeworkScale[i][j - 1])
    # Adding quiz scaling
    for j in range(1, 13):
        if j < 10:
            df.insert(df.columns.get_loc('Quiz 0%s' % j) + i + 1, 'Quiz 0%s Scaling %s' % (j, i + 1),
                      quizScale[i][j - 1])
        else:
            df.insert(df.columns.get_loc('Quiz %s' % j) + i + 1, 'Quiz %s Scaling %s' % (j, i + 1), quizScale[i][j - 1])
    # Adding peer evaluation scaling
    df.insert(df.columns.get_loc('Peer Evaluations') + i + 1, 'Peer Evaluations Scaling %s' % (i + 1),
              peScale[i])
    # Adding final exam scaling
    df.insert(df.columns.get_loc('Final Exam') + i + 1, 'Final Exam Scaling %s' % (i + 1), finalScale[i])
    # Adding total score scaling
    df.insert(df.columns.get_loc('Total Score') + i + 1, 'Total Score Scaling %s' % (i + 1), totalScale[i])

#
# Saving new dataframe to csv
#
del df['Semester']
del df['Section']
df.to_csv('/Users/admin/Desktop/EMORY/Academics/Spring_2020/CS470/CS470-1.hw1/results.csv', index=False)

#
# Plotting Data
#


df.boxplot(column=['Homework %s' % i for i in range(1, 6)])
plt.savefig('hwbox.png')
df.boxplot(column=['Quiz 0%s' % i for i in range(1, 10)])
plt.savefig('quizbox.png')
df.boxplot(column='Final Exam')
plt.savefig('finalbox.png')

df.hist(column=['Peer Evaluations'])
plt.savefig('pehist.png')
df.hist(column=['Final Exam'])
plt.savefig('finalhist.png')
df.hist(column=['Total Score'])
plt.savefig('totalhist.png')

plt.scatter(df['Final Exam'], df['Total Score'])
plt.savefig('finalscat.png')

plt.scatter(df['Peer Evaluations'], df['Total Score'])
plt.savefig('pescat.png')

plt.scatter(df['Homework 1'], df['Quiz 01'])
plt.savefig('hw1quiz1scat.png')

plt.scatter(quizMeanSem['F18'], quizMeanSem['F17'])
plt.title('Quiz 1 in Semester F18 to Semester F17 Scatter Plot')
plt.xlabel('F18')
plt.ylabel('F17')
plt.savefig('quizMeanSemScat.png')
