import pandas as pd

df = pd.read_csv("corpus_annotated.csv")

human = df[df["speaker"] == "human"]
ai = df[df["speaker"] == "ai"]

report = f"""
==================================================
   HUMAN vs AI CORPUS ANALYSIS REPORT
==================================================

DATASET SUMMARY
---------------
Total turns        : {len(df)}
Human turns        : {len(human)}
AI turns           : {len(ai)}

WORD COUNT
----------
Human avg          : {human['word_count'].mean():.2f}
AI avg             : {ai['word_count'].mean():.2f}

SENTENCE COUNT
--------------
Human avg          : {human['sentence_count'].mean():.2f}
AI avg             : {ai['sentence_count'].mean():.2f}

AVG WORD LENGTH
---------------
Human avg          : {human['avg_word_length'].mean():.2f}
AI avg             : {ai['avg_word_length'].mean():.2f}

==================================================
"""

print(report)
with open("report.txt", "w") as f:
    f.write(report)
print("Report saved as report.txt")