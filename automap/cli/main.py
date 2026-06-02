import asyncio
from enum import Enum
import json
import os 
from pathlib import Path

import typer
from rich.console import Console


from automap.analysis.ai import analyze_scan
from automap.reporting.markdown import render_report


from automap.scanner.discovery import devices
from automap.scanner.ports import (
    build_port_results,
    get_port_count_for_mode,
    get_port_preview_for_mode,
    get_ports_mode,
    scan_ports_for_host,
)

app = typer.Typer(help="AutoMap - AI Security Analyst for Local Networks")
console = Console()



if os.getuid() !=0:
    console.print("[bold red]Error: This program must be run as root.[/bold red]")
    raise typer.Exit(1)




@app.callback()
def main():
    # AutoMap command line interface entry point.
    console.print("[dim]Powered By Pharosys[/dim]")


class ScanMode(str, Enum):
    smart = "smart"
    quick = "quick"
    full = "full"





#here the programm is calling the port scanned and the number of ports selected with the help of scan mode 
@app.command()
def scan(
    target: str = typer.Argument(..., help="IP address or target range to scan"),
    mode: ScanMode = typer.Option(ScanMode.smart, "--mode", "-m", help="Scan mode"),
    ai: bool = typer.Option(True, "--ai/--no-ai", help="Enable or disable AI analysis"),
    ai_host: str | None = typer.Option(None, "--ai-host", help="Bring your own Ollama host URL, accepts base host or /api/chat link"),
    ai_model: str | None = typer.Option(None, "--ai-model", help="Bring your own Ollama model name"),
    report: Path = typer.Option(Path("automap-report.md"), "--report", "-r", help="Markdown report output path"),
):
    # Discovers devices in a target range, scans ports, then runs AI analysis.
    console.print("[bold cyan]AutoMap Scan Started[/bold cyan]")
    console.print("[dim]Powered By Pharosys[/dim]")
    console.print(f"IP: [bold cyan]{target}[/bold cyan]")
    console.print(f"Mode: [bold magenta]{mode.value}[/bold magenta]")
    if ai and ai_model and ai_host:
        console.print(f"AI Model: [bold magenta]{ai_model}[/bold magenta]")
        console.print(f"AI Host: [dim]{ai_host}[/dim]")
    elif ai:
        console.print("[yellow]AI disabled: pass --ai-host and --ai-model to enable BYOO analysis.[/yellow]")
        ai = False

    port_count = get_port_count_for_mode(mode.value)
    port_preview = get_port_preview_for_mode(mode.value)
    ports = get_ports_mode(mode.value)

    console.print(f"Ports selected: [green]{port_count}[/green]")
    console.print(f"Port preview: [dim]{', '.join(map(str, port_preview))}[/dim]")
    console.print(f"Report: [bold cyan]{report}[/bold cyan]")

    console.print("[bold red]Starting the scan...[/bold red]")
    
    devices_found = devices(target)  
    
    if not devices_found:
        console.print("[dim]No devices found on the network.[/dim]")
    

    result_devices = {}
    for device in devices_found:
        ip = device["IP"]
        mac = device["MAC"]
        console.print(f"Scanning device: [green]{ip}[/green]")
        open_ports = asyncio.run(scan_ports_for_host(ip, ports))
        port_results = build_port_results(open_ports)
        result_devices[ip] = {"ip": ip, "mac": mac, "open_ports": port_results}

    total_devices = len(result_devices)
    total_open_ports = 0
    
    for device_result in result_devices.values():
        total_open_ports += len(device_result["open_ports"])
        
    console.print("\n[bold cyan]Scan Summary[/bold cyan]")
    console.print(f"Devices scanned: [green]{total_devices}[/green]")
    console.print(f"Open ports found: [yellow]{total_open_ports}[/yellow]")

    report_data = {
        "target": target,
        "mode": mode.value,
        "summary": {
            "devices_scanned": total_devices,
            "open_ports_found": total_open_ports,
        },
        "devices": list(result_devices.values()),
    }

    if ai:
        console.print("[bold magenta]Running AI analysis...[/bold magenta]")
        ai_report_text = analyze_scan(report_data, host=ai_host, model=ai_model)

        try:
            ai_report = json.loads(ai_report_text)
        except json.JSONDecodeError:
            ai_report = {
                "summary": ai_report_text,
                "network_posture": "unknown",
                "top_risks": [],
                "recommendations": [],
                "next_steps": [],
                "limitations": ["AI response was not valid JSON."],
            }

        report_data["ai_analysis"] = ai_report
        console.print("[green]AI analysis complete.[/green]")
    else:
        report_data["ai_analysis"] = {}

    report.write_text(render_report(report_data), encoding="utf-8")
    console.print(f"[bold green]Report saved to root of the Project:[/bold green] {report}")
        


if __name__ == "__main__":
    app()
