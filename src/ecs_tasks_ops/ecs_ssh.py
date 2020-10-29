"""Generate ssh commands to access to ECS resources"""

def ssh_cmd_container_instance(detail):
    return f"TERM=xterm ssh {detail['ec2InstanceId']}"

def ssh_cmd_task_log(detail):
    return f"TERM=xterm ssh {detail['ec2InstanceId']} docker logs -f --tail=100 {detail['containers'][0]['runtimeId']}"

def ssh_cmd_task_exec(detail, command_on_docker, wait_press_key=None):
    wait_cmd = ""
    if wait_press_key:
        wait_cmd = "; echo 'Press a key'; read q"
    return f"TERM=xterm ssh -t {detail['ec2InstanceId']} docker exec -ti {detail['containers'][0]['runtimeId']} {command_on_docker}" + wait_cmd

def ssh_cmd_docker_container_log(detail):
    return f"TERM=xterm ssh {detail['ec2InstanceId']} docker logs -f --tail=100 {detail['runtimeId']}"

def ssh_cmd_docker_container_exec(detail, command_on_docker, wait_press_key=None):
    wait_cmd = ""
    if wait_press_key:
        wait_cmd = "; echo 'Press a key'; read q"
    return f"TERM=xterm ssh -t {detail['ec2InstanceId']} docker exec -ti {detail['runtimeId']} {command_on_docker}"+ wait_cmd