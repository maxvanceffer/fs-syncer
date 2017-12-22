import QtQuick 2.4
import QtQuick.Controls 1.2
import QtQuick.Window 2.2
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.2

Item {
    id: wizard
    width: 400
    height: 400

    signal done()

    function switchPage(name) {
        switch(name) {
            case 'ssh':
                stack.push(sshChannel)
                break;
            default:
                break;
        }
    }

    StackView {
        id: stack
        initialItem: page === 'initial' ? view : sshChannel
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.bottom: controlLayout.top

        Component {
            id: sshChannel
            Ssh {}
        }

        Component {
            id: view

            Item {
                width: stack.width
                height: stack.height

                ListView {
                    id: chooseChannelListView
                    anchors.fill: parent
                    anchors.margins: 6

                    model: ListModel {
                        ListElement {name: 'SSH sync'; page: 'ssh'}
                        ListElement {name: 'Web sync'; page: 'ssh'}
                    }

                    delegate: Item {
                        height: 50
                        width: chooseChannelListView.width

                        Label {
                            text: name
                            font.bold: true
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {

                                switchPage(page)
                            }
                        }
                    }
                }
            }
        }
    }

    RowLayout {
        id: controlLayout

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.margins: 6

        Button {
            text: "Chancel"
            onClicked: {
                channelDialog.close()
                wizard.done()
            }
        }

        Button {
            text: "Create"
            onClicked: {
                stack.currentItem.create()
                addChannelDialog.close()
                wizard.done()
            }
        }

        Button {
            text: qsTr("Save")
            onClicked: {
                stack.currentItem.save()
                channelDialog.close()
                wizard.done()
            }
        }
    }
}