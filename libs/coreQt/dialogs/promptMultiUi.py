import os
from PyQt4 import QtGui
from coreSys import env
from coreQt import dialogs, pQt

# dialogs.compileUi(['dial_prompt.ui', 'wg_promptLine.ui', 'wg_promptColor.ui', 'wg_promptCombo.ui'])
from _ui import dial_promptUI, wg_promptLineUI, wg_promptColorUI, wg_promptComboUI


class PromptMulti(QtGui.QDialog, dial_promptUI.Ui_dial_prompt):
    """
    Prompt dialog ui class

    :param title: Dialog title
    :type title: str
    :param prompts: Prompts dict list
                    [dict(promptType='line', promptLabel='name', promptValue='test'),
                     dict(promptType='color', promptLabel='style', promptValue=(175, 80, 120)),
                     dict(promptType='combo', promptLabel='lists', promptValue=['item1', 'item2', 'item3'])]
    :type prompts: list
    :param acceptCmd: Command to launch when 'Save' QPushButton is clicked
    :type acceptCmd: method || function
    :param parent: Parent ui or widget
    :type parent: QtGui.QWidget
    """

    __iconPath__ = env.iconsPath

    def __init__(self, title='Prompt Dialog', prompts=[], acceptCmd=None, parent=None):
        super(PromptMulti, self).__init__(parent)
        self._parent = parent
        self.title = title
        self.prompts = prompts
        self.accetpCmd = acceptCmd
        #--- Setup ---#
        self.setupUi(self)
        self._initDialog()

    def _initDialog(self):
        """
        Init dialog window
        """
        self.l_title.setText(self.title)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.setMinimumHeight(60 + (25 * len(self.prompts)))
        if self.minimumHeight() > 400:
            self.setMinimumHeight(400)
        #--- Icons ---#
        self.pb_save.setIcon(QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'apply.png')))
        self.pb_cancel.setIcon(QtGui.QIcon(os.path.join(self.__iconPath__, 'png', 'cancel.png')))
        #--- Connect ---#
        if self.accetpCmd is not None:
            self.pb_save.clicked.connect(self.accetpCmd)
        self.pb_cancel.clicked.connect(self.close)
        self.buildPrompts()

    def buildPrompts(self):
        """
        Build prompt widgets
        """
        self.tw_prompts.clear()
        for data in self.prompts:
            newItem = self.new_promptItem(**data)
            self.tw_prompts.addTopLevelItem(newItem)
            self.tw_prompts.setItemWidget(newItem, 0, newItem.itemWidget)

    @staticmethod
    def new_promptItem(**kwargs):
        """
        Create new prompt item

        :param kwargs: Prompt data (ex: dict(promptType='line', promptLabel='name', promptValue='test'))
        :type kwargs: dict
        :return: New prompt item
        :rtype: QtGui.QTreeWidgetItem
        """
        newItem = QtGui.QTreeWidgetItem()
        newItem.itemType = kwargs.get('promptType')
        newItem.itemLabel = kwargs.get('promptLabel')
        #--- Create Prompt Line ---#
        if newItem.itemType == 'line':
            newItem.itemWidget = PromptLine(label=newItem.itemLabel, value=kwargs.get('promptValue'))
            if kwargs.get('enable') is not None:
                newItem.itemWidget.le_prompt.setEnabled(kwargs.get('enable'))
            if kwargs.get('readOnly') is not None:
                newItem.itemWidget.le_prompt.setReadOnly(kwargs.get('readOnly'))
        #--- Create Prompt Color ---#
        elif newItem.itemType == 'color':
            newItem.itemWidget = PromptColor(label=newItem.itemLabel, value=kwargs.get('promptValue'))
        #--- create Prompt Combo ---#
        elif newItem.itemType == 'combo':
            newItem.itemWidget = PromptCombo(label=newItem.itemLabel, value=kwargs.get('promptValue'))
            defaultValue = kwargs.get('defaultValue')
            if defaultValue is not None:
                newItem.itemWidget.cb_prompt.setCurrentIndex(newItem.itemWidget.cb_prompt.findText(str(defaultValue)))
        #--- Result ---#
        return newItem

    def result(self):
        """
        Get dialog result

        :return: Dialog result
        :rtype: dict
        """
        data = dict()
        for item in pQt.getAllItems(self.tw_prompts):
            data[item.itemLabel] = item.itemWidget.result()
        return data


class PromptLine(QtGui.QWidget, wg_promptLineUI.Ui_wg_promptLine):
    """
    PromptLine class: Prompt dialog item widget

    :param label: Prompt label
    :type label: str
    :param value: Prompt value
    :type value: str
    """

    def __init__(self, label='Untitled', value=None):
        self.label = label
        self.value = value
        super(PromptLine, self).__init__()
        self.setupUi(self)
        self._initWidget()

    def _initWidget(self):
        """
        Init widget ui
        """
        self.l_prompt.setText(self.label)
        if self.value is not None:
            self.le_prompt.setText(self.value)

    def result(self):
        """
        Get prompt line result

        :return: Prompt line result
        :rtype: str
        """
        return str(self.le_prompt.text())


class PromptColor(QtGui.QWidget, wg_promptColorUI.Ui_wg_promptColor):
    """
    PromptColor class: Prompt dialog item widget

    :param label: Prompt label
    :type label: str
    :param value: Prompt value
    :type value: tuple
    """

    def __init__(self, label='Untitled', value=None):
        self.label = label
        self.value = value
        super(PromptColor, self).__init__()
        self.setupUi(self)
        self._initWidget()

    def _initWidget(self):
        """
        Init widget ui
        """
        self.l_prompt.setText(self.label)
        #--- Init Values ---#
        if self.value is not None:
            self.sb_colorRed.setValue(self.value[0])
            self.sb_colorGreen.setValue(self.value[1])
            self.sb_colorBlue.setValue(self.value[2])
            self.pb_color.setStyleSheet("background-color: rgb(%s, %s, %s)" % (self.value[0],
                                                                               self.value[1],
                                                                               self.value[2]))
        #--- Connect ---#
        self.sb_colorRed.editingFinished.connect(self.on_rgb)
        self.sb_colorGreen.editingFinished.connect(self.on_rgb)
        self.sb_colorBlue.editingFinished.connect(self.on_rgb)
        self.pb_color.clicked.connect(self.on_color)

    def on_rgb(self):
        """
        Command launched when 'RGB' QSpinBoxes are edited

        Edit and refresh color
        """
        self.pb_color.setStyleSheet("background-color: rgb(%s, %s, %s)" % (self.result()[0],
                                                                           self.result()[1],
                                                                           self.result()[2]))

    def on_color(self):
        """
        Command launched when 'Color' QPushButton is clicked

        Launch color dialog
        """
        # noinspection PyArgumentList
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            rgba = color.getRgb()
            self.sb_colorRed.setValue(rgba[0])
            self.sb_colorGreen.setValue(rgba[1])
            self.sb_colorBlue.setValue(rgba[2])
            self.on_rgb()

    def result(self):
        """
        Get prompt color result

        :return: Prompt color result
        :rtype: str
        """
        color = (self.sb_colorRed.value(), self.sb_colorGreen.value(), self.sb_colorBlue.value())
        return color


class PromptCombo(QtGui.QWidget, wg_promptComboUI.Ui_wg_promptCombo):
    """
    PromptCombo class: Prompt dialog item widget

    :param label: Prompt label
    :type label: str
    :param value: Prompt value
    :type value: list
    """

    def __init__(self, label='Untitled', value=None):
        self.label = label
        self.value = value
        super(PromptCombo, self).__init__()
        self.setupUi(self)
        self._initWidget()

    def _initWidget(self):
        """
        Init widget ui
        """
        self.l_prompt.setText(self.label)
        if self.value is not None:
            self.cb_prompt.addItems(self.value)

    def result(self):
        """
        Get prompt combo result

        :return: Prompt combo result
        :rtype: str
        """
        return str(self.cb_prompt.currentText())



if __name__ == '__main__':
    import sys

    color = (175, 80, 120)
    combo = ['item1', 'item2', 'item3']
    prompts = [dict(promptType='line', promptLabel='name', promptValue='test', enable=True, readOnly=False),
               dict(promptType='color', promptLabel='style', promptValue=color),
               dict(promptType='combo', promptLabel='lists', promptValue=combo)]

    app = QtGui.QApplication(sys.argv)
    window = PromptMulti(prompts=prompts)
    window.show()
    sys.exit(app.exec_())