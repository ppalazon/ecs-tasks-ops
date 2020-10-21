"""Qt5 Tree Model for ecs"""

from PyQt5 import QtWidgets, QtCore
from ecs_tasks_ops import ecs_data

class ECSTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, name, identifier, detail_type, detail, parent=None):
        super(ECSTreeItem, self).__init__(parent, [name, identifier])
        self.name = name
        self.identifier = identifier
        self.detail_type = detail_type
        self.detail = detail

    def refresh_children(self):
        pass

    def get_attributes(self):
        return []


class ECSClusterTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSClusterTreeItem, self).__init__(name=detail['clusterName'], identifier=detail['clusterArn'], detail_type='cluster', detail=detail, parent=parent)

    def refresh_children(self):
        self.addChild(ECSListTasksClusterTreeItem(self.detail, self))
        self.addChild(ECSListServicesClusterTreeItem(self.detail, self))
        self.addChild(ECSListContainersClusterTreeItem(self.detail, self))

    def get_attributes(self):
        return [("Name", self.detail['clusterName']),
                ("Arn", self.detail['clusterArn']),
                ("Status", self.detail['status']),
                ("Active Services", self.detail['activeServicesCount']),
                ("Running Tasks", self.detail['runningTasksCount']),
                ("Pending Tasks", self.detail['pendingTasksCount']),
                ("Containers", self.detail['registeredContainerInstancesCount'])]
            

class ECSListServicesClusterTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSListServicesClusterTreeItem, self).__init__(name="Services", identifier='Services for '+detail['clusterName'], detail_type='list_services', detail=detail, parent=parent)

    def refresh_children(self):
        pass


class ECSListTasksClusterTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSListTasksClusterTreeItem, self).__init__(name="Tasks", identifier='Tasks for '+detail['clusterName'], detail_type='list_services', detail=detail, parent=parent)

    def refresh_children(self):
        pass


class ECSListContainersClusterTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSListContainersClusterTreeItem, self).__init__(name="Containers", identifier='Containers for '+detail['clusterName'], detail_type='list_services', detail=detail, parent=parent)

    def refresh_children(self):
        pass