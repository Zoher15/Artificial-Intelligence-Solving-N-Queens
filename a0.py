#!/usr/bin/env python
# a0.py : Solve the N-Rooks and NEW N-Queens problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Edited to specifications for Assignment 0 by Zoher Kachwala, with BFS(fifth command line argument as 1)/DFS(by default) Switch by Zoher Kachwala September 2017

import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# NEW Count # of pieces in given diagonal
def count_on_dia(board, dia):
	return sum (board[dia])

# NEW To convert the board to a list of left-to-right diagonal lists
def lrdiagonal(board):
	dia=[[] for i in range(2*N-1)]
	for i in range (0,N):
		for j in range (0,N):
			dia[j-i+N-1].append(board[i][j])
	return dia

# NEW To convert the board to a list of right-to-left diagonal lists
def rldiagonal(board):
	dia=[[] for i in range(2*N-1)]
	for i in range (0,N):
		for j in range (0,N):
			dia[i+j].append(board[i][j])
	return dia

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
# Modified using Professor's Crandall's expanded function in the assignment vidoes
# To print X for the unavailable coordinates
def printable_board(board):
    str=""
    for r in range(0,N):
    		for c in range(0,N):
    			if nanx-1==r and nany-1==c:
    				str+="X "
    			elif board[r][c]==1:
    				if RorQ=="nqueen":
    					str+="Q "
    				elif RorQ=="nrook":
    					str+="R "
    			else:
    				str+="_ "
    		str+="\n"
    return str

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# NEW Get list of successors of given board state for n-queens
# Same as the original function with a modification on the range of succession using vacantrows and vacantcolumns
# NEW if condition to test whether a given the lrdiagonal(left to right) and rldiagonal (right to left) for a coordinate [r,c] is vacant
# NEW if condition to avoid successor to unavailable coordinates "X"
def successors2q(board):
	return[add_piece(board, r, c) for r in vacantrows(board) for c in vacantcolumns(board) if (r!=nanx-1 or c!=nany-1) and count_on_dia(lrdiagonal(board),c-r+N-1)==0 and count_on_dia(rldiagonal(board),c+r)==0]

# Get list of successors of given board state for n-rooks
# Same as the original function with a modification on the range of succession using vacantrows and vacantcolumns
# NEW if condition to avoid successor to unavailable coordinates "X"
def successors2r(board):
	return [ add_piece(board, r, c) for r in vacantrows(board) for c in vacantcolumns(board) if (r!=nanx-1 or c!=nany-1)]

# NEW check if board is a goal state with additional conditions for n-queens problem
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] ) and \
        all( [ count_on_dia(lrdiagonal(board), d) <= 1 for d in range(0, 2*N-1) if RorQ=="nqueen"] ) and \
        all( [ count_on_dia(rldiagonal(board), d) <= 1 for d in range(0, 2*N-1) if RorQ=="nqueen"] )

# to avoid the rows already occupied
def vacantrows(board):
	rows=[]
	for r in range(0,N):
		if count_on_row(board,r)==0:
			rows.append(r)
	return rows

# to avoid the columns already occupied
def vacantcolumns(board):
	cols=[]
	for c in range(0,N):
		if count_on_col(board,c)==0:
			cols.append(c)
	return cols

# NEW Solve n-queens or n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    if RorQ=="nqueen":
	    while len(fringe) > 0:#BFS is only chosen if a 5th command line argument is passed as 1 in BFSorNot
	    	for s in successors2q(fringe.pop(0) if BFSorNot is 1 else fringe.pop()):#Popping at the 0th position to make it BFS
	    		if is_goal(s):
	    			return(s)
	    		fringe.append(s)
	    return False

    elif RorQ=="nrook":
	    while len(fringe) > 0:#BFS is only chosen if a 5th command line argument is passed as 1 in BFSorNot
	    	for s in successors2r(fringe.pop(0) if BFSorNot is 1 else fringe.pop()):#Popping at the 0th position to make it BFS
	    		if is_goal(s):
	    			return(s)  
	           	fringe.append(s)
	    return False

# This is N, the size of the board. It is passed through command line arguments.
RorQ=sys.argv[1]
N = int(sys.argv[2])
nanx=int(sys.argv[3])
nany=int(sys.argv[4])
# To enable a switch between DFS and BFS, I have given an option to enter a 5th commandline argument.
# By default BFSorNot will take up the value None and executed DFS. Only if 1 is passed to BFSorDFS, BFS will execute 
try:
	BFSorNot=int(sys.argv[5])
except IndexError:
	BFSorNot=None
# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N


print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
solution = solve(initial_board)
print (printable_board(solution) if solution else "Sorry, no solution found. :(")