import matplotlib.pyplot as plt

accuracies = [("All Word Features\nReview Text", 28), ("Simple Tagging\n Review Text", 30), ("Bigram-Based Tagging\nReview Text", 50), ("All Word Features\nSummary Text", 78)]

methods = [a[0] for a in accuracies]
vals = [a[1] for a in accuracies]

ind = list(range(len(vals)))
ind = [(a * 10) + 5.0 for a in ind]

plt.bar(ind, vals, width=3.0, color='r')
plt.ylabel("Accuracy (%)")
plt.title("Accuracy of tested methods")
plt.xticks([a + 1.5 for a in ind], methods)
plt.yticks([a * 10 for a in range(11)])
plt.show()
