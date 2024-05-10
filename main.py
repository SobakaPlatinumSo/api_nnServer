from fastapi import FastAPI
import subprocess
from os import system
import uvicorn
import subprocess, shlex, pprint



app = FastAPI()

cmd = 'python3 /home/maks/stable-diffusion-webui/webui.py --listen --no-half --api'
args = shlex.split(cmd)

# System

@app.get("/system/reboot") # перезапуск
async def Reboot():
        system('reboot')
        return {"message" : "ok"}


# NN

@app.get("/nn/automatic/start") # включение automatic
async def start_automatic():
        result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        for line in result.stdout.splitlines():
                if "python3 /home/maks/stable-diffusion-webui/webui.py" in line:
                    return {"message" : "already started"}
        p = subprocess.Popen(args)
        return {"message" : "Successfully started"}

@app.get("/nn/automatic/status") # статус automatic
async def status_automatic():
        result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        for line in result.stdout.splitlines():
                if "python3 /home/maks/stable-diffusion-webui/webui.py" in line:
                    return {"message" : True}

        return {"message" : False}

@app.get("/nn/automatic/kill") # выключение automatic
async def kill_automatic():
        result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        for line in result.stdout.splitlines():
                if "python3 /home/maks/stable-diffusion-webui/webui.py" in line:
                        res = line.split()[1]
                        print(res)
                        system(f'kill {res}')
                        return {"message" : "killed"}
        return {"message" : "Not started"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
