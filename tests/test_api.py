from fastapi import status


def test_missed_pool_id(app, test_client, mock_pool_service, mocker):
    response = test_client.get("/")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["header", "X-Pool-ID"],
                "msg": "Field required",
                "input": None,
                "url": mocker.ANY,
            }
        ]
    }


def test_unknown_pool_id(app, test_client, mock_pool_service):
    _POOL_ID = "unknown-pool-id"

    mock_pool_service.get_redirect_domain.return_value = None

    response = test_client.get("/", headers={"X-Pool-ID": _POOL_ID})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Unknown pool-id"}

    mock_pool_service.get_redirect_domain.assert_awaited_once_with(_POOL_ID)


def test_successful_redirect(app, test_client, mock_pool_service):
    _POOL_ID = "known-pool-id"

    mock_pool_service.get_redirect_domain.return_value = ("example.com", 1)

    response = test_client.get("/path?a=1&b=2", headers={"X-Pool-ID": _POOL_ID}, follow_redirects=False)

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["Location"] == "http://example.com/path?a=1&b=2"
