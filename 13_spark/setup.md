# Spark Basics Exercise

## Setup von Spark
Mein Setup besteht aus Visual Studio Code als Editor mit der offiziellen Spark/Hive Extension von Microsoft, um von VS Code direkt eine Verbindung zu einem Spark-Cluster aufnehmen zu können. Unter der Haube verwendet die Extension Python Notebooks und Sparkmagic.

[Sparkmagic](https://github.com/jupyter-incubator/sparkmagic) kommuniziert über die Python Notebooks mit dem Spark REST Server **Livy**, der wiederum mit dem Spark-Cluster kommunizieren.

Damit die Extension richtig funktioniert, musste zuvor Spark und Hadoop installiert werden bzw. in C: unter Windows abgelegt und in den Umgebungsvariablen registriert werden.

Es muss also

- C:\hadoop\bin existieren,
- C:\Spark\spark-3.0.0-bin-hadoop2.7\bin existieren und
- Umgebungsvariablen registriert sein.

Die Installation der drei konnte relativ einfach mit Hilfe eines [Online-Tutorials](https://phoenixnap.com/kb/install-spark-on-windows-10) vollzogen werden. Prinzipiell sind die Schritte aber nicht allzu schwer gewesen, auch einige Schritte aus der Spark 1 & 2 Powerpoint waren nicht notwendig.

## Schreiben von Python-Skripten mit PySpark
Nachdem das Setup abgeschlossen wurde, kann in VS Code ein Python-Skript angelegt werden. In dem Ordnerverzeichnis /.vscode kann eine settings.json Datei angelegt werden, wo dann Python-Skripte als Spark-Skripte deklariert werden können.

```json
{
    "hdinsightJobSubmission.ClusterConf": [
        {
            "name": "Spark",
            "filePath": "c:\\Users\\thomai\\Google Drive\\Ostfalia\\SS 20\\DataScience\\13_spark\\13_spark.py"
        }
    ]
}
```

Die Extension wird dann beim Öffnen dieser ausgewählten Python-Skripte im Hintergrund das komplette Spark-Setup übernehmen. Beim Ausführen des Skriptes wird eine Art Pyton-Notebook Shell geöffnet. Diese kann auch als .ipynb-Datei exportiert werden.

![Shell and Coding](./result.png)

Das Skript zur Shell sieht z.B. wie folgt aus und ist in der settings.json als *13_spark.py* hinterlegt.

```py
import numpy as np
from pyspark import SparkConf, SparkContext

# Environment
n = 24

# Context
conf = SparkConf().setAppName("word count").setMaster("local[1]")
sc = SparkContext(conf=conf)

# Import Data
text = sc.textFile("shakespear.txt")

# Setup Filter Function
disabledCharacters = [".", ",", ";", "!", "?", "(", ")", "[", "]", "'", "-"]

def mapper(text):
    line = np.array(text.split(" "))
    line = line[np.logical_and(line != "", line != " ")]
    line = np.char.lower(line)

    for char in disabledCharacters:
        line = np.char.strip(line, chars=char)

    if len(line) > 0:
        return line.tolist()
    else:
        return []

# Processing Spark
lines = text.map(lambda textLine: mapper(textLine)) \
            .filter(lambda line: len(line) > 0)
result = lines.countByKey()

# Sorting
sorted = sorted(result.items(), key=lambda x: x[1], reverse=True)

for i in sorted[:n]:
	print(i[0], "  ", i[1])

```

## Ausführen von Skripten
Das Resultat der Ausführung eines Skript-Durchlaufes ist oben zu sehen.

Im Browser kann man unter http://localhost:4040 auch die Oberfläche von Spark erreichen.

![Spark](./spark.png)

Dort werden die Durchläufe samt entsprechenden Zeiten, zur Verfügung stehenden Workern etc. visualisiert.

## Lösung der Einsendeaufgabe
In der nachfolgenden Grafik sind die am meisten verwendeten Wörter in der Textdatei aufgelistet. Dabei wurden vorher einige Filter angewendet wie z.B. Sonderzeichen entfernen und alle Lowercase machen. Pluralisierte Wörter auf das entsprechende Singular zurückzuführen habe ich mir mal erspart. :D

![Lösung der ESA 13](./solution.png)