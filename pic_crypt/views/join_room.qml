import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
    width: 400
    height: 320
    visible: true
    title: "Join Room"

    // Theme
    Material.theme: Material.Dark
    Material.accent: Material.Orange

    ColumnLayout {
        anchors.fill: parent
        anchors.centerIn: parent
        spacing: 20
        anchors.margins: 24

        Item {
            Layout.fillHeight: true
        }
        TextField {
            id: roomID
            placeholderText: "Room ID"
            Layout.fillWidth: true
            Layout.maximumWidth: 320
            Layout.alignment: Qt.AlignCenter
        }
        Button {
            text: "Join!"
            Layout.alignment: Qt.AlignCenter
        }
        Item {
            Layout.fillHeight: true
        }
    }
}
