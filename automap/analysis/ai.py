import json

from ollama import Client



# Converts scan report data into a prompt for the AI analyst.
def build_scan_prompt(report_data: dict) -> str:
    scan_json = json.dumps(report_data, indent=2)

    return f"""You are AutoMap, a defensive AI security analyst for authorized local network scans.

Your job:
Analyze the provided network scan data and explain the security meaning clearly.

Important rules:
- This is defensive analysis only.
- Do not provide exploitation steps.
- Do not suggest attacking, bypassing, brute forcing, or abusing services.
- Focus on risk explanation, prioritization, and safe remediation.
- If data is missing, say what is missing.
- Do not invent devices, ports, services, CVEs, versions, or vulnerabilities.
- Base your answer only on the scan data.
- If a port risk is unknown, explain that more fingerprinting is needed.
- Keep advice beginner-friendly but technically correct.

Input meaning:
- devices contains discovered network devices.
- open_ports contains TCP ports found open by AutoMap.
- service is AutoMap's best-known service guess.
- risk is a basic local risk label, not a confirmed vulnerability.
- summary contains scan totals.

Output format:
Return ONLY valid JSON.
Do not wrap it in markdown.
Do not add text before or after the JSON.

Required JSON shape:
{{
  "summary": "short overall explanation",
  "network_posture": "low | medium | high | unknown",
  "top_risks": [
    {{
      "device": "ip address",
      "port": 0,
      "service": "service name",
      "risk": "low | medium | high | unknown",
      "why_it_matters": "beginner-friendly explanation",
      "safe_fix": "defensive remediation"
    }}
  ],
  "recommendations": [
    "prioritized defensive recommendation"
  ],
  "next_steps": [
    "safe next validation step"
  ],
  "limitations": [
    "what this scan cannot prove"
  ]
}}

Risk guidance:
- High risk: remote admin, plaintext login, database exposure, file sharing, insecure legacy services.
- Medium risk: common services that need verification, access control, or patching.
- Low risk: expected services that still need monitoring.
- Unknown risk: not enough information.

Prioritization:
1. Exposed admin services first.
2. Plaintext or legacy protocols second.
3. Databases and file sharing third.
4. Web services fourth.
5. Unknown services last.

Scan data:
{scan_json}
""".strip()



# Accepts both base Ollama hosts and full endpoint links like /api/chat.
def normalize_ollama_host(host: str) -> str:
    clean_host = host.strip().rstrip("/")

    if clean_host.endswith("/api/chat"):
        return clean_host.removesuffix("/api/chat")

    if clean_host.endswith("/api/generate"):
        return clean_host.removesuffix("/api/generate")

    return clean_host


# Sends scan data to Ollama and returns the model's JSON response text.
def analyze_scan(report_data: dict, host: str, model: str) -> str:
    prompt = build_scan_prompt(report_data)
    ollama_host = normalize_ollama_host(host)
    client = Client(host=ollama_host, timeout=120)

    response = client.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format="json",
        stream=False,
    )

    return response["message"]["content"].strip()
