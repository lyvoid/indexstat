# -*-coding:utf-8-*-

from dao.mongotool import *


class SZIndexStat(Table):
    __table__ = 'szindex'
    date = AssistColumnClass(str)
    today_index_value = AssistColumnClass(float)
    avg_30_index = AssistColumnClass(float)
    avg_90_index = AssistColumnClass(float)
    avg_180_index = AssistColumnClass(float)
