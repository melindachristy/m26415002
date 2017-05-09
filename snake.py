#!/usr/bin/python
import sys, time
import thread
from random import randrange

from PyQt4 import QtGui, QtCore

class Snake(QtGui.QWidget):
	def __init__(self):
		super(Snake, self).__init__()
		self.initUI()

	def initUI(self):
		self.newGame()
		self.setStyleSheet("QWidget { background: #b7d2ff }")
		self.setFixedSize(500, 500)
		self.setWindowTitle('Snake')
		self.show()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.placeFood(qp)
		self.drawSnake(qp)
qp.end()


	def newGame(self):
		self.score = 0
		self.x = 12;
		self.y = 36;
		self.snakeArray = [[self.x, self.y], [self.x-12, self.y], [self.x-24, self.y]]
		self.foodx = 0
		self.foody = 0
		self.FoodPlaced = False
		self.speed = 100
		self.start()


	def start(self):
		self.update()

	def direction(self, dir):


	def gameOver(self, event, qp):


	def checkStatus(self, x, y):
		if y > 288 or x > 288 or x < 0 or y < 24:
			self.pause()
			self.isPaused = True
			self.isOver = True
			return False
		elif self.snakeArray[0] in self.snakeArray[1:len(self.snakeArray)]:
			self.pause()
			self.isPaused = True
			self.isOver = True
			return False
		elif self.y == self.foody and self.x == self.foodx:
			self.FoodPlaced = False
			self.score += 1
			return True
		elif self.score >= 573:
			print "you win!"

		self.snakeArray.pop()

		return True

	def placeFood(self, qp):
		if self.FoodPlaced == False:
			self.foodx = randrange(24)*12
			self.foody = randrange(2, 24)*12
			if not [self.foodx, self.foody] in self.snakeArray:
				self.FoodPlaced = True;
		qp.setBrush(QtGui.QColor(80, 180, 0, 160))
		qp.drawRect(self.foodx, self.foody, 12, 12)

	def drawSnake(self, qp):
		qp.setPen(QtCore.Qt.NoPen)
		qp.setBrush(QtGui.QColor(255, 80, 0, 255))
		for i in self.snakeArray:
			qp.drawRect(i[0], i[1], 12, 12)


def main():
	app = QtGui.QApplication(sys.argv)
	ex = Snake()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()