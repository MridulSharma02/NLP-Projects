import pandas as pd
import matplotlib.pyplot as plt

print("Loading annotated corpus...")
df = pd.read_csv("corpus_annotated.csv")

human = df[df["speaker"] == "human"]
ai = df[df["speaker"] == "ai"]

print(f"Human turns: {len(human)}")
print(f"AI turns: {len(ai)}")
print(f"\nAvg word count - Human: {human['word_count'].mean():.2f}")
print(f"Avg word count - AI: {ai['word_count'].mean():.2f}")
print(f"\nAvg sentence count - Human: {human['sentence_count'].mean():.2f}")
print(f"Avg sentence count - AI: {ai['sentence_count'].mean():.2f}")
print(f"\nAvg word length - Human: {human['avg_word_length'].mean():.2f}")
print(f"Avg word length - AI: {ai['avg_word_length'].mean():.2f}")

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Human vs AI Sentence Structure Analysis", fontsize=14)

axes[0].bar(["Human", "AI"], [human["word_count"].mean(), ai["word_count"].mean()], color=["#4C72B0", "#DD8452"])
axes[0].set_title("Avg Word Count")
axes[0].set_ylabel("Words")

axes[1].bar(["Human", "AI"], [human["sentence_count"].mean(), ai["sentence_count"].mean()], color=["#4C72B0", "#DD8452"])
axes[1].set_title("Avg Sentence Count")
axes[1].set_ylabel("Sentences")

axes[2].bar(["Human", "AI"], [human["avg_word_length"].mean(), ai["avg_word_length"].mean()], color=["#4C72B0", "#DD8452"])
axes[2].set_title("Avg Word Length")
axes[2].set_ylabel("Characters")

plt.tight_layout()
plt.savefig("analysis_chart.png", dpi=150)
print("\nChart saved as analysis_chart.png")
plt.show()