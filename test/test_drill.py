import json

from fastapi.testclient import TestClient

from dependencies import Move, BoardState
from main import app

client = TestClient(app)

e4 = BoardState(
    move_history=[Move(fen='rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', san='e4', uci='e2e4')],
    selected_pgns=['test'])

Nc3 = BoardState(
    # 1. e4 e5 2.Nc3
    move_history=[Move(fen='rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', san='e4', uci='e2e4'),
                  Move(fen='rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', san='e5', uci='e7e5'),
                  Move(fen='rnbqkbnr/pppp1ppp/8/4p3/4P3/2N5/PPPP1PPP/R1BQKBNR b KQkq - 1 2', san='Nc3', uci='b1c3')],
    selected_pgns=['test'])


def test_cpu_single_move_request():
    response = client.post("/cpu/move", json=json.loads(e4.json()))
    assert response.status_code == 200
    assert response.json()['course'] == 'test'
    assert response.json()['FEN'] == 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2'
    assert len(response.json()['move_history']) == 2
    assert [move['san'] for move in response.json()['move_history']] == ['e4', 'e5']


def test_cpu_two_move_request():
    response = client.post("/cpu/move", json=json.loads(e4.json()))
    assert response.status_code == 200
    assert response.json()['course'] == 'test'
    assert response.json()['FEN'] == 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2'
    assert len(response.json()['move_history']) == 2
    assert [move['san'] for move in response.json()['move_history']] == ['e4', 'e5']

    response = client.post("/cpu/move", json=json.loads(Nc3.json()))
    assert response.status_code == 200
    assert response.json()['FEN'] == 'rnbqkb1r/pppp1ppp/5n2/4p3/4P3/2N5/PPPP1PPP/R1BQKBNR w KQkq - 2 3'
    assert len(response.json()['move_history']) == 4
    assert [move['san'] for move in response.json()['move_history']] == ['e4', 'e5', 'Nc3', 'Nf6']
