import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
    width: 520
    height: 360
    visible: true
    title: "Create Room"

    // Theme
    Material.theme: Material.Dark
    Material.accent: Material.Orange

    ColumnLayout {
        anchors.centerIn: parent

        GridLayout {
            columns: 2
            Layout.alignment: Qt.AlignCenter
            Layout.margins: 10
            columnSpacing: 100
            rowSpacing: 10

            Label {
                text: "Max Players"
            }
            SpinBox {
                id: maxPlayers
                from: 2
                value: 8
                to: 16
                Layout.alignment: Qt.AlignRight
            }

            Label {
                text: "Time Limit"
            }
            SpinBox {
                id: timeLimit
                from: 15
                value: 80
                to: 240
                Layout.alignment: Qt.AlignRight
            }

            Label {
                text: "Rounds"
            }
            SpinBox {
                id: rounds
                from: 1
                value: 3
                to: 80
                Layout.alignment: Qt.AlignRight
            }
        }

        Button {
            text: "Start!"
            Layout.alignment: Qt.AlignCenter
        }
    }
}
