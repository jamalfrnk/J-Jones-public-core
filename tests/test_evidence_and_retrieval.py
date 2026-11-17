# SPDX-License-Identifier: Apache-2.0
from jjones_core.evidence import build_manifest, verify_manifest
from jjones_core.retrieval import LocalIndex


def test_manifest_and_rebuildable_index():
    data = b"hello"
    manifest = build_manifest("e-1", "notes/a.md", data)
    assert verify_manifest(manifest, data)
    assert not verify_manifest(manifest, b"changed")
    index = LocalIndex()
    index.rebuild([("n-1", "Alpha", "local knowledge")])
    assert index.search("knowledge")[0].note_id == "n-1"
    index.clear()
    assert index.search("knowledge") == []
    index.close()
