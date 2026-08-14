import json
from unittest.mock import MagicMock, patch
import pytest
from app import app, get_redis

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_index_no_cookie(client):
    """Test GET / without a voter_id cookie."""
    response = client.get('/')
    assert response.status_code == 200
    cookie_header = response.headers.get('Set-Cookie')
    assert cookie_header is not None
    assert 'voter_id=' in cookie_header
    assert b'Cats' in response.data
    assert b'Dogs' in response.data

def test_get_index_with_cookie(client):
    """Test GET / with an existing voter_id cookie."""
    client.set_cookie('voter_id', 'test_voter_123')
    response = client.get('/')
    assert response.status_code == 200
    assert b'Cats' in response.data
    assert b'Dogs' in response.data

@patch('app.get_redis')
def test_post_vote(mock_get_redis, client):
    """Test POST / submitting a vote."""
    mock_redis = MagicMock()
    mock_get_redis.return_value = mock_redis

    client.set_cookie('voter_id', 'voter_abc')
    response = client.post('/', data={'vote': 'a'})

    assert response.status_code == 200
    mock_redis.rpush.assert_called_once()
    args, _ = mock_redis.rpush.call_args
    assert args[0] == 'votes'
    payload = json.loads(args[1])
    assert payload['voter_id'] == 'voter_abc'
    assert payload['vote'] == 'a'

def test_get_redis_helper():
    """Test get_redis helper function attaches Redis instance to Flask g."""
    with app.test_request_context():
        with patch('app.Redis') as mock_redis_cls:
            mock_instance = MagicMock()
            mock_redis_cls.return_value = mock_instance
            r1 = get_redis()
            r2 = get_redis()
            assert r1 == r2
            mock_redis_cls.assert_called_once_with(host="redis", db=0, socket_timeout=5)
