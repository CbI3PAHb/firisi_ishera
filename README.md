### Simple ML model

### Requirements

1. [Github](https://github.com/)
2. [Git](https://git-scm.com/)
3. [VS Code](https://code.visualstudio.com/)
4. [Fastapi](https://fastapi.tiangolo.com/)
5. [Docker](https://www.docker.com/)

Create a new environment

```
python3 -m venv venv
```

Activate the environment

```
source venv/bin/activate
```

Install requirements.txt
```
pip install -r requirements.txt
```

to be commited ->
```
git add .
```

Commit
```
git commit -m "This commit includes requirement.txt and readme file"
```

Push
```
git push origin main
```

run docker container
```
sudo docker run -d -p 8000:80 myimage:2.0
```