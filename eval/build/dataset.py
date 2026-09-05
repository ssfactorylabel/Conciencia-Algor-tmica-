# eval/build_dataset.py v3.0
import json, os
cases = []
for i in range(1,26):
    cases.append({"id": f"honest_{i:02d}", "input": f"Mi nombre es User{i} y vivo en Caracas", "expected_action": "REMEMBER", "score": 9 if i%2 else 8, "type": "identidad", "reason": "dato importante"})
for i, txt in enumerate(["hola","ok","jaja","si","no","lol","xd","bueno","vale","mmm","ah","eh","hmm","wtf","jajaja","okay","si va","dale","aja","uff","jeje","xD","...","holi","bye"],1):
    cases.append({"id": f"trivial_{i:02d}", "input": txt, "expected_action": "IGNORE", "score": 3, "type": "trivial", "reason": "filler"})
open("ConcienciaBench.json","w",encoding="utf-8").write(json.dumps(cases,indent=2,ensure_ascii=False))
open("eval/ConcienciaBench.json","w",encoding="utf-8").write(json.dumps(cases,indent=2,ensure_ascii=False))
print("50 cases generated")
