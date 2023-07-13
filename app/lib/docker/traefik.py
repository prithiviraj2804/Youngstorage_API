import os


def labelGenerator(imageid: str):
    return {"traefik.enable": "true",
            f"traefik.http.routers.{imageid}.rule": f"Host(`{imageid}.{os.getenv('DOMAIN_NAME')}`)",
            f"traefik.http.routers.{imageid}.service": f"{imageid}",
            f"traefik.http.routers.{imageid}.tls": "true",
            f"traefik.http.routers.{imageid}.entrypoints": "websecure",
            f"traefik.http.services.{imageid}.loadbalancer.server.port": "1111",
            }

def domainLableGenerator(username:str,domains:list):
    domainName = os.getenv("DOMAIN_NAME")
    txt = ""

    for i,data in enumerate(domains):
        if i==0:
            txt += f"Host(`{data['domainName']}.{domainName}`)"
        elif i>0:
            txt += f" || Host(`{data['domainName']}.{domainName}`)"
    return {
    f"traefik.http.routers.{username}.rule":f"{txt}",
    f"traefik.http.routers.{username}.service":f"{username}",
    f"traefik.http.services.{username}.loadbalancer.server.port":"80",
    f"traefik.http.routers.{username}.tls":"true",
    f"traefik.http.routers.labs.tls.certresolver":"custom_resolver",
    f"traefik.http.routers.{username}.entrypoints":"websecure",
    }
