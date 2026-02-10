import requests
import json

url = "http://localhost:11434/api/chat"
model = "llama2:13b"   # change to llama2:7b if you want speed

PROMPT = """
You are a strict logical checker.

Your task is to decide whether the paragraph
LOGICALLY CONTRADICTS the backstory claim.

Rules:
- A contradiction exists ONLY if the paragraph makes the claim
  logically impossible.
- If the paragraph merely adds information, restricts scope,
  or is compatible, it is NOT a contradiction.
- Do NOT infer impossibility from imprisonment, location,
  beliefs, or vague language.
- Subjective beliefs or perceptions do NOT contradict facts.
- Vague terms (rarely, believed, felt) CANNOT cause contradiction.
- Constraints must be direct factual statements explicitly stated
  in the paragraph.
- Constraints must NOT mention contradiction or evaluation.
- If there is any doubt, output CONTRADICTION: 0.
- Use '-' for bullet points only.
- Do NOT include explanations.

Backstory Claim:
{BACKSTORY}

Paragraph:
{PARA}

Output EXACTLY in this format:

CONSTRAINTS:
- <fact-style constraint OR None>

CONTRADICTION: <0 or 1>
STRENGTH: <STRONG or NONE>
""".strip()


def call_llama(prompt):
    payload = {
        "model": model,
        "stream": False,
        "temperature": 0,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    r = requests.post(url, json=payload)
    return r.json()["message"]["content"]


def parse_output(text):
    contradiction = 0
    strength = "NONE"
    constraints = []

    if re.search(r"CONTRADICTION:\s*1", text):
        contradiction = 1

    m = re.search(r"STRENGTH:\s*(STRONG|NONE)", text)
    if m:
        strength = m.group(1)

    for line in text.splitlines():
        line = line.strip()
        if line.startswith(("-", "*")):
            c = line[1:].strip()
            if c.lower() != "none":
                if not any(w in c.lower() for w in [
                    "contradict", "conflict", "inconsistent",
                    "implies", "suggests", "belief"
                ]):
                    constraints.append(c)

    return contradiction, strength, constraints


def check_story(paras, backstory):
    constraints_ledger = []

    for para in paras:
        prompt = PROMPT.format(
            BACKSTORY=backstory,
            PARA=para
        )

        output = call_llama(prompt)
        contradiction, strength, constraints = parse_output(output)
        constraints_ledger.extend(constraints)

        print(output)

        if contradiction == 1 and strength == "STRONG":
            return 1, constraints_ledger

    return 0, constraints_ledger
