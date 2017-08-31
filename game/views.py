from django.shortcuts import render
from django.http import  HttpResponse, JsonResponse
from game.board import Board, WordDictionary
import json
from django.views.decorators.csrf import csrf_exempt
from game.game_utils import compute_score

def index(request):
	board = Board()
	dictionary = WordDictionary("game/dictionary.txt")
	solved = list(board.solve(dictionary))

	return render(request, 'game/single_player_game.html', { 'board': board.board, 'solved': json.dumps(solved), 'json_board': json.dumps(board.board) })

@csrf_exempt
def game_over(request):
	solvedWords = request.POST.getlist("words[]")
	
	# populate board one dimension at a time since django doesn't support multi-dim lists in request body
	board = []
	board.append(request.POST.getlist("row0[]"))
	board.append(request.POST.getlist("row1[]"))
	board.append(request.POST.getlist("row2[]"))
	board.append(request.POST.getlist("row3[]"))

	score = compute_score(solvedWords)
	

	return JsonResponse("look charlie, candy mountain", safe=False)


