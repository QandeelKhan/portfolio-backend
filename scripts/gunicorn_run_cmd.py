def generate_run_command(project_name):
    return f"gunicorn --worker-tmp-dir /dev/shm {project_name}.wsgi:application"


project_name = input(
    "Please enter project name to generate its gunicorn cmd: ")
run_command = generate_run_command(project_name)
print(run_command)
