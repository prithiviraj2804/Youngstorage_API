def domainLable(username:str,domains:list):
    domainName = "youngstorage.tech"
    txt = ""

    for i,data in enumerate(domains):
        if i==0:
            txt += f"Host(`{data}.{domainName}`)"
        elif i>0:
            txt += f" || Host(`{data}.{domainName}`)"
    return {
    f"traefik.http.routers.{username}.rule":f"{txt}",
    f"traefik.http.routers.{username}.service":f"{username}",
    f"traefik.http.services.{username}.loadbalancer.server.port":"80",
    f"traefik.http.routers.{username}.tls":"true",
    f"traefik.http.routers.labs.tls.certresolver":"custom_resolver",
    f"traefik.http.routers.{username}.entrypoints":"websecure",
    }

    

domainlist = ["bhadri","anish","madara","minato"]


print(domainLable("bhadri2002",domainlist))