import subprocess
import sys
import time

"""

Configuration Variables
* Note that this code works only in Windows

"""

# GitHub .ssh credential file location on Windows
GITHUB_SECRET_PATH = "~/.ssh/ywcheong-github"

# GitHub project name (e.g., user/repo)
GITHUB_PROJECT_NAME = "ywcheong/solved-baekjoon"

# Git user email
GIT_USER_EMAIL = "tencise@gmail.com"

# Git user name
GIT_USER_NAME = "ywcheong"

# Docker Project Name (-image, -container)
DOCKER_NAME = "solved-baekjoon"

# Docker Installation Location
DOCKER_EXECUTABLE = "C:/Program Files/Docker/Docker/Docker Desktop.exe"


def launch_docker_desktop():
    if check_docker_running():
        return

    print("launching docker desktop... ", end="")
    powershell_launch_docker = ["Start-Process", f'"{DOCKER_EXECUTABLE}"']

    try:
        subprocess.run(
            ["powershell", "-Command"] + powershell_launch_docker, check=True
        )
        print("success.")
    except subprocess.CalledProcessError:
        print("failed. bye")
        sys.exit(1)
    else:
        print("waiting for ready... ", end="")
        time.sleep(10)
        print("done.")

        if not check_docker_running():
            print("Docker Desktop is not running. Please start it manually.")
            sys.exit(1)


def check_docker_running():
    print("checking docker desktop... ", end="")
    try:
        subprocess.run(
            ["docker", "info"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("running.")
        return True
    except subprocess.CalledProcessError:
        print("not running.")
        return False


def build_docker_image():
    print("building docker image... ", end="")
    build_command = [
        "docker",
        "build",
        "-t",
        DOCKER_NAME + "-image",
        "--build-arg",
        f"GITHUB_PROJECT_NAME={GITHUB_PROJECT_NAME}",
        ".",
    ]
    subprocess.run(build_command, check=True)
    print(f"image now available({DOCKER_NAME}-image). bye")


def run_docker_container():
    print("running docker container... ", end="")
    run_command = [
        "docker",
        "run",
        "-d",
        "-v",
        f"{GITHUB_SECRET_PATH}:/root/.ssh/id_rsa",
        "-e",
        f"GIT_USER_NAME={GIT_USER_NAME}",
        "-e",
        f"GIT_USER_EMAIL={GIT_USER_EMAIL}",
        "-e",
        f"GITHUB_PROJECT_NAME={GITHUB_PROJECT_NAME}",
        "--name",
        DOCKER_NAME + "-container",
        "--rm",
        DOCKER_NAME + "-image",
    ]
    subprocess.run(["powershell", "-Command"] + run_command, check=True)
    print(f"container now online({DOCKER_NAME}-container). bye")


def main():
    if len(sys.argv) != 2:
        print("usage: python solve-docker.py [build|run]")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "build":
        launch_docker_desktop()
        build_docker_image()
    elif action == "run":
        launch_docker_desktop()
        run_docker_container()
    else:
        print("usage: python solve-docker.py [build|run]")
        sys.exit(1)


if __name__ == "__main__":
    main()
