"""Qt5 Tree Model for ecs"""

from PyQt5 import QtWidgets, QtCore
from ecs_tasks_ops import ecs_data
from ecs_tasks_ops import pretty_json

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
        return [("Name", self.name),
                ("Identifier", self.identifier),
                ("Detail Type", self.detail_type)]

    def clear_children(self):
        for i in reversed(range(self.childCount())):
            self.removeChild(self.child(i))

    def get_context_menu(self, menu):
        menu.addAction("Show Detail", self.command_show_detail)

    def command_show_detail(self):
        self.treeWidget().command_show_detail(self)


class ECSClusterTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSClusterTreeItem, self).__init__(name=detail['clusterName'], identifier=detail['clusterArn'], detail_type='cluster', detail=detail, parent=parent)

    def refresh_children(self):
        self.clear_children()
        self.addChild(ECSListTasksClusterTreeItem(self.detail, self))
        self.addChild(ECSListServicesClusterTreeItem(self.detail, self))
        self.addChild(ECSListContainersClusterTreeItem(self.detail, self))

    def get_attributes(self):
        return [("Name", self.name),
                ("Identifier", self.identifier),
                ("Detail Type", self.detail_type),
                ("Status", self.detail['status']),
                ("Active Services", self.detail['activeServicesCount']),
                ("Running Tasks", self.detail['runningTasksCount']),
                ("Pending Tasks", self.detail['pendingTasksCount']),
                ("Containers", self.detail['registeredContainerInstancesCount'])]

    def get_context_menu(self, menu):        
        menu.addAction("Info", self.show_info)          
        super(ECSClusterTreeItem, self).get_context_menu(menu)
    
    def show_info(self):
        print(f"Show info {self.name}")

class ECSListServicesClusterTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSListServicesClusterTreeItem, self).__init__(name="Services", identifier=detail['clusterName'], detail_type='list_services', detail=detail, parent=parent)

    def refresh_children(self):
        self.clear_children()
        for service in ecs_data.get_services(self.identifier):
            self.addChild(ECSServiceTreeItem(service, self))


class ECSListTasksClusterTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSListTasksClusterTreeItem, self).__init__(name="Tasks", identifier=detail['clusterName'], detail_type='list_services', detail=detail, parent=parent)

    def refresh_children(self):
        self.clear_children()
        for task in ecs_data.get_tasks_cluster(self.identifier):
            self.addChild(ECSTaskTreeItem(task, self))

class ECSListContainersClusterTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSListContainersClusterTreeItem, self).__init__(name="Containers", identifier=detail['clusterName'], detail_type='list_services', detail=detail, parent=parent)

    def refresh_children(self):
        self.clear_children()
        for container in ecs_data.get_containers_instances(self.identifier):
            self.addChild(ECSContainerTreeItem(container, self.identifier, self))


class ECSServiceTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSServiceTreeItem, self).__init__(name=detail['serviceName'], identifier=detail['serviceArn'], detail_type='service', detail=detail, parent=parent)
        self.clusterArn = detail['clusterArn']

    def refresh_children(self):
        self.clear_children()
        for task in ecs_data.get_tasks_service(self.clusterArn, self.identifier):
            self.addChild(ECSTaskTreeItem(task, self))

    def get_attributes(self):
        deployment_config = self.detail['deploymentConfiguration']
        min_bracket = deployment_config['minimumHealthyPercent']
        max_bracket = deployment_config['maximumPercent']

        return [("Name", self.name),
                ("Identifier", self.identifier),
                ("Detail Type", self.detail_type),
                ('Status', self.detail['status']),
                ('Task Definition', self.detail['taskDefinition']),
                ('Running', self.detail['runningCount']),
                ('Pending', self.detail['pendingCount']),
                ('Desired', self.detail['desiredCount']),
                ('Redeployment bracket', "Min: " + str(min_bracket) + "%, Max: " + str(max_bracket) + "%")]


class ECSTaskTreeItem(ECSTreeItem):
    def __init__(self, detail, parent=None):
        super(ECSTaskTreeItem, self).__init__(name=detail['name'], identifier=detail['taskArn'], detail_type='task', detail=detail, parent=parent)

    def refresh_children(self):
        pass

    def get_attributes(self):
        return [("Name", self.name),
                ("Identifier", self.identifier),
                ("Detail Type", self.detail_type),
                ('Status', self.detail['lastStatus']),
                ('Desired Status', self.detail['desiredStatus']),
                ('EC2 Instance', self.detail['ec2InstanceId']),
                ('Availability Zone', self.detail['availabilityZone']),
                ('Connectivity', self.detail['connectivity']),
                ('Task Definition', self.detail['taskDefinitionArn']),
                ('Container Instance ID', self.detail['containerInstanceArn'].split("/", 1)[1]),
                ('N. Docker images', len(self.detail['containers'])),
                ('Networks', '\n'.join(self.detail['networks'])),
                ('Connectivity Time', self.detail['connectivityAt'])]


class ECSContainerTreeItem(ECSTreeItem):
    def __init__(self, detail, cluster_identifier, parent=None):
        super(ECSContainerTreeItem, self).__init__(name=detail['ec2InstanceId'], identifier=detail['containerInstanceArn'], detail_type='container', detail=detail, parent=parent)
        self.cluster_identifier = cluster_identifier

    def refresh_children(self):
        self.clear_children()
        for task in ecs_data.get_tasks_container_instance(self.cluster_identifier, self.identifier):
            self.addChild(ECSTaskTreeItem(task, self))

    def get_attributes(self):
        return [("Name", self.name),
                ("Identifier", self.identifier),
                ("Detail Type", self.detail_type),
                ('Status', self.detail['status']),
                ('EC2 Instance Id', self.detail['ec2InstanceId']),
                ('Running Tasks', self.detail['runningTasksCount']),
                ('Pending Tasks', self.detail['pendingTasksCount']),
                ('AMI Id', self.detail['ami_id']),
                ('Instance Type', self.detail['instance_type']),
                ('Availability Zone', self.detail['availability_zone']),
                ('Memory', 'Available: ' + str(self.detail['available_memory']) +" Total: " + str(self.detail['total_memory'])),
                ('CPU', 'Available: ' + str(self.detail['available_cpu']) +" Total: " + str(self.detail['total_cpu'])),
                ('Taken ports', self.detail['taken_ports'])]


class ECSElementsTreeWidget(QtWidgets.QTreeWidget):

    statusChanged = QtCore.pyqtSignal(str)
    commandShowDetail = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)

    def __init__(self, parent=None):
        super(ECSElementsTreeWidget, self).__init__(parent)
        self.reload_cluster_info()
        self.currentItemChanged.connect(lambda item: self.show_status_on_selection(item))
        self.itemActivated.connect(lambda item: item.refresh_children())
        self.itemDoubleClicked.connect(lambda item: item.refresh_children())

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            menu = QtWidgets.QMenu(self)            
            item.get_context_menu(menu)
            menu.exec_(event.globalPos())
        else:
            super(ECSElementsTreeWidget, self).contextMenuEvent(event)

    def keyPressEvent(self, e):
        # if e.key() == QtCore.Qt.Key_Escape:
        #     self.close()

        super(ECSElementsTreeWidget, self).keyPressEvent(e)

    @QtCore.pyqtSlot()
    def reload_cluster_info(self):
        self.clear()
        for cluster in ecs_data.get_clusters():
            self.addTopLevelItem(ECSClusterTreeItem(cluster))

    def show_status_on_selection(self, item):
        if item:
            self.statusChanged.emit(f"Selecting {item.name}: {item.identifier}")

    
    def command_show_detail(self, item):
        if item:
            self.commandShowDetail.emit(item)

    # @QtCore.pyqtSignal(str)
    # def operation_status(self, message):
    #     self.emit

class ECSAttributesTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ECSAttributesTreeWidget, self).__init__(parent)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def update_attributes(self, item):        
        self.clear()
        if item:
            for attr in item.get_attributes():
                self.addTopLevelItem(QtWidgets.QTreeWidgetItem([str(a) for a in attr]))


class ECSTabView(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(ECSTabView, self).__init__(parent)
        self.tabCloseRequested.connect(self.info_tab_closed)

    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem)
    def open_tab_show_detail(self, item):
        if item and item.detail:
            self.addTab(ShowCode(pretty_json.get_pretty_json_str(item.detail)), item.name)

    def info_tab_closed(self, index):
        self.widget(index).close()
        self.removeTab(index)


class ShowCode(QtWidgets.QWidget):
    def __init__(self, code_str, parent=None):
        super(ShowCode, self).__init__(parent)
    
        layout = QtWidgets.QVBoxLayout()
        text = QtWidgets.QTextBrowser()
        text.setPlainText(code_str)
        layout.addWidget(text)

        self.setLayout(layout)    

class EmbTerminal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EmbTerminal, self).__init__(parent)
        self.process = QtCore.QProcess(self)
        self.terminal = QtWidgets.QWidget(self)
        self.command = QtWidgets.QLineEdit(self)
        self.command.setReadOnly(True)
        self.command.setText("ssh i-2343432fds")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.command)
        layout.addWidget(self.terminal)

        # Works also with urxvt:
        self.process.start('urxvt',['-embed', str(int(self.terminal.winId()))])
