import os
import subprocess
import sys

# Chuyen thu muc lam viec ve thu muc chua file script nay
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Lay thong tin Codespace de tao IP ket noi
codespace_name = os.environ.get("CODESPACE_NAME")
port_domain = os.environ.get("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev")

print("=" * 70)
print("             MINECRAFT FORGE 1.16.5 SERVER LAUNCHER")
print("=" * 70)

if codespace_name:
    public_ip = f"{codespace_name}-25565.{port_domain}"
    print(f"\n[+] Phat hien dang chay trong GitHub Codespace!")
    print(f"[+] Cong Server Minecraft: 25565")
    print(f"[+] DIA CHI IP DE KET NOI (Minecraft Server IP):")
    print(f"    \033[92m\033[1m{public_ip}\033[0m")
    print("\n[!] HUONG DAN KET NOI:")
    print("    1. Vao tab 'Ports' (Canh Terminal).")
    print("    2. Click chuot phai vao port 25565 -> Port Visibility -> Public.")
    print("    3. Copy dia chi tren vao muc Direct Connection trong game Minecraft.")
else:
    print(f"\n[+] Dang chay o may local.")
    print(f"[+] IP ket noi: localhost:25565")

# Tao thu muc crash-reports neu chua ton tai
os.makedirs("crash-reports", exist_ok=True)

print("=" * 70)
print("Khoi dong Minecraft Server... Vui long doi...")
print("=" * 70)

# Khoi chay server tuy theo he dieu hanh
try:
    # Cau hinh RAM toi thieu 4GB (-Xms4G) va toi da 8GB (-Xmx8G)
    ram_args = ["-Xms4G", "-Xmx8G", "-XX:+UseG1GC"]
    jar_file = "forge-1.16.5-36.2.42.jar"
    
    if os.name == 'nt':
        # Chay tren Windows
        # Tim Java 8 hoac 11 (Forge 1.16.5 can Java 8/11)
        import glob
        java_cmd = "java"
        possible_windows_patterns = [
            "C:\\Program Files\\Java\\jre1.8.*\\bin\\java.exe",
            "C:\\Program Files\\Java\\jdk1.8.*\\bin\\java.exe",
            "C:\\Program Files\\Java\\jre-11.*\\bin\\java.exe",
            "C:\\Program Files\\Java\\jdk-11.*\\bin\\java.exe",
            "C:\\Program Files (x86)\\Java\\jre1.8.*\\bin\\java.exe",
            "C:\\Program Files (x86)\\Java\\jdk1.8.*\\bin\\java.exe",
        ]
        found_java_paths = []
        for pattern in possible_windows_patterns:
            found_java_paths.extend(glob.glob(pattern))
            
        if found_java_paths:
            java_cmd = found_java_paths[0]
            print(f"[+] Tim thay Java 8/11 tai: {java_cmd}")
        else:
            print("[-] CANH BAO: Khong tim thay phien ban Java 8/11 trong he thong!")
            print("[+] Se thu dung lenh 'java' mac dinh cua he thong.")
            
        cmd = [java_cmd] + ram_args + ["-jar", jar_file, "nogui"]
        print(f"[+] Lenh khoi chay: {' '.join(cmd)}")
        if java_cmd == "java":
            subprocess.run(cmd, shell=True)
        else:
            subprocess.run(cmd)
    else:
        # Chay tren Linux / Codespace
        # Tim Java 8 hoac 11 (Forge 1.16.5 can Java 8/11 de hoat dong tot nhat)
        import glob
        java_cmd = "java"
        possible_patterns = [
            "/usr/local/sdkman/candidates/java/8*/bin/java",
            "/usr/local/sdkman/candidates/java/11*/bin/java",
            "/usr/lib/jvm/java-8*/bin/java",
            "/usr/lib/jvm/java-1.8.0*/bin/java",
            "/usr/lib/jvm/java-11*/bin/java",
            "/usr/lib/jvm/jdk-11*/bin/java",
            # Fallback sang Java 17 neu khong tim thay Java 8/11
            "/usr/local/sdkman/candidates/java/17*/bin/java",
            "/usr/lib/jvm/java-17*/bin/java",
        ]
        found_java_paths = []
        for pattern in possible_patterns:
            found_java_paths.extend(glob.glob(pattern))
        
        if found_java_paths:
            java_cmd = found_java_paths[0]
            print(f"[+] Tim thay Java tai: {java_cmd}")
        else:
            print("[-] CANH BAO: Khong tim thay phien ban Java phu hop (Java 8/11) trong he thong!")
            print("[+] Cac phien ban Java dang co san trong SDKMAN:")
            if os.path.exists("/usr/local/sdkman/candidates/java/"):
                try:
                    print("    " + ", ".join(os.listdir("/usr/local/sdkman/candidates/java/")))
                except Exception:
                    pass

        cmd = [java_cmd] + ram_args + ["-jar", jar_file, "nogui"]
        print(f"[+] Lenh khoi chay: {' '.join(cmd)}")
        subprocess.run(cmd)
except KeyboardInterrupt:
    print("\n[!] Dang tat server...")
except Exception as e:
    print(f"[!] Loi khi chay server: {e}")
