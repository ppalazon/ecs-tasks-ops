"""Urwid data conversor from ECS facade"""

import urwid
from ecs_tasks_ops import ecs_data


class EcsButton(urwid.Button):

    def __init__(self, identifier, name, detail):
        self.identifier = identifier
        self.detail = detail
        self.name = name
        self.showing_detail = False
        super(EcsButton, self).__init__(name)

    def retrieve_important_details(self):
        return []

    def retrieve_children(self):
        return (None, [])

    def retrieve_by_highlight(self, key):
        return (None, [])

    def special_action(self, key):
        return (None, [])

    def contains_word(self, word):
        return word.lower() in self.name.lower()

class Cluster(EcsButton):

    def __init__(self, identifier, name, detail):
        super(Cluster, self).__init__(identifier, name, detail)

    def retrieve_important_details(self):
        return [("Status", self.detail['status']),
                (["Active ", ('key', "S"), "ervices"], self.detail['activeServicesCount']),
                (["Running ", ('key', "T"), "asks"], self.detail['runningTasksCount']),
                ("Pending Tasks", self.detail['pendingTasksCount']),
                ([('key',"C"), "ontainers"], self.detail['registeredContainerInstancesCount'])]

    def retrieve_children(self):
        return (f"Cluster '{self.name}'", [TasksLabel(self.identifier), ServicesLabel(self.identifier), ContainersLabel(self.identifier)])

    def retrieve_by_highlight(self, key):
        if key == "T":
            return (f"Tasks '{self.name}'", [Task(None, self.identifier, t['name'], t) for t in ecs_data.get_tasks_cluster(self.identifier)], None)
        if key == "S":
            return (f"Services '{self.name}'", [Service(s['serviceArn'], s['serviceName'], self.identifier, s) for s in ecs_data.get_services(self.identifier)], None)
        if key == "C":
            return (f"Containers '{self.name}'", [Container(c['containerInstanceArn'], c['ec2InstanceId'], self.identifier, c) for c in ecs_data.get_containers_instances(self.identifier)], None)
        else:
            return (None, [])


class TasksLabel(EcsButton):
    def __init__(self, cluster_identifier):
        super(TasksLabel, self).__init__(cluster_identifier, "Tasks", "")

    def retrieve_children(self):
        return (f"Tasks '{self.identifier}'", [Task(None, self.identifier, t['name'], t) for t in ecs_data.get_tasks_cluster(self.identifier)], None)


class ServicesLabel(EcsButton):
    def __init__(self, cluster_identifier):
        super(ServicesLabel, self).__init__(cluster_identifier, "Services", "")

    def retrieve_children(self):
        return (f"Services '{self.identifier}'", [Service(s['serviceArn'], s['serviceName'], self.identifier, s) for s in ecs_data.get_services(self.identifier)])


class ContainersLabel(EcsButton):
    def __init__(self, cluster_identifier):
        super(ContainersLabel, self).__init__(
            cluster_identifier, "Containers", "")

    def retrieve_children(self):
        return (f"Containers '{self.identifier}'", [Container(c['containerInstanceArn'], c['ec2InstanceId'], self.identifier, c) for c in ecs_data.get_containers_instances(self.identifier)], None)


class Container(EcsButton):

    def __init__(self, identifier, name, cluster_identifier, detail):
        super(Container, self).__init__(identifier, name, detail)
        self.cluster_identifier = cluster_identifier

    def retrieve_children(self):
        return (f"Tasks '{self.name}'", [Task(self.identifier, self.cluster_identifier, t['name'], t) for t in ecs_data.get_tasks_container_instance(self.cluster_identifier, self.identifier)], None)

    def retrieve_important_details(self):
        ci = self.detail
        return [('Status', ci['status']),
                ('EC2 Instance Id', ci['ec2InstanceId']),
                # (['Private ', ('key', 'I'), 'P'], self.detail[1]['PrivateIpAddress']),
                # ('Private DNS Name', self.detail[1]['PrivateDnsName']),
                # ('Public DNS Name', self.detail[1]['PublicDnsName']),
                (['Running ', ('key','T'), 'asks'], ci['runningTasksCount']),
                ('Pending Tasks', ci['pendingTasksCount']),
                ('AMI Id', ci['ami_id']),
                ('Instance Type', ci['instance_type']),
                ('Availability Zone', ci['availability_zone']),
                ('Memory', 'Available: ' + str(ci['available_memory']) +" Total: " + str(ci['total_memory'])),
                ('CPU', 'Available: ' + str(ci['available_cpu']) +" Total: " + str(ci['total_cpu'])),
                ('Taken ports', ci['taken_ports'])]


    def retrieve_by_highlight(self, key):
        if key == "T":
            return (f"Tasks '{self.name}'", [Task(self.identifier, self.cluster_identifier, t['name'], t) for t in ecs_data.get_tasks_container_instance(self.cluster_identifier, self.identifier)], None)
        else:
            return (None, [])

    def special_action(self, key):
        if key == "I":
            return ("SSH", self.detail['ec2InstanceId'])
        else:
            return (None, [])

class Service(EcsButton):

    def __init__(self, identifier, name, cluster_identifier, detail):
        super(Service, self).__init__(identifier, name, detail)
        self.cluster_identifier = cluster_identifier

    def retrieve_children(self):
        return (f"Tasks '{self.name}'", [Task(self.identifier, self.cluster_identifier, t['name'], t) for t in ecs_data.get_tasks_service(self.cluster_identifier, self.identifier)])

    def retrieve_important_details(self):
        deployment_config = self.detail['deploymentConfiguration']
        min_bracket = deployment_config['minimumHealthyPercent']
        max_bracket = deployment_config['maximumPercent']

        return [('Status', self.detail['status']),
                ('Task Definition', self.detail['taskDefinition']),
                ('Running', self.detail['runningCount']),
                ('Pending', self.detail['pendingCount']),
                ('Desired', self.detail['desiredCount']),
                ('Redeployment bracket', "Min: " + str(min_bracket) + "%, Max: " + str(max_bracket) + "%")]


class Task(EcsButton):

    def __init__(self, service_identifier, cluster_identifier, identifier, detail):
        super(Task, self).__init__(identifier, identifier, detail)
        self.service_identifier = service_identifier
        self.cluster_identifier = cluster_identifier

    def retrieve_children(self):
        return (f"Docker Containers '{self.name}'", [DockerContainer(self.identifier, self.cluster_identifier, t['name'], t) for t in ecs_data.get_containers_tasks(self.cluster_identifier, self.detail['taskArn'])])

    def retrieve_important_details(self):
        return [('Status', self.detail['lastStatus']),
                ('Desired Status', self.detail['desiredStatus']),
                ('EC2 Instance', self.detail['ec2InstanceId']),
                ('Task Definition', self.detail['taskDefinitionArn']),
                (['Container ', ('key', 'I'), 'nstance ID'], self.detail['containerInstanceArn'].split("/", 1)[1]),
                ('N. Docker images', len(self.detail['containers'])),
                ('Networks', '\n'.join(self.detail['networks']))]

    def special_action(self, key):
        first_container = self.detail['containers'][0]
        if key == "I":
            return ("SSH", self.detail['ec2InstanceId'])
        if key == "C":            
            return ("SSH", "-t "+ self.detail['ec2InstanceId']+" docker exec -ti "+first_container['runtimeId']+" /bin/sh")
        if key == "L":
            return ("SSH", self.detail['ec2InstanceId']+" docker logs -f --tail=100 "+first_container['runtimeId'])
        else:
            return (None, [])


class DockerContainer(EcsButton):

    def __init__(self, task_identifier, cluster_identifier, identifier, detail):
        super(DockerContainer, self).__init__(identifier, identifier, detail)
        self.task_identifier = task_identifier
        self.cluster_identifier = cluster_identifier

    def retrieve_important_details(self):
        return [('Container Arn', self.detail['containerArn']),
                ('Status', self.detail['lastStatus']),
                ('Health Status', self.detail['healthStatus']),
                ('Docker id', self.detail['runtimeId']),
                ('Docker Image', self.detail['image']),
                ('CPU', self.detail['cpu']),
                #('Memory Reservation', self.detail['memoryReservation']),
                ('Instance ID', self.detail['ec2InstanceId']),
                ('Networks', self.detail['networks'])]

    def special_action(self, key):
        if key == "I":
            return ("SSH", self.detail['ec2InstanceId'])
        if key == "C":
            return ("SSH", "-t "+ self.detail['ec2InstanceId']+" docker exec -ti "+self.detail['runtimeId']+" /bin/sh")
        if key == "L":
            return ("SSH", self.detail['ec2InstanceId']+" docker logs -f --tail=100 "+self.detail['runtimeId'])
        else:
            return (None, [])