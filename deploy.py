import asyncio, base64, json, sys
from pathlib import Path
from sdk.tools.pd_vercel_token_auth import pd_vercel_token_auth_proxy_post

ROOT = Path("/work/projects/mediapulse")
FILES = ["index.html",
         "assets/hero.jpg", "assets/team1.jpg", "assets/team2.jpg",
         "assets/team3.jpg", "assets/team4.jpg"]

async def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "preview"
    files = []
    for f in FILES:
        data = (ROOT / f).read_bytes()
        files.append({"file": f, "data": base64.b64encode(data).decode(), "encoding": "base64"})
    body = {"name": "mediapulse", "project": "mediapulse", "files": files,
            "projectSettings": {"framework": None}}
    if target == "production":
        body["target"] = "production"
    res = await pd_vercel_token_auth_proxy_post(
        url="https://api.vercel.com/v13/deployments",
        query_params={"teamId": "team_OQDfLNrhsVEdGmu0hP11iY8W"},
        json_body=body,
    )
    print(json.dumps(res, default=str)[:3000])

asyncio.run(main())
