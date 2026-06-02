from datetime import datetime


# Returns a visual icon for a risk level.
def risk_icon(risk: str) -> str:
    risk = str(risk).strip().lower()

    if risk in ("critical", "high"):
        return "🔴"
    if risk in ("medium", "med"):
        return "🟡"
    if risk == "low":
        return "🟢"

    return "⚪"


# Keeps Markdown tables from breaking when text contains pipes or newlines.
def table_text(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ").strip()


# Detects weak model output where the AI copied the prompt schema.
def is_template_text(value: object) -> bool:
    text = str(value).strip().lower()

    if not text:
        return True

    template_phrases = (
        "short overall explanation",
        "low | medium | high | unknown",
        "ip address",
        "service name",
        "beginner-friendly explanation",
        "defensive remedy",
        "defensive remediation",
        "prioritized recommendations",
        "safe next validation step",
        "what this scan cannot prove",
    )

    return any(phrase in text for phrase in template_phrases)


# Removes empty strings and copied prompt-template values from AI lists.
def clean_text_list(items: object) -> list[str]:
    if not isinstance(items, list):
        return []

    clean_items = []
    for item in items:
        if isinstance(item, str) and not is_template_text(item):
            clean_items.append(item.strip())

    return clean_items


# Finds the highest actual port risk from scan results.
def highest_scan_risk(devices: list[dict]) -> str:
    risk_rank = {"unknown": 0, "low": 1, "medium": 2, "med": 2, "high": 3, "critical": 4}
    highest = "unknown"

    for device in devices:
        for port in device.get("open_ports", []):
            risk = str(port.get("risk", "unknown")).lower()
            if risk_rank.get(risk, 0) > risk_rank.get(highest, 0):
                highest = risk

    return "medium" if highest == "med" else highest


# Keeps only AI risks that match real devices and real open ports.
def clean_top_risks(ai: dict, devices: list[dict]) -> list[dict]:
    valid_ports = {}
    for device in devices:
        ip = device.get("ip")
        valid_ports[ip] = {port.get("port") for port in device.get("open_ports", [])}

    clean_risks = []
    for risk in ai.get("top_risks", []):
        if not isinstance(risk, dict):
            continue

        device = risk.get("device")
        port = risk.get("port")

        if device not in valid_ports or port not in valid_ports[device]:
            continue

        if is_template_text(risk.get("why_it_matters", "")):
            continue

        clean_risks.append(risk)

    return clean_risks


# Generates the final Markdown report from scan data and optional AI analysis.
def render_report(data: dict) -> str:
    summary = data.get("summary", {})
    devices = data.get("devices", [])
    ai = data.get("ai_analysis", {})

    total_devices = summary.get("devices_scanned", len(devices))
    total_ports = summary.get(
        "open_ports_found",
        sum(len(device.get("open_ports", [])) for device in devices),
    )
    highest_risk = highest_scan_risk(devices)
    ai_summary = ai.get("summary", "")
    ai_risks = clean_top_risks(ai, devices)
    recommendations = clean_text_list(ai.get("recommendations", []))
    next_steps = clean_text_list(ai.get("next_steps", []))
    limitations = clean_text_list(ai.get("limitations", []))
    has_ai_content = (
        isinstance(ai_summary, str)
        and not is_template_text(ai_summary)
    ) or ai_risks or recommendations or next_steps
    ai_status = "Skipped"

    if ai.get("error"):
        ai_status = "Failed"
    elif ai and has_ai_content:
        ai_status = "Completed"
    elif ai:
        ai_status = "Filtered"

    lines = []

    lines.append("# 🛡️ AutoMap Scan Report\n")
    lines.append(f"**Target Range:** `{data.get('target', 'unknown')}`")
    lines.append(f"**Generated:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append(f"**Scan Mode:** `{str(data.get('mode', 'unknown')).title()}`\n")
    lines.append("---\n")

    lines.append("## 📊 Executive Summary\n")
    lines.append("| Metric | Detail |")
    lines.append("| --- | --- |")
    lines.append(f"| **Devices Discovered** | {total_devices} |")
    lines.append(f"| **Total Open Ports** | {total_ports} |")
    lines.append(f"| **Highest Risk Found** | {risk_icon(highest_risk)} {highest_risk.title()} |")
    lines.append(f"| **AI Analysis** | {ai_status} |")
    lines.append("")

    lines.append("---\n")
    lines.append("## 🤖 AI Security Analysis\n")

    if ai.get("error"):
        lines.append("> [!WARNING]")
        lines.append("> AI analysis could not run because AutoMap could not reach the configured Ollama host.")
    elif total_devices == 0:
        lines.append("> No devices were discovered, so there is no device-level security analysis to show.")
    elif total_ports == 0:
        lines.append("> Devices were discovered, but no selected TCP ports were open in this scan mode.")
    elif isinstance(ai_summary, str) and not is_template_text(ai_summary):
        lines.append(f"> **Summary:** {ai_summary}")
    else:
        lines.append(f"> AutoMap found {total_ports} open port(s) across {total_devices} discovered device(s).")

    if ai_risks:
        lines.append(">\n> **Top Risks:**")
        for risk in ai_risks:
            risk_level = str(risk.get("risk", "unknown")).lower()
            lines.append(
                f"> - {risk_icon(risk_level)} `{risk.get('device')}:{risk.get('port')}` "
                f"{table_text(risk.get('service', 'Unknown'))}: "
                f"{table_text(risk.get('why_it_matters', 'Needs review'))}"
            )

    if recommendations:
        lines.append(">\n> **Key Recommendations:**")
        for index, recommendation in enumerate(recommendations, 1):
            lines.append(f"> {index}. {recommendation}")

    if next_steps:
        lines.append(">\n> **Next Steps:**")
        for step in next_steps:
            lines.append(f"> - {step}")

    lines.append("")
    lines.append("---\n")
    lines.append("## 📡 Network Inventory\n")

    if not devices:
        lines.append("No devices were discovered in this scan.\n")
    else:
        for device in devices:
            ip = device.get("ip", "unknown")
            mac = device.get("mac", "unknown")
            ports = device.get("open_ports", [])
            device_risk = highest_scan_risk([device])

            lines.append(f"### 📍 Device: `{ip}`\n")
            lines.append(f"- **MAC Address:** `{mac}`")
            lines.append(f"- **Status:** {risk_icon(device_risk)} {device_risk.title()}\n")

            if not ports:
                lines.append("No open ports detected.\n")
                continue

            lines.append("| Port | Service | Risk | Notes |")
            lines.append("| --- | --- | --- | --- |")

            for port in ports:
                risk = str(port.get("risk", "unknown")).lower()
                protocol = str(port.get("protocol", "tcp")).lower()
                service = table_text(port.get("service", "Unknown"))
                lines.append(
                    f"| `{port.get('port')}/{protocol}` | {service} | "
                    f"{risk_icon(risk)} {risk.title()} | Review exposure and access control |"
                )

            lines.append("")

    if limitations:
        lines.append("---\n")
        lines.append("## ⚠️ Limitations\n")
        for limitation in limitations:
            lines.append(f"- {limitation}")
        lines.append("")

    lines.append("---\n")
    lines.append("_Report generated by AutoMap_")
    lines.append("_Powered By Pharosys_")

    return "\n".join(lines)
