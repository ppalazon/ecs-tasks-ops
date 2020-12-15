"""Urwid data conversor from ECS facade."""
from typing import Any
from typing import List
from typing import Tuple

import urwid

from ecs_tasks_ops import ecs_data
from ecs_tasks_ops import ecs_ssh


UrwidData = Tuple[str, Any]


class EcsButton(urwid.Button):
    """Specific button for ECS elements."""

    def __init__(self, identifier: str, name: str, detail: UrwidData) -> None:
        """Create a new Element for ECS.

        Args:
            identifier (str): Unique identification for element, it could be aws arn
            name (str): Name for visual identification of element
            detail (UrwidData): JSON information from ECS
        """
        self.identifier = identifier
        self.detail = detail
        self.name = name
        self.showing_detail = False
        super(EcsButton, self).__init__(name)

    def retrieve_important_details(self) -> List[Any]:
        """Get a list of details as attributes as name / values.

        Returns:
            List[Any]: List of typles with name and value
        """
        return []

    def retrieve_children(self) -> UrwidData:
        """Request children for this element of this element.

        Returns:
            UrwidData: Tuple where first element is a name, and the second is a list
        """
        return ("", [])

    def retrieve_by_highlight(self, key: str) -> UrwidData:
        """Get element children when you hit a key.

        Args:
            key (str): Pressed key character

        Returns:
            UrwidData: Tuple with a title and a list of elements
        """
        return ("", [])

    def special_action(self, key: str) -> UrwidData:
        """Execute an special action pressing a key.

        Args:
            key (str): Key pressed character

        Returns:
            UrwidData: Tuple with name command and command
        """
        return ("", [])

    def contains_word(self, word: str) -> bool:
        """Check the name of the element contains this word.

        Args:
            word (str): Word to search

        Returns:
            bool: Return if this element name contains this word
        """
        return word.lower() in self.name.lower()


class Cluster(EcsButton):
    """Specific button for ECS Clusters elements."""

    def __init__(self, identifier: str, name: str, detail: UrwidData) -> None:
        """Create a new Cluster Element.

        Args:
            identifier (str): Unique identification for element, it could be aws arn
            name (str): Name for visual identification of element
            detail (UrwidData): JSON information from ECS
        """
        super(Cluster, self).__init__(identifier, name, detail)

    def retrieve_important_details(self) -> List[Any]:
        """Get a list of details as attributes as name / values.

        Returns:
            List[Any]: List of typles with name and value
        """
        return [
            ("Status", self.detail["status"]),
            (["Active ", ("key", "S"), "ervices"], self.detail["activeServicesCount"]),
            (["Running ", ("key", "T"), "asks"], self.detail["runningTasksCount"]),
            ("Pending Tasks", self.detail["pendingTasksCount"]),
            (
                [("key", "C"), "ontainers"],
                self.detail["registeredContainerInstancesCount"],
            ),
        ]

    def retrieve_children(self) -> UrwidData:
        """Show a menu to get Tasks, Services and Container of this cluster.

        Returns:
            UrwidData: Tuple where first element is a name, and the second is a list
        """
        return (
            f"Cluster '{self.name}'",
            [
                TasksLabel(self.identifier),
                ServicesLabel(self.identifier),
                ContainersLabel(self.identifier),
            ],
        )

    def retrieve_by_highlight(self, key: str) -> UrwidData:
        """Get element children when you hit a key.

        Args:
            key (str): Pressed key character

        Returns:
            UrwidData: Tuple with a title and a list of elements
        """
        if key == "T":
            return (
                f"Tasks '{self.name}'",
                [
                    Task(None, self.identifier, t["name"], t)
                    for t in ecs_data.get_tasks_cluster(self.identifier)
                ],
            )
        if key == "S":
            return (
                f"Services '{self.name}'",
                [
                    Service(s["serviceArn"], s["serviceName"], self.identifier, s)
                    for s in ecs_data.get_services(self.identifier)
                ],
            )
        if key == "C":
            return (
                f"Containers '{self.name}'",
                [
                    Container(
                        c["containerInstanceArn"],
                        c["ec2InstanceId"],
                        self.identifier,
                        c,
                    )
                    for c in ecs_data.get_containers_instances(self.identifier)
                ],
            )
        else:
            return (None, [])


class TasksLabel(EcsButton):
    """Specific button for ECS Tasks elements."""

    def __init__(self, cluster_identifier: str) -> None:
        """Create a new TaskLabel Element.

        Args:
            cluster_identifier (str): Cluster unique identification
        """
        super(TasksLabel, self).__init__(cluster_identifier, "Tasks", "")

    def retrieve_children(self) -> UrwidData:
        """Get a list of tasks of this cluster.

        Returns:
            UrwidData: Tuple where first element is a name, and the second is a list
        """
        return (
            f"Tasks '{self.identifier}'",
            [
                Task(None, self.identifier, t["name"], t)
                for t in ecs_data.get_tasks_cluster(self.identifier)
            ],
        )


class ServicesLabel(EcsButton):
    """Specific button for ECS Services elements."""

    def __init__(self, cluster_identifier: str) -> None:
        """Create a new ServiceLabel Element.

        Args:
            cluster_identifier (str): Cluster unique identification
        """
        super(ServicesLabel, self).__init__(cluster_identifier, "Services", "")

    def retrieve_children(self) -> List[Any]:
        """Get a list of services of this cluster.

        Returns:
            List[Any]: Tuple where first element is a name, and the second is a list
        """
        return (
            f"Services '{self.identifier}'",
            [
                Service(s["serviceArn"], s["serviceName"], self.identifier, s)
                for s in ecs_data.get_services(self.identifier)
            ],
        )


class ContainersLabel(EcsButton):
    """Specific button for ECS Container Label elements."""

    def __init__(self, cluster_identifier: str) -> None:
        """Create a new ContainersLabel Element.

        Args:
            cluster_identifier (str): Cluster unique identification
        """
        super(ContainersLabel, self).__init__(cluster_identifier, "Containers", "")

    def retrieve_children(self) -> UrwidData:
        """Get a list of containers of this cluster.

        Returns:
            UrwidData: Tuple where first element is a name, and the second is a list
        """
        return (
            f"Containers '{self.identifier}'",
            [
                Container(
                    c["containerInstanceArn"], c["ec2InstanceId"], self.identifier, c
                )
                for c in ecs_data.get_containers_instances(self.identifier)
            ],
        )


class Container(EcsButton):
    """Specific button for ECS Container elements."""

    def __init__(
        self,
        identifier: str,
        name: str,
        cluster_identifier: str,
        detail: UrwidData,
    ) -> None:
        """Create a new Container Element.

        Args:
            identifier (str): Unique identification for element, it could be aws arn
            name (str): Name for visual identification of element
            cluster_identifier (str): Cluster unique identification
            detail (UrwidData): JSON information from ECS
        """
        super(Container, self).__init__(identifier, name, detail)
        self.cluster_identifier = cluster_identifier

    def retrieve_children(self) -> UrwidData:
        """Get a list of tasks for this container.

        Returns:
            UrwidData: Tuple where first element is a name, and the second is a list
        """
        return (
            f"Tasks '{self.name}'",
            [
                Task(self.identifier, self.cluster_identifier, t["name"], t)
                for t in ecs_data.get_tasks_container_instance(
                    self.cluster_identifier, self.identifier
                )
            ],
        )

    def retrieve_important_details(self) -> List[Any]:
        """Get a list of details as attributes as name / values.

        Returns:
            List[Any]: List of typles with name and value
        """
        ci = self.detail
        return [
            ("Status", ci["status"]),
            ("EC2 Instance Id", ci["ec2InstanceId"]),
            # (['Private ', ('key', 'I'), 'P'], self.detail[1]['PrivateIpAddress']),
            # ('Private DNS Name', self.detail[1]['PrivateDnsName']),
            # ('Public DNS Name', self.detail[1]['PublicDnsName']),
            (["Running ", ("key", "T"), "asks"], ci["runningTasksCount"]),
            ("Pending Tasks", ci["pendingTasksCount"]),
            ("AMI Id", ci["ami_id"]),
            ("Instance Type", ci["instance_type"]),
            ("Availability Zone", ci["availability_zone"]),
            (
                "Memory",
                "Available: "
                + str(ci["available_memory"])
                + " Total: "
                + str(ci["total_memory"]),
            ),
            (
                "CPU",
                "Available: "
                + str(ci["available_cpu"])
                + " Total: "
                + str(ci["total_cpu"]),
            ),
            ("Taken ports", ci["taken_ports"]),
        ]

    def retrieve_by_highlight(self, key: str) -> UrwidData:
        """Get element children when you hit a key.

        Args:
            key (str): Pressed key character

        Returns:
            UrwidData: Tuple with a title and a list of elements
        """
        if key == "T":
            return (
                f"Tasks '{self.name}'",
                [
                    Task(self.identifier, self.cluster_identifier, t["name"], t)
                    for t in ecs_data.get_tasks_container_instance(
                        self.cluster_identifier, self.identifier
                    )
                ],
            )
        else:
            return (None, [])

    def special_action(self, key: str) -> List[Any]:
        """Execute an special action pressing a key.

        Args:
            key (str): Key pressed character

        Returns:
            List[Any]: Tuple with name command and command
        """
        if key == "I":
            return ("SSH", ecs_ssh.ssh_cmd_container_instance(self.detail))
        else:
            return (None, [])


class Service(EcsButton):
    """Specific button for ECS Services elements."""

    def __init__(
        self,
        identifier: str,
        name: str,
        cluster_identifier: str,
        detail: UrwidData,
    ) -> None:
        """Create a new Service Element.

        Args:
            identifier (str): Unique identification for element, it could be aws arn
            name (str): Name for visual identification of element
            cluster_identifier (str): Cluster unique identification
            detail (UrwidData): JSON information from ECS
        """
        super(Service, self).__init__(identifier, name, detail)
        self.cluster_identifier = cluster_identifier

    def retrieve_children(self) -> UrwidData:
        """Request children for this element of this element.

        Returns:
            UrwidData: Tuple where first element is a name, and the second is a list
        """
        return (
            f"Tasks '{self.name}'",
            [
                Task(self.identifier, self.cluster_identifier, t["name"], t)
                for t in ecs_data.get_tasks_service(
                    self.cluster_identifier, self.identifier
                )
            ],
        )

    def retrieve_important_details(self) -> List[Any]:
        """Get a list of details as attributes as name / values.

        Returns:
            List[Any]: List of typles with name and value
        """
        deployment_config = self.detail["deploymentConfiguration"]
        min_bracket = deployment_config["minimumHealthyPercent"]
        max_bracket = deployment_config["maximumPercent"]

        return [
            ("Status", self.detail["status"]),
            ("Task Definition", self.detail["taskDefinition"]),
            ("Running", self.detail["runningCount"]),
            ("Pending", self.detail["pendingCount"]),
            ("Desired", self.detail["desiredCount"]),
            (
                "Redeployment bracket",
                "Min: " + str(min_bracket) + "%, Max: " + str(max_bracket) + "%",
            ),
        ]


class Task(EcsButton):
    """Specific button for ECS Task elements."""

    def __init__(
        self,
        service_identifier: str,
        cluster_identifier: str,
        identifier: str,
        detail: UrwidData,
    ) -> None:
        """Create a new Task Element.

        Args:
            service_identifier (str): Service unique identification
            cluster_identifier (str): Cluster unique identification
            identifier (str): Unique identification for element, it could be aws arn
            detail (UrwidData): JSON information from ECS
        """
        super(Task, self).__init__(identifier, identifier, detail)
        self.service_identifier = service_identifier
        self.cluster_identifier = cluster_identifier

    def retrieve_children(self) -> UrwidData:
        """Request children for this element of this element.

        Returns:
            UrwidData: Tuple where first element is a name, and the second is a list
        """
        return (
            f"Docker Containers '{self.name}'",
            [
                DockerContainer(self.identifier, self.cluster_identifier, t["name"], t)
                for t in ecs_data.get_containers_tasks(
                    self.cluster_identifier, self.detail["taskArn"]
                )
            ],
        )

    def retrieve_important_details(self) -> List[Any]:
        """Get a list of details as attributes as name / values.

        Returns:
            List[Any]: List of typles with name and value
        """
        return [
            ("Status", self.detail["lastStatus"]),
            ("Desired Status", self.detail["desiredStatus"]),
            ("EC2 Instance", self.detail["ec2InstanceId"]),
            ("Task Definition", self.detail["taskDefinitionArn"]),
            (
                ["Container ", ("key", "I"), "nstance ID"],
                self.detail["containerInstanceArn"].split("/", 1)[1],
            ),
            ("N. Docker images", len(self.detail["containers"])),
            ("Networks", "\n".join(self.detail["networks"])),
        ]

    def special_action(self, key: str) -> UrwidData:
        """Execute an special action pressing a key.

        Args:
            key (str): Key pressed character

        Returns:
            UrwidData: Tuple with name command and command
        """
        if key == "I":
            return ("SSH", ecs_ssh.ssh_cmd_container_instance(self.detail))
        if key == "C":
            return ("SSH", ecs_ssh.ssh_cmd_task_exec(self.detail, "/bin/sh"))
        if key == "L":
            return ("SSH", ecs_ssh.ssh_cmd_task_log(self.detail))
        else:
            return (None, [])


class DockerContainer(EcsButton):
    """Specific button for Docker container elements."""

    def __init__(
        self,
        task_identifier: str,
        cluster_identifier: str,
        identifier: str,
        detail: UrwidData,
    ) -> None:
        """Create a new Docker Container Element.

        Args:
            task_identifier (str): Task unique identification
            cluster_identifier (str): Cluster unique identification
            identifier (str): Unique identification for element, it could be aws arn
            detail (UrwidData): JSON information from ECS
        """
        super(DockerContainer, self).__init__(identifier, identifier, detail)
        self.task_identifier = task_identifier
        self.cluster_identifier = cluster_identifier

    def retrieve_important_details(self) -> List[Any]:
        """Get a list of details as attributes as name / values.

        Returns:
            List[Any]: List of typles with name and value
        """
        return [
            ("Container Arn", self.detail["containerArn"]),
            ("Status", self.detail["lastStatus"]),
            ("Health Status", self.detail["healthStatus"]),
            ("Docker id", self.detail["runtimeId"]),
            ("Docker Image", self.detail["image"]),
            ("CPU", self.detail["cpu"]),
            # ('Memory Reservation', self.detail['memoryReservation']),
            ("Instance ID", self.detail["ec2InstanceId"]),
            ("Networks", self.detail["networks"]),
        ]

    def special_action(self, key: str) -> UrwidData:
        """Execute an special action pressing a key.

        Args:
            key (str): Key pressed character

        Returns:
            UrwidData: Tuple with name command and command
        """
        if key == "I":
            return ("SSH", ecs_ssh.ssh_cmd_container_instance(self.detail))
        if key == "C":
            return (
                "SSH",
                ecs_ssh.ssh_cmd_docker_container_exec(self.detail, "/bin/sh"),
            )
        if key == "L":
            return ("SSH", ecs_ssh.ssh_cmd_docker_container_log(self.detail))
        else:
            return (None, [])
