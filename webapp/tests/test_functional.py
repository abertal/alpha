import pytest

from . import pages


@pytest.mark.selenium
def test_main(selenium, live_server, admin_user):
    selenium.maximize_window()
    selenium.get(live_server.url)
    (
        pages
        .Login(selenium)
        .login('admin', 'password')
        .logout()
    )
    selenium.quit()
