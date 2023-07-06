import os


def labelGenerator(imageid):
    return {"traefik.enable": "true",
            f"traefik.http.routers.{imageid}.rule": f"Host(`{imageid}.{os.getenv('DOMAIN_NAME')}`)",
            f"traefik.http.routers.{imageid}.service": f"{imageid}",
            f"traefik.http.routers.{imageid}.tls": "true",
            f"traefik.http.routers.{imageid}.entrypoints": "websecure",
            f"traefik.http.services.{imageid}.loadbalancer.server.port": "1111",
            }
