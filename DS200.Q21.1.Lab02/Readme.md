# DS200.Q21.1 - Lab 02: Apache Pig Hotel Review Analysis

**Course**: DS200.Q21.1 - Big Data Analysis | **Student**: Nguyen Ba Long (23520880)

---

## Overview

Process hotel review data using **Apache Pig** scripting language. Analyze word frequencies, sentiment patterns, and category distributions from hotel-review.csv dataset.

---

## Technologies

- **Apache Pig 0.17.0** - Data processing scripting
- **Apache Hadoop 3.3.6+** - Distributed file system
- **Java 11+** - Runtime

---

## Dataset

**File**: `Data/hotel-review.csv` (Semicolon-delimited)

| Column | Type | Description |
|--------|------|-------------|
| id | int | Review ID |
| review | chararray | Review text |
| category | chararray | Category (room, service, etc.) |
| aspect | chararray | Aspect reviewed |
| sentiment | chararray | positive/negative |

**Stopwords**: `Data/stopwords.txt` - Common words filter

---

## Project Structure

```
DS200.Q21.1.Lab02/
├── Data/                    # Input files
├── Source_Pig/              # 5 Pig scripts
│   ├── bai1.pig            # Task 1: Text cleaning & tokenization
│   ├── bai2.pig            # Task 2: Word frequency & counting
│   ├── bai3.pig            # Task 3: Sentiment analysis
│   ├── bai4.pig            # Task 4: Advanced analysis
│   └── bai5.pig            # Task 5: Data aggregation
├── Notebook/                # Analysis notebooks
├── Output/                  # Results
└── Result/                  # Final summaries
```

---

## Tasks Summary

| Task | Description |
|------|-------------|
| **1** | Lowercase → tokenize → remove stopwords → clean tokens |
| **2** | Word frequency (>500), category count, aspect count |
| **3** | Sentiment by aspect (positive/negative split) |
| **4** | Advanced filtering & grouping |
| **5** | Multi-level aggregation |

---

## Running Scripts

### Setup Environment
```bash
export PIG_HOME=/path/to/pig-0.17.0
export HADOOP_HOME=/path/to/hadoop-3.3.6
export PATH=$PIG_HOME/bin:$HADOOP_HOME/bin:$PATH
```

### Run Individual Task (Local Mode)
```bash
cd DS200.Q21.1.Lab02
pig -x local Source_Pig/bai1.pig
```

### Run All Tasks
```bash
for i in 1 2 3 4 5; do
  echo "Running Task $i..."
  pig -x local Source_Pig/bai$i.pig
done
```

---

## Key Pig Operations

```pig
-- Load CSV data
raw = LOAD 'file.csv' USING PigStorage(';') 
      AS (id:int, text:chararray);

-- Transform data
cleaned = FOREACH raw GENERATE id, LOWER(text);

-- Filter rows
filtered = FILTER cleaned BY condition;

-- Group & count
grouped = GROUP filtered BY category;
counted = FOREACH grouped GENERATE group, COUNT(filtered);

-- Sort & save
sorted = ORDER counted BY $1 DESC;
STORE sorted INTO 'output' USING PigStorage('\t');
```

---

## Output Format

Tab-delimited results:
```
word1	456
word2	423
```

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Pig not found | `export PATH=$PIG_HOME/bin:$PATH` |
| File not found | Use absolute paths or cd to lab directory |
| Delimiter error | Check `PigStorage(';')` matches CSV |
| Memory error | `export PIG_OPTS="-Xmx4g"` |

---

## References

- [Apache Pig Docs](https://pig.apache.org/docs/r0.17.0/)
- [Pig Latin Guide](https://pig.apache.org/docs/r0.17.0/basic.html)
- [Hadoop](https://hadoop.apache.org/docs/stable/)

---

**Last Updated**: April 28, 2026 | **Status**:  Complete
