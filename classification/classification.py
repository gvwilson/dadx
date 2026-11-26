# mccole:setup
import random

import polars as pl

SEED = 20261108
random.seed(SEED)
# mccole:/setup

# mccole:generate
KINDS = ["storm", "flood", "power-outage", "fire"]
KIND_BASE = {"storm": 0.02, "flood": 0.05, "power-outage": 0.00, "fire": 0.10}
SEVERITY_CHANCE = {1: 0.05, 2: 0.08, 3: 0.12, 4: 0.50, 5: 0.75}

def make_incidents(n):
    rows = []
    for i in range(1, n + 1):
        kind = random.choice(KINDS)
        severity = random.randint(1, 5)
        chance = min(1.0, SEVERITY_CHANCE[severity] + KIND_BASE[kind])
        escalated = 1 if random.random() < chance else 0
        rows.append(
            {"id": i, "kind": kind, "severity": severity, "escalated": escalated}
        )
    return rows

incidents = make_incidents(500)
df = pl.DataFrame(incidents)
print(df.head())
# mccole:/generate

# mccole:rate
rate = df["escalated"].mean()
print(f"escalation rate: {rate:.0%}")
# mccole:/rate

# mccole:split
n_train = int(len(df) * 0.8)
train = df.slice(0, n_train)
test = df.slice(n_train, len(df) - n_train)
print(f"train: {len(train)} rows, test: {len(test)} rows")
# mccole:/split

# mccole:predict
def predict(severity, threshold):
    return 1 if severity >= threshold else 0
# mccole:/predict

# mccole:confusion
def confusion(y_true, y_pred):
    tp = fp = tn = fn = 0
    for t, p in zip(y_true, y_pred):
        if t == 1 and p == 1:
            tp += 1
        elif t == 1 and p == 0:
            fn += 1
        elif t == 0 and p == 1:
            fp += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn}

def stats(cm):
    tp, fp, tn, fn = cm["tp"], cm["fp"], cm["tn"], cm["fn"]
    accuracy = (tp + tn) / (tp + fp + tn + fn)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0.0
    )
    return accuracy, precision, recall, f1
# mccole:/confusion

# mccole:fit_threshold
train_true = train["escalated"].to_list()
train_sev = train["severity"].to_list()

best_threshold, best_f1 = None, -1.0
for threshold in range(1, 6):
    preds = [predict(s, threshold) for s in train_sev]
    score = stats(confusion(train_true, preds))[3]
    if score > best_f1:
        best_threshold, best_f1 = threshold, score
    print(f"threshold {threshold}: F1 = {score:.2f}")

print(f"chosen threshold: severity >= {best_threshold}")
# mccole:/fit_threshold

# mccole:evaluate
test_true = test["escalated"].to_list()
test_sev = test["severity"].to_list()
test_pred = [predict(s, best_threshold) for s in test_sev]

cm = confusion(test_true, test_pred)
print("confusion matrix")
print("              predicted")
print("               no   yes")
print(f"actual no    {cm['tn']:>4}  {cm['fp']:>4}")
print(f"actual yes   {cm['fn']:>4}  {cm['tp']:>4}")
# mccole:/evaluate

# mccole:metrics
accuracy, precision, recall, f1 = stats(cm)
print(f"accuracy  = {accuracy:.2f}")
print(f"precision = {precision:.2f}")
print(f"recall    = {recall:.2f}")
print(f"F1        = {f1:.2f}")
# mccole:/metrics

# mccole:baseline
never_pred = [0] * len(test_true)
never_cm = confusion(test_true, never_pred)
never_acc, _, never_recall, _ = stats(never_cm)
print(f"always-no accuracy = {never_acc:.2f}")
print(f"always-no recall   = {never_recall:.2f}")
# mccole:/baseline
