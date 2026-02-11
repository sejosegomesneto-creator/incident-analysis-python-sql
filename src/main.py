import os
import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = "data/incidents.db"
REPORT_PATH = "reports/report.txt"

SEVERITIES = ["Low", "Medium", "High", "Critical"]
INCIDENT_TYPES = ["Brute Force", "Malware", "Phishing", "Port Scan", "Suspicious Login", "Data Exfil Attempt"]
SOURCE_IPS = ["192.168.1.10", "10.0.0.5", "172.16.0.3", "8.8.8.8", "45.33.32.156", "203.0.113.25"]
USERS = ["admin", "jose", "service_account", "guest", "analyst", "system"]


def ensure_dirs():
    os.makedirs("data", exist_ok=True)
    os.makedirs("reports", exist_ok=True)


def connect():
    return sqlite3.connect(DB_PATH)


def create_schema():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                username TEXT NOT NULL,
                incident_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)
        conn.commit()


def seed_data(rows: int = 120):
    """
    Gera incidentes simulados.
    Para evitar duplicar toda vez, só insere se a tabela estiver vazia.
    """
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM incidents")
        count = cur.fetchone()[0]
        if count > 0:
            return

        now = datetime.now()
        data = []
        for _ in range(rows):
            ts = now - timedelta(minutes=random.randint(1, 60 * 24 * 10))  # até 10 dias atrás
            source_ip = random.choice(SOURCE_IPS)
            username = random.choice(USERS)
            incident_type = random.choice(INCIDENT_TYPES)

            # regra simples pra deixar mais realista:
            if incident_type in ["Data Exfil Attempt", "Malware"]:
                severity = random.choices(SEVERITIES, weights=[5, 20, 35, 40])[0]
            elif incident_type in ["Brute Force", "Port Scan"]:
                severity = random.choices(SEVERITIES, weights=[20, 35, 30, 15])[0]
            else:
                severity = random.choices(SEVERITIES, weights=[35, 35, 20, 10])[0]

            description = f"{incident_type} detected for user '{username}' from IP {source_ip}"

            data.append((
                ts.strftime("%Y-%m-%d %H:%M:%S"),
                source_ip,
                username,
                incident_type,
                severity,
                description
            ))

        cur.executemany("""
            INSERT INTO incidents (timestamp, source_ip, username, incident_type, severity, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()


def query_one(cur, sql, params=None):
    cur.execute(sql, params or ())
    return cur.fetchall()


def analyze():
    with connect() as conn:
        cur = conn.cursor()

        total = query_one(cur, "SELECT COUNT(*) FROM incidents")[0][0]

        by_severity = query_one(cur, """
            SELECT severity, COUNT(*) as qtd
            FROM incidents
            GROUP BY severity
            ORDER BY qtd DESC
        """)

        top_ips = query_one(cur, """
            SELECT source_ip, COUNT(*) as qtd
            FROM incidents
            GROUP BY source_ip
            ORDER BY qtd DESC
            LIMIT 5
        """)

        top_users = query_one(cur, """
            SELECT username, COUNT(*) as qtd
            FROM incidents
            GROUP BY username
            ORDER BY qtd DESC
            LIMIT 5
        """)

        top_types = query_one(cur, """
            SELECT incident_type, COUNT(*) as qtd
            FROM incidents
            GROUP BY incident_type
            ORDER BY qtd DESC
            LIMIT 5
        """)

        recent_critical = query_one(cur, """
            SELECT timestamp, source_ip, username, incident_type
            FROM incidents
            WHERE severity = 'Critical'
            ORDER BY timestamp DESC
            LIMIT 10
        """)

    return {
        "total": total,
        "by_severity": by_severity,
        "top_ips": top_ips,
        "top_users": top_users,
        "top_types": top_types,
        "recent_critical": recent_critical
    }


def write_report(result: dict):
    lines = []
    lines.append("Incident Analysis Report (Python + SQL)")
    lines.append("=" * 42)
    lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"Total incidents: {result['total']}")
    lines.append("")

    def section(title):
        lines.append(title)
        lines.append("-" * len(title))

    section("Incidents by severity")
    for sev, qtd in result["by_severity"]:
        lines.append(f"- {sev}: {qtd}")
    lines.append("")

    section("Top 5 source IPs")
    for ip, qtd in result["top_ips"]:
        lines.append(f"- {ip}: {qtd}")
    lines.append("")

    section("Top 5 affected users")
    for user, qtd in result["top_users"]:
        lines.append(f"- {user}: {qtd}")
    lines.append("")

    section("Top 5 incident types")
    for itype, qtd in result["top_types"]:
        lines.append(f"- {itype}: {qtd}")
    lines.append("")

    section("Most recent Critical incidents (last 10)")
    if not result["recent_critical"]:
        lines.append("- None")
    else:
        for ts, ip, user, itype in result["recent_critical"]:
            lines.append(f"- {ts} | {itype} | {user} | {ip}")

    lines.append("")
    lines.append("Notes")
    lines.append("-----")
    lines.append("- Dataset is simulated for portfolio purposes.")
    lines.append("- SQL used: GROUP BY, ORDER BY, LIMIT, filtering by severity.")

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    print("🚀 Starting Incident Analysis with Python & SQL")
    ensure_dirs()
    create_schema()
    seed_data(rows=120)

    result = analyze()
    write_report(result)

    print("✅ Done!")
    print(f"📦 Database: {DB_PATH}")
    print(f"📄 Report:   {REPORT_PATH}")
    print("\nQuick summary:")
    print(f"Total incidents: {result['total']}")
    print("Top severities:", ", ".join([f"{s}:{q}" for s, q in result["by_severity"]]))


if __name__ == "__main__":
    main()

