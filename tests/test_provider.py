# SPDX-License-Identifier: Apache-2.0
import pytest

from jjones_core.provider import ProviderRequest, require_explicit_auth


def test_explicit_authentication_is_required():
    with pytest.raises(PermissionError):
        require_explicit_auth(None)
    assert require_explicit_auth("token") == "token"
    assert ProviderRequest("hello", "public").max_tokens == 1024
