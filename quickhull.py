"""
Import all libraries needed
"""
import numpy as np
from math import atan2 # math.atan2() method returns the arc tangent of  coordinates y/x, in radians.
from math import hypot # finds the hypotenuse of a triangle.
import matplotlib.pyplot as plt

"""
Find the centre point of the set of points S.
"""
def findCentre(S):
	x = 0 # Set x as 0.
	y = 0 # Set y as 0.
	for point in S: # Iterate through all points in S.
		x += point[0] # Set x as x coord.
		y += point[1] # Set y as y coord.
	k = len(S) # Find length of point set S.
	centre = [x/k, y/k] # Centre of the set will be at the average x and y coords.
	return centre

"""
Find which side of line AB, C is located on.
"""
def sideCheck(A, B, C):
	return (C[0]-A[0])*(B[1]-A[1]) - (C[1]-A[1])*(B[0]-A[0])

"""
For line AB find perpendicular distance from AB to point C.
"""
def distancePointToLine(A, B, C, ABCdist):
	x = abs(sideCheck(A, B, C))
	return x/ABCdist

"""
Calculate the distance between point A and point B by calculating the hypotenuse.
"""
def distancePointToPoint(A,B):
	return hypot((B[1]-A[1]), (B[0]-A[0]))

"""
Recursively finds each hull vertex.
"""
def quickhull(S):
	S.sort(key = lambda x : (x[0], x[1])) # Sort set of points S by value of the x coord.

	leftmost = S[0] # Leftmost point will be point with lowest x value.
	rightmost = S[-1] # Rightmost point will be point with lowest x value.

	aboveLinePoint = [leftmost[0], leftmost[1]+1] # A point above the line with leftmost x coord leftmost y+1 y coord.
	aboveLine = sideCheck(leftmost, rightmost, aboveLinePoint) # Check the point is above the bisecting line.

	# Set of points located in the top side and bottom side of line L respectively
	aboveS = [] # List of points above the bisecting line.
	belowS = [] # List of points below the bisecting line.

	# Split set of points S into above or below bisecting line.
	for point in S: # Iterate through each point in S.
		if point != leftmost and point != rightmost: # If the point is not the left or right most point continue. If a
													 # point is one of these it will be part of the line instead.
			j = sideCheck(leftmost, rightmost, point) # Check which side the current point is on.
			if j != 0 and np.sign(aboveLine) == np.sign(j): # If the point is above the bisecting line.
				aboveS.append(point) # Add point to list of points above the bisecting line.
			else: # Point is not above bisecting line and is not a part of the line.
				belowS.append(point) # Add point to list of points above the bisecting line.

	# Initialize call to find Hull in the top and bottom section respectively
	aboveHull = FindHull(aboveS, leftmost, rightmost)
	belowHull = FindHull(belowS, rightmost, leftmost)

	# Merge final answer
	return [leftmost] + aboveHull + belowHull + [rightmost]

"""
Find the point farthest from the line between the leftmost and rightmost points (A and B) recursively.
"""
def FindHull(P, leftmost, rightmost):
	if not P: # If there are no points
		return [] # Return an empty list
	else: # If there are points
		currentMaxDist = -1 # Set the current max to -1 as this can never be the case in practice whereas 0 could be.
		distanceAtoB = distancePointToPoint(leftmost, rightmost) # Find the distance between left and right most points.

		for point in P: # Iterate through all points.
			pointDistance = distancePointToLine(leftmost, rightmost, point, distanceAtoB) # Find the distance to point.
			currentMaxDist = max(currentMaxDist, pointDistance) # If this distance > the previous max distance, update.
			if currentMaxDist == pointDistance: # If this point is the farthest.
				currentPoint = point # Store the current top point as point.

		listOfVertices = [currentPoint] # Initialise a list of vertices.
		for point in P: # Iterate through all points.
			pointDistance = distancePointToLine(leftmost, rightmost, point, distanceAtoB) # Find the distance to point.
			if currentMaxDist == pointDistance: # If this point is the farthest.
				listOfVertices.append(point) # Add current point to list of vertices.

		abovePoint = [] # List of top points.
		belowPoint = [] # List of bottom points.

		sideRightmost = sideCheck(leftmost, currentPoint, rightmost) # Check side of points
		sideLeftmost = sideCheck(currentPoint, rightmost, leftmost)

		for point in P: # Iterate through all points.
			if point not in listOfVertices: # If the point is not already in the vertices list.
				l = sideCheck(leftmost, currentPoint, point) # Check if above line from the leftmost to farthest points.
				r = sideCheck(currentPoint, rightmost, point) # Check if above line from the right to farthest points.
				if np.sign(l) != np.sign(sideRightmost):
					abovePoint.append(point)
				if np.sign(r) != np.sign(sideLeftmost):
					belowPoint.append(point)

		aboveHull = FindHull(abovePoint, leftmost, currentPoint) # Recursively find vertices above current hull.
		belowHull = FindHull(belowPoint, currentPoint, rightmost) # Recursively find vertices above current hull.
		return listOfVertices + aboveHull + belowHull # Return the list of all hull points.

"""
########################################################################################################################
Main program
########################################################################################################################
"""
if __name__ == "__main__":
	numPoints = int(input("Number of points: ")) # Get the user input for number of points as an int.
	xCoord = [x for x in [np.random.randint(0, 100) for _ in range(numPoints)]] # Randomly generate numPoints x coords.
	yCoord = [x for x in [np.random.randint(0, 100) for _ in range(numPoints)]] # Randomly generate numPoints y coords.
	coords = [[item[0], item[1]] for item in zip(xCoord, yCoord)] # Zip the x and y coords into lists of full coords.

	plt.plot(xCoord, yCoord, "bo") # Plot all starting points
	plt.show() # Show the plot.

	vertices = [] # List of all hull points
	vertices = quickhull(coords) # Use quicksort function to find hull vertices.

	centre = findCentre(vertices) # Find the centre of the hull vertices.
	vertices.sort(key = lambda x : (atan2(x[1]-centre[1], x[0]-centre[0]))) # Sort the vertices by their angle to the
																			  # centre point so line plots correctly.

	verticesX, verticesY = [x for x in zip(*vertices)] # Unzip vertices into x and y coords for plotting.
	verticesX = list(verticesX) # Convert to list form.
	verticesY = list(verticesY) # Convert to list form.

	verticesX.append(vertices[0][0]) # Connect the first to last point so that the line forms a full convex hull.
	verticesY.append(vertices[0][1])

	numVertices = len(vertices) # Find how many vertices there are.
	print("\n Sequence of vertices:")
	for i in range(numVertices): # Go through all vertices and print it.
		l = vertices[i]
		r = vertices[(i+1)%numVertices]
		if l != r:
			print("Vertex {:>10} to vertex {:}".format(str(l), str(r)))

	plt.plot(xCoord, yCoord, "ro") 	# Plot all starting points.
	plt.plot(list(verticesX), list(verticesY), "go-") # Plot hull vertices with connecting lines between.
	plt.show() # Show the plot.
